from flask import Blueprint, jsonify, request
from math import ceil
import re
import os
from ..postgres import db_open, db_close
from ..tools import get_session

bp = Blueprint("post_get", __name__)


def post_schema(post):
    post["photo"] = (f"{request.host_url}file/{post['photo']}"
                     if post['photo'] else None)
    post["files"] = [f"{request.host_url}file/{x}" for x in post["files"]]
    return post


@bp.get("/post/<key>")
def get(key):
    con, cur = db_open()

    session = get_session(cur)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    cur.execute("""
        SELECT * FROM post WHERE slug = %s OR key::TEXT = %s
    """, (key, key))
    item = cur.fetchone()

    if not item:
        db_close(con, cur)
        return jsonify({
            "status": 404,
            "error": "Oops! The post you're looking for doesn't exist"
        })

    if (
        item["status"] != "active"
        and "post:add" not in user["access"]
        and "post:edit_status" not in user["access"]
    ):
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "unauthorized access"
        })

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "item": post_schema(item)
    })


@bp.get("/posts")
def get_many(cur=None):
    close_conn = not cur
    if not cur:
        con, cur = db_open()

    session = get_session(cur)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    search = request.args.get("search", "").strip()
    status = request.args.get("status", "active")
    tag = request.args.get("tag", "")
    order = request.args.get("order", "latest")
    page_no = int(request.args.get("page_no", 1))
    page_size = int(request.args.get("page_size", 24))

    if (
        "post:edit_status" not in user["access"]
        or "post:add" not in user["access"]
    ):
        status = "active"

    multiply = False
    if tag[-4:] == ":all":
        multiply = True
        tag = tag[:-4]
    tags = tag.split(",")
    tags = [] if not tags[0] else tags

    order_by = {
        'latest': 'post.date_created',
        'oldest': 'post.date_created',
        'title (a-z)': 'post.title',
        'title (z-a)': 'post.title',
        'comment': "COALESCE(comment._count, 0)",
        'view': "COALESCE(view._count, 0)",
        'like': 'COALESCE("like"._count, 0)'

    }

    order_dir = {
        'latest': 'DESC',
        'oldest': 'ASC',
        'title (a-z)': 'ASC',
        'title (z-a)': 'DESC',
        'comment': 'DESC',
        'view': 'DESC',
        'like': 'DESC'
    }

    params = [status, search, f"%{search}%"]
    tag_query = ""
    if tags != []:
        op = "@>" if multiply else "&&"
        tag_query = f"AND cardinality(post.tags) > 0 AND post.tags {op} %s"
        params.append(tags)
    params.append(page_size)
    params.append((page_no - 1) * page_size)

    cur.execute(f"""
        WITH
        "like" AS (
            SELECT
                entity_key AS key,
                COUNT(*) FILTER (WHERE reaction = 'like') -
                COUNT(*) FILTER (WHERE reaction = 'dislike') AS _count
            FROM "like"
            WHERE entity_type = 'post'
            GROUP BY entity_key
        ),

        comment AS (
            SELECT post_key AS key, COUNT(*) AS _count
            FROM comment
            GROUP BY post_key
        ),

        view AS (
            SELECT entity_key::UUID AS key, COUNT(DISTINCT user_key) AS _count
            FROM log
            WHERE entity_type = 'post' AND action = 'viewed'
            GROUP BY entity_key
        ),

        share AS (
            SELECT entity_key::UUID AS key, COUNT(*) AS _count
            FROM log
            WHERE entity_type = 'post' AND action = 'shared'
            GROUP BY entity_key
        )

        SELECT
            post.*,
            COUNT(*) OVER() AS _count,
            jsonb_build_object(
                'comment', COALESCE(comment._count, 0),
                'view', COALESCE(view._count, 0),
                'share', COALESCE(share._count, 0),
                'like', COALESCE("like"._count, 0)
            ) AS engagement
        FROM post
        LEFT JOIN "like" ON post.key = "like".key
        LEFT JOIN comment ON post.key = comment.key
        LEFT JOIN view ON post.key = view.key
        LEFT JOIN share ON post.key = share.key

        WHERE
            post.status = %s
            AND (%s = '' OR post.title ILIKE %s) {tag_query}
        GROUP BY
            post.key, post.status, post.title, post.slug, post.content,
            post.description, post.files, post.tags,
            "like"._count, comment._count, view._count, share._count
        ORDER BY {order_by[order]} {order_dir[order]}
        LIMIT %s OFFSET %s;
    """, (params))
    items = cur.fetchall()

    if close_conn:
        db_close(con, cur)
    return jsonify({
        "status": 200,
        "items": [post_schema(x) for x in items],
        "order_by": list(order_by.keys()),
        "_status": ['active', 'draft'],
        "total_page": ceil(items[0]["_count"] / page_size) if items else 0
    })


@bp.get("/post/similar/<key>")
def similar_posts(key):
    con, cur = db_open()

    cur.execute("""
        SELECT * FROM post WHERE key = %s;
    """, (key,))
    post = cur.fetchone()

    if not post:
        db_close(con, cur)
        return jsonify({
            "status": 200,
            "items": []
        })

    keywords = list(set(
        post["tags"] + re.split(r'\s+', post["title"].lower())))

    cur.execute("""
        WITH likeness AS (
            SELECT key, COUNT(*) AS score
            FROM post,
                unnest(tags || STRING_TO_ARRAY(lower(title), ' ')) AS tn
            WHERE tn = ANY(%s)
            GROUP BY key
        )
        SELECT post.*
        FROM post
        JOIN likeness ON post.key = likeness.key
        WHERE post.status = 'active'
            AND post.key != %s
            AND likeness.score > 0
        ORDER BY likeness.score DESC
        LIMIT 4;
    """, (keywords, key))
    items = cur.fetchall()

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "items": [post_schema(x) for x in items]
    })


@bp.get("/post/author/<key>")
def get_author(key):
    con, cur = db_open()

    cur.execute("""
        SELECT "user".key, "user".name,  "user".username, "user".photo
        FROM post
        LEFT JOIN "user" ON post.author_key = "user".key
        WHERE post.key = %s;
    """, (key,))
    item = cur.fetchone()
    if not item:
        cur.execute("""
            SELECT key, name, photo FROM "user" WHERE email = %s;
        """, (os.environ["MAIL_USERNAME"],))
        item = cur.fetchone()
    if not item:
        db_close(con, cur)
        return jsonify({
            "status": 400
        })

    item["photo"] = (
        f"{request.host_url}file/{item['photo']}"
        if item["photo"] else None
    )

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "item": item
    })


@bp.get("/tags")
def all_tags():
    con, cur = db_open()

    cur.execute("SELECT tags FROM post WHERE status = 'active';")
    temp = cur.fetchall()

    tags = []
    for x in temp:
        tags += x["tags"]

    tags_count = []
    unique_tags = []
    for x in tags:
        if x not in unique_tags:
            unique_tags.append(x)
            tags_count.append({
                "tag":  x,
                "count":  tags.count(x)
            })

    tags_count = sorted(tags_count, key=lambda d: d["count"], reverse=True)

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "tags": [x["tag"] for x in tags_count]
    })
