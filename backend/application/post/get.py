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
def get_post(key):
    con, cur = db_open()

    # NOTE: validate session only
    session = get_session(cur)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)

    cur.execute("""
        SELECT * FROM post WHERE post.slug = %s OR post.key::TEXT = %s;
    """, (key, key))
    post = cur.fetchone()

    if not post:
        db_close(con, cur)
        return jsonify({
            "status": 404,
            "error": "Oops! The post you’re looking for doesn’t exist"
        })

    if post["status"] != "active":
        session = get_session(cur, True)
        if session["status"] != 200:
            db_close(con, cur)
            return jsonify(session)
        user = session["user"]

        if (
            "post:add" not in user["access"]
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
        "post": post_schema(post)
    })


@bp.get("/post")
def get_all(cur=None):
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
    if tag[-2:] == ":x":
        multiply = True
        tag = tag[:-2]
    tags = tag.split(",")
    tags = [] if not tags[0] else tags

    order_by = {
        'latest': 'post.date_created',
        'oldest': 'post.date_created',
        'title (a-z)': 'post.title',
        'title (z-a)': 'post.title',
        'rating': 'rating',
        'comment': 'comment',
        'view': 'view',
        'like': '_like'

    }

    order_dir = {
        'latest': 'DESC',
        'oldest': 'ASC',
        'title (a-z)': 'ASC',
        'title (z-a)': 'DESC',
        'rating': 'DESC',
        'comment': 'DESC',
        'view': 'DESC',
        'like': 'DESC'
    }

    query = ""
    if tags != []:
        query = f"""
            AND cardinality(post.tags) > 0
            AND post.tags {"@>" if multiply else "&&"} ARRAY[{tags}]
        """

    cur.execute("""
        WITH
        _like AS (
            SELECT
                key,
                COALESCE(array_length(likes, 1), 0) -
                COALESCE(array_length(dislikes, 1), 0) AS _count
            FROM post
        ),

        ratings AS (
            SELECT key,
            (jsonb_array_elements(ratings) ->> 'rating')::INTEGER AS ratings
            FROM post
        ),
        rating AS (
            SELECT key, AVG(ratings) AS rating
            FROM ratings
            GROUP BY key
        ),

        comment AS (
            SELECT
                post_key AS key,
                COUNT(*) AS _count
            FROM comment
            GROUP BY post_key
        ),

        view1 AS (
            SELECT
                DISTINCT ON (user_key, entity_key)
                entity_key::UUID
            FROM log
            WHERE
                entity_type = 'post'
                AND action = 'viewed'
        ),
        view AS (
            SELECT
                entity_key AS key,
                COUNT(*) AS _count
            FROM view1
            GROUP BY entity_key
        ),

        share1 AS (
            SELECT entity_key::UUID
            FROM log
            WHERE
                entity_type = 'post'
                AND action = 'shared'
        ),
        share AS (
            SELECT
                entity_key AS key,
                COUNT(*) AS _count
            FROM share1
            GROUP BY entity_key
        )

        SELECT
            post.*,
            COALESCE(rating.rating, 0) AS rating,
            COALESCE(comment._count, 0) AS comment,
            COALESCE(view._count, 0) AS view,
            COALESCE(share._count, 0) AS share,
            COALESCE(_like._count, 0) AS _like,
            COUNT(*) OVER() AS _count
        FROM post
        LEFT JOIN _like ON post.key = _like.key
        LEFT JOIN rating ON post.key = rating.key
        LEFT JOIN comment ON post.key = comment.key
        LEFT JOIN view ON post.key = view.key
        LEFT JOIN share ON post.key = share.key

        WHERE
            post.status = %s
            AND (%s = '' OR post.title ILIKE %s) {}
        GROUP BY
            post.key, post.status, post.title, post.slug, post.content,
            post.description, post.files, post.tags,
            _like._count, comment._count, view._count, share._count,
            rating.rating
        ORDER BY {} {}
        LIMIT %s OFFSET %s;
    """.format(
        query,
        order_by[order],
        order_dir[order]
    ), (
        status,
        search, f"%{search}%",
        page_size, (page_no - 1) * page_size
    ))
    posts = cur.fetchall()

    if close_conn:
        db_close(con, cur)
    return jsonify({
        "status": 200,
        "posts": [post_schema(x) for x in posts],
        "order_by": list(order_by.keys()),
        "_status": ['active', 'draft'],
        "total_page": ceil(posts[0]["_count"] / page_size) if posts else 0
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
            "posts": []
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
    posts = cur.fetchall()

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "posts": [post_schema(x) for x in posts]
    })


@bp.get("/post/author/<key>")
def get_author(key):
    con, cur = db_open()

    cur.execute("""
        SELECT "user".key, "user".name, "user".photo
        FROM post
        LEFT JOIN "user" ON post.author_key = "user".key
        WHERE post.key = %s;
    """, (key,))
    user = cur.fetchone()
    if not user:
        cur.execute("""
            SELECT key, name, photo FROM "user" WHERE email = %s;
        """, (os.environ["MAIL_USERNAME"],))
        user = cur.fetchone()
    if not user:
        db_close(con, cur)
        return jsonify({
            "status": 400
        })

    user["photo"] = (
        f"{request.host_url}file/{user['photo']}"
        if user["photo"] else None
    )

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "user": user
    })


@bp.get("/tag")
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
