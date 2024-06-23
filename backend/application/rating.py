from flask import Blueprint, jsonify, request
from .tools import token_to_user
from uuid import uuid4
from .postgres import db_close, db_open
from .log import log

bp = Blueprint("rating", __name__)


@bp.get("/rating/<key>")
def get_ratings(key, cur=None):
    close_conn = not cur
    if not cur:
        con, cur = db_open()

    cur.execute("""
        SELECT
            rating.rating,
            "user".key AS user_key
        FROM rating
        LEFT JOIN "user" ON rating.user_key = "user".key
        WHERE
            rating.post_key = %s
    """, (key,))
    ratings = cur.fetchall()

    if close_conn:
        db_close(con, cur)
    return jsonify({
        "status": 200,
        "ratings": ratings
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
    elif request.json["rating"] not in range(-5, 6):
        error["rating"] = "invalid rating"

    if error != {}:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            **error
        })

    cur.execute("""
        SELECT * FROM rating WHERE user_key = %s AND post_key = %s;
    """, (user["key"], post["key"]))
    rating = cur.fetchone()
    if rating:
        cur.execute("""
            DELETE FROM rating WHERE user_key = %s AND post_key = %s;
        """, (user["key"], post["key"]))

    cur.execute("""
        INSERT INTO rating (key, user_key, post_key, rating)
        VALUES (%s, %s, %s, %s);
    """, (
        uuid4().hex,
        user["key"],
        post["key"],
        request.json["rating"]
    ))

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

    ratings = get_ratings(post["key"], cur).json["ratings"]

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "ratings": ratings
    })
