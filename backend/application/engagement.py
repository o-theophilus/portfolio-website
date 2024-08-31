from flask import Blueprint, jsonify, request
from .tools import token_to_user
from .postgres import db_close, db_open
from .log import log
from .post_get import post_schema
import json

bp = Blueprint("engagement", __name__)


@bp.get("/post/engagements/<key>")
def get_engagements(key):
    con, cur = db_open()

    cur.execute("""
        SELECT * FROM post WHERE post.slug = %s OR post.key = %s;
    """, (key, key))
    post = cur.fetchone()

    if not post:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    cur.execute("""
        WITH
        _like AS (
            SELECT
                key,
                COALESCE(array_length("like", 1), 0) -
                COALESCE(array_length(dislike, 1), 0) AS _count
            FROM post
        ),

        ratings AS (
            SELECT key, (unnest(ratings) ->> 'rating')::INTEGER AS ratings
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
            WHERE
                status = 'active'
            GROUP BY post_key
        ),

        view1 AS (
            SELECT
                DISTINCT ON (user_key, entity_key)
                entity_key
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
            SELECT entity_key
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

        WHERE post.key = %s
        GROUP BY
            post.key, post.status, post.title, post.slug, post.content,
            post.description, post.files, post.tags,
            _like._count, comment._count, view._count, share._count,
            rating.rating
    ;""", (post["key"],))
    post = cur.fetchone()

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "post": post_schema(post)
    })


@ bp.post("/post/like/<key>")
def like(key):
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    cur.execute("""
        SELECT * FROM post WHERE post.key = %s;
    """, (key,))
    post = cur.fetchone()

    if (
        not post
        or "like" not in request.json
        or type(request.json["like"]) is not bool
    ):
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    if request.json["like"]:
        if user["key"] in post["dislike"]:
            post["dislike"].remove(user["key"])
        if user["key"] in post["like"]:
            post["like"].remove(user["key"])
        else:
            post["like"].append(user["key"])
    else:
        if user["key"] in post["like"]:
            post["like"].remove(user["key"])
        if user["key"] in post["dislike"]:
            post["dislike"].remove(user["key"])
        else:
            post["dislike"].append(user["key"])

    cur.execute("""
        UPDATE post
        SET "like" = %s, dislike = %s
        WHERE key = %s
        RETURNING *;
    """, (
        post["like"],
        post["dislike"],
        post["key"]
    ))
    post = cur.fetchone()

    log(
        cur=cur,
        user_key=user["key"],
        action='liked' if request.json['like'] else 'disliked',
        entity_key=post["key"],
        entity_type="post"
    )

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "post": post_schema(post)
    })


@bp.post("/rating/<key>")
def rating(key):
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    cur.execute("""
        SELECT * FROM post WHERE key = %s;
    """, (key,))
    post = cur.fetchone()

    if not post:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    error = None
    if "rating" not in request.json or (
            not request.json["rating"] and request.json["rating"] != 0):
        error = "cannot be empty"
    elif (
        type(request.json["rating"]) is not int
        or request.json["rating"] not in range(-5, 6)
    ):
        error = "invalid rating"
    elif request.json["rating"] == 0:
        error = "cannot rate 0"

    if error:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": error
        })

    for x in post["ratings"]:
        if x["user_key"] == user["key"]:
            post["ratings"].remove(x)

    post["ratings"].append({
        "user_key": user["key"],
        "rating": request.json["rating"]
    })

    cur.execute("""
        UPDATE post
        SET ratings = %s::JSONB[]
        WHERE key = %s
        RETURNING *;
    """, (
        [json.dumps(x) for x in post["ratings"]],
        post["key"]
    ))
    post = cur.fetchone()

    log(
        cur=cur,
        user_key=user["key"],
        action="rated",
        entity_key=post["key"],
        entity_type="post",
        misc={
            "rating":  request.json["rating"]
        }
    )

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "post": post_schema(post)
    })
