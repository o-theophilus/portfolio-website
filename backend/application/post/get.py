import os
import re
from math import ceil

from flask import Blueprint, jsonify, request

from ..postgres import db_close, db_open
from ..tools import get_session
from .comment.get import get_many as get_comments

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
        "post": post_schema(item)
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

    order_by = {
        'latest': 'post.date_created',
        'oldest': 'post.date_created',
        'title (a-z)': 'post.title',
        'title (z-a)': 'post.title',
        'comment': "COALESCE(c._count, 0)",
        'like': 'COALESCE(l."like", 0) - COALESCE(l.dislike, 0)',
        'view': "COALESCE(v._count, 0)"
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

    searchParams = {
        "search": "",
        "status": "active",
        "tag": "",
        "order": "latest",
        "page_no": 1,
        "page_size": 24
    }
    search = request.args.get("search", searchParams["search"]).strip()
    status = request.args.get("status", searchParams["status"])
    tag = request.args.get("tag", searchParams["tag"])
    order = request.args.get("order", searchParams["order"])
    page_no = int(request.args.get("page_no", searchParams["page_no"]))
    page_size = int(request.args.get("page_size", searchParams["page_size"]))
    page_size = min(page_size, 100)

    if (
        "post:edit_status" not in user["access"]
        and "post:add" not in user["access"]
    ):
        status = "active"

    params = [status, search, f"%{search}%"]

    op = "&&"
    tag_query = ""
    if tag[-4:] == ":all":
        op = "@>"
        tag = tag[:-4]
    tags = tag.split(",") if tag else []
    if tags != []:
        tag_query = f"AND cardinality(post.tags) > 0 AND post.tags {op} %s"
        params.append(tags)

    cur.execute(f"""
        SELECT
            post.*,
            jsonb_build_object(
                'comment', COALESCE(c._count, 0),
                'like', COALESCE(l."like", 0) - COALESCE(l.dislike, 0),
                'view', COALESCE(v._count, 0),
                'share', COALESCE(s._count, 0)
            ) AS engagement

        FROM post

        LEFT JOIN (
            SELECT post_key, COUNT(*) AS _count
            FROM comment
            GROUP BY post_key
        ) c ON c.post_key = post.key

        LEFT JOIN (
            SELECT post_key,
                COUNT(*) FILTER (WHERE reaction = 'like') AS "like",
                COUNT(*) FILTER (WHERE reaction = 'dislike') AS dislike
            FROM "like"
            WHERE post_key IS NOT NULL
            GROUP BY post_key
        ) l ON l.post_key = post.key

        LEFT JOIN (
            SELECT entity_key, COUNT(DISTINCT user_key) AS _count
            FROM log
            WHERE entity_type = 'post'
                AND action = 'viewed'
            GROUP BY entity_key
        ) v ON v.entity_key = post.key::TEXT

        LEFT JOIN (
            SELECT entity_key, COUNT(DISTINCT user_key) AS _count
            FROM log
            WHERE entity_type = 'post'
                AND action = 'shared'
            GROUP BY entity_key
        ) s ON s.entity_key = post.key::TEXT

        WHERE post.status = %s
            AND (%s = '' OR post.title ILIKE %s) {tag_query}
        ORDER BY {order_by[order]} {order_dir[order]}, post.key DESC
        LIMIT %s OFFSET %s;
    """, (*params, page_size, (page_no - 1) * page_size))
    posts = cur.fetchall()

    cur.execute(f"""
        SELECT COUNT(*) FROM post
        WHERE post.status = %s
            AND (%s = '' OR post.title ILIKE %s) {tag_query}
    """, (*params,))
    total_page = cur.fetchone()["count"]

    if close_conn:
        db_close(con, cur)
    return jsonify({
        "status": 200,
        "posts": [post_schema(x) for x in posts],
        "order_by": list(order_by.keys()),
        "_status": ['active', 'draft'],
        "total_page": ceil(total_page / page_size),
        "searchParams": searchParams
    })


def get_engagement(cur, key, user_key):
    cur.execute("""
        SELECT
            COUNT(CASE WHEN user_key != %s
                AND reaction = 'like' THEN 1 END) AS others_like,
            COUNT(CASE WHEN user_key != %s
                AND reaction = 'dislike' THEN 1 END) AS others_dislike,
            MAX(CASE WHEN user_key = %s THEN reaction END) AS user_reaction
        FROM "like"
        WHERE post_key = %s
    """, (user_key, user_key, user_key, key))
    reactions = cur.fetchone()

    cur.execute("SELECT COUNT(*) FROM comment WHERE post_key = %s", (key,))
    comment_count = cur.fetchone()["count"]

    cur.execute("""
        SELECT COUNT(DISTINCT user_key) FROM log
        WHERE entity_type = 'post' AND action = 'viewed' AND entity_key = %s
    """, (key,))
    view_count = cur.fetchone()["count"]

    cur.execute("""
        SELECT COUNT(*) FROM log
        WHERE entity_type = 'post' AND action = 'shared' AND entity_key = %s
    """, (key,))
    share_count = cur.fetchone()["count"]

    return {
        "comment": comment_count,
        "view": view_count,
        "share": share_count,
        **reactions,
    }


def get_author(cur, key):
    cur.execute("""
        SELECT "user".key, "user".name,  "user".username, "user".photo
        FROM post
        LEFT JOIN "user" ON post.author_key = "user".key
        WHERE post.key = %s;
    """, (key,))
    author = cur.fetchone()
    if not author:
        cur.execute("""
            SELECT key, name, photo FROM "user" WHERE email = %s;
        """, (os.environ["MAIL_USERNAME"],))
        author = cur.fetchone()
    if not author:
        return None

    author["photo"] = (
        f"{request.host_url}file/{author['photo']}"
        if author["photo"] else None
    )

    return author


def get_similar(cur, key):
    cur.execute("""SELECT * FROM post WHERE key = %s;""", (key,))
    post = cur.fetchone()
    if not post:
        return []

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
    posts = cur.fetchall()

    return [post_schema(x) for x in posts]


@bp.get("/post/after/<key>")
def after_post(key):
    con, cur = db_open()

    session = get_session(cur)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    engagement = get_engagement(cur, key, user["key"])
    author = get_author(cur, key)
    comment = get_comments(key, cur).json
    similar = get_similar(cur, key)

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "engagement": engagement,
        "author": author,
        "comment": {
            "comments": comment["comments"],
            "order_by": comment["order_by"]
        },
        "similar": similar
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
