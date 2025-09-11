from flask import Blueprint, jsonify, request
from psycopg2.extras import Json
from ...tools import get_session
from ...postgres import db_close, db_open
from ...log import log
from ..get import post_schema

bp = Blueprint("post_engage", __name__)


@bp.post("/post/like/<key>")
def like(key):
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    cur.execute("""
        SELECT * FROM post WHERE post.key = %s;
    """, (key,))
    post = cur.fetchone()

    like = request.json.get("like")

    if not post or not like or type(like) is not bool:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    if like:
        if user["key"] in post["dislikes"]:
            post["dislikes"].remove(user["key"])
        if user["key"] in post["likes"]:
            post["likes"].remove(user["key"])
        else:
            post["likes"].append(user["key"])
    else:
        if user["key"] in post["likes"]:
            post["likes"].remove(user["key"])
        if user["key"] in post["dislikes"]:
            post["dislikes"].remove(user["key"])
        else:
            post["dislikes"].append(user["key"])

    cur.execute("""
        UPDATE post SET likes = %s, dislikes = %s
        WHERE key = %s RETURNING *;
    """, (post["likes"], post["dislikes"], post["key"]))
    post = cur.fetchone()

    log(
        cur=cur,
        user_key=user["key"],
        action='liked' if like else 'disliked',
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

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    cur.execute("""
        SELECT * FROM post WHERE key = %s;
    """, (key,))
    post = cur.fetchone()

    if not post:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    rating = request.json.get("rating")

    error = None
    if not rating and rating != 0:
        error = "This field is required"
    elif type(rating) is not int or rating not in range(-5, 6):
        error = "invalid rating"
    elif rating == 0:
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
        "rating": rating
    })

    cur.execute("""
        UPDATE post
        SET ratings = %s::JSONB[]
        WHERE key = %s
        RETURNING *;
    """, (
        [Json(x) for x in post["ratings"]],
        post["key"]
    ))
    post = cur.fetchone()

    log(
        cur=cur,
        user_key=user["key"],
        action="rated",
        entity_key=post["key"],
        entity_type="post",
        misc={"rating":  rating}
    )

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "post": post_schema(post)
    })
