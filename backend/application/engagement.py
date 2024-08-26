from flask import Blueprint, jsonify, request
from .tools import token_to_user
from .postgres import db_close, db_open
from .log import log
from .post_get import post_schema
import json

bp = Blueprint("engagement", __name__)


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

    error = {}
    if "rating" not in request.json or not request.json["rating"]:
        error["rating"] = "cannot be empty"
    elif (
        type(request.json["rating"]) is not int
        or request.json["rating"] not in range(-5, 6)
    ):
        error["rating"] = "invalid rating"

    if error != {}:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            **error
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
