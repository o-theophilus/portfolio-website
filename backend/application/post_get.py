from flask import Blueprint, jsonify, request
from .postgres import db_open, db_close
from .tools import token_to_user
from math import ceil

bp = Blueprint("post_read", __name__)


@bp.get("/tag")
def all_tags():
    con, cur = db_open()

    cur.execute("SELECT tags FROM post WHERE status = 'publish';")
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


@bp.get("/post/<key>")
def get_post(key, cur=None):
    close_conn = not cur
    if not cur:
        con, cur = db_open()

    cur.execute("""
        SELECT
            post.*,
            COALESCE(ARRAY_AGG(feedback.rating), ARRAY[]::int[]) AS ratings
        FROM post
        LEFT JOIN feedback ON post.key = feedback.post_key
        WHERE post.slug = %s OR post.key = %s
        GROUP BY post.key;
    """, (key, key))
    post = cur.fetchone()

    if not post:
        if close_conn:
            db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    if post["status"] != "publish":
        user = token_to_user(cur)
        if not user:
            if close_conn:
                db_close(con, cur)
            return jsonify({
                "status": 400,
                "error": "invalid token"
            })

        if set([
            "post:add",
            "post:edit_status"
        ]).isdisjoint(user["permissions"]):
            if close_conn:
                db_close(con, cur)
            return jsonify({
                "status": 400,
                "error": "unauthorized access"
            })

    post["photos"] = [f"{request.host_url}photo/{x}" for x in post["photos"]]

    if close_conn:
        db_close(con, cur)
    return jsonify({
        "status": 200,
        "post": post
    })


@bp.get("/post")
def get_all(order="latest", page_size=24):
    con, cur = db_open()
    user = token_to_user(cur)

    status = "publish"
    search = ""
    tag = ""
    page_no = 1

    if (
        "status" in request.args and user and (
            "post:edit_status" in user["permissions"]
            or "post:add" in user["permissions"]
        )
    ):
        status = request.args["status"]
    if "search" in request.args:
        search = request.args["search"].strip()
    if "order" in request.args:
        order = request.args["order"]
    if "page_no" in request.args:
        page_no = int(request.args["page_no"])
    if "page_size" in request.args:
        page_size = int(request.args["page_size"])
    if "tag" in request.args:
        tag = request.args["tag"]
    multiply = False
    if tag[-2:] == ":x":
        multiply = True
        tag = tag[:-2]
    tags = tag.split(",")
    tags = [] if not tags[0] else tags

    order_by = {
        'latest': 'post.date',
        'oldest': 'post.date',
        'title (a-z)': 'post.title',
        'title (z-a)': 'post.title',
        'rating': 'rating'
    }

    order_dir = {
        'latest': 'DESC',
        'oldest': 'ASC',
        'title (a-z)': 'ASC',
        'title (z-a)': 'DESC',
        'rating': 'DESC'
    }

    query = ""
    if tags != []:
        query = f"""
            AND cardinality(post.tags) > 0
            AND post.tags {"@>" if multiply else "&&"} ARRAY[{tags}]
        """

    cur.execute("""
        SELECT
            post.*,
            COALESCE(AVG(feedback.rating), 0) AS rating,
            COALESCE(ARRAY_AGG(feedback.rating), ARRAY[]::int[]) AS ratings,
            COUNT(*) OVER() AS total_posts
        FROM post
        LEFT JOIN feedback ON post.key = feedback.post_key
        WHERE
            post.status = %s
            AND (%s = '' OR post.title ILIKE %s) {}
        GROUP BY
            post.key, post.status, post.title, post.slug, post.content,
            post.description, post.photos, post.videos, post.tags
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
    for x in posts:
        x["photos"] = [f"{request.host_url}photo/{y}" for y in x["photos"]]

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "posts": posts,
        "order_by": list(order_by.keys()),
        "post_status": ['publish', 'draft', 'delete'],
        "total_page": ceil(posts[0]["total_posts"] / page_size) if posts else 0
    })
