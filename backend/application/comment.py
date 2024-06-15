from flask import Blueprint, jsonify, request
from .tools import token_to_user
from uuid import uuid4
from .postgres import db_close, db_open
from .log import log

bp = Blueprint("comment", __name__)


@bp.get("/comment/<key>")
def get_comments(key):
    con, cur = db_open()

    order = request.args["order"] if "order" in request.args else "latest"

    order_by = {
        'latest': 'log.date',
        'oldest': 'log.date',
        'high_rating': 'feedback.rating',
        'low_rating': 'feedback.rating',
        'name (a-z)': '"user".name',
        'name (z-a)': '"user".name'
    }

    order_dir = {
        'latest': 'DESC',
        'oldest': 'ASC',
        'high_rating': 'DESC',
        'low_rating': 'ASC',
        'name (a-z)': 'ASC',
        'name (z-a)': 'DESC'
    }

    cur.execute("""
        SELECT
            comment.key,
            comment.comment,
            comment.path,
            comment.upvote,
            comment.downvote,
            log.date AS date,
            "user".key AS user_key,
            "user".name AS user_name,
            "user".photo AS user_photo,
            COUNT(*) OVER() AS total_items
        FROM comment
        LEFT JOIN log ON comment.key = log.entity_key
        LEFT JOIN "user" ON comment.user_key = "user".key
        WHERE
            comment.post_key = %s
            AND comment.status = 'active'
            AND log.action = 'added_comment'
            AND log.entity_type = 'comment'
        ORDER BY {} {};
    """.format(order_by[order], order_dir[order]), (key,))
    comments = cur.fetchall()
    for x in comments:
        x["user_photo"] = f"{request.host_url}photo/{x[
            "user_photo"]}" if x["user_photo"] else None

    cur.execute("""
        SELECT
            COALESCE(ARRAY_AGG(rating), ARRAY[]::int[]) AS ratings
        FROM rating
        WHERE post_key = %s;
    """, (key,))
    ratings = cur.fetchone()

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "comments": comments,
        "ratings": ratings["ratings"],
        "order_by": list(order_by.keys())
    })


@bp.post("/comment/<key>")
def create(key):
    con, cur = db_open()

    user = token_to_user(cur)
    if not user or not user["login"]:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    cur.execute("""
        SELECT * FROM post WHERE slug = %s OR key = %s;
    """, (key, key))
    post = cur.fetchone()

    if (
        not post
        or "path" not in request.json
        or type(request.json["path"]) is not list
    ):
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    if "comment" not in request.json or not request.json["comment"]:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "comment": "This field is required"
        })

    cur.execute("""
        SELECT * FROM comment WHERE key = ANY(%s);
    """, (request.json["path"],))
    comments = cur.fetchall()
    if len(comments) != len(request.json["path"]):
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    cur.execute("""
        INSERT INTO comment (key, user_key, post_key, comment, path)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING *;
    """, (
        uuid4().hex,
        user["key"],
        post["key"],
        request.json["comment"],
        request.json["path"]
    ))
    comment = cur.fetchone()

    log(
        cur=cur,
        user_key=user["key"],
        action="added_comment",
        entity_key=comment["key"],
        entity_type="comment",
        misc={
            "comment":  request.json["comment"],
            "path": request.json["path"]
        }
    )

    db_close(con, cur)
    return get_comments(post["key"])


@bp.post("/comment/vote/<key>")
def vote(key):
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    cur.execute("""
        SELECT
            comment.key,
            comment.comment,
            comment.path,
            comment.upvote,
            comment.downvote,
            log.date AS date,
            "user".key AS user_key,
            "user".name AS user_name,
            "user".photo AS user_photo
        FROM comment
        LEFT JOIN log ON comment.key = log.entity_key
        LEFT JOIN "user" ON comment.user_key = "user".key
        WHERE comment.key = %s;
    """, (key,))
    comment = cur.fetchone()

    if (
        not comment
        or "vote" not in request.json
        or not request.json["vote"]
        or request.json["vote"] not in ["up", "down"]
    ):
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    if request.json["vote"] == "up":
        if user["key"] in comment["downvote"]:
            comment["downvote"].remove(user["key"])
        if user["key"] in comment["upvote"]:
            comment["upvote"].remove(user["key"])
        else:
            comment["upvote"].append(user["key"])
    elif request.json["vote"] == "down":
        if user["key"] in comment["upvote"]:
            comment["upvote"].remove(user["key"])
        if user["key"] in comment["downvote"]:
            comment["downvote"].remove(user["key"])
        else:
            comment["downvote"].append(user["key"])

    cur.execute("""
        UPDATE comment
        SET
            upvote = %s,
            downvote = %s
        WHERE key = %s;
    """, (
        comment["upvote"],
        comment["downvote"],
        comment["key"]
    ))
    comment["user_photo"] = f"{request.host_url}photo/{comment[
        "user_photo"]}" if comment["user_photo"] else None

    log(
        cur=cur,
        user_key=user["key"],
        action="voted",
        entity_key=comment["key"],
        entity_type="comment",
        misc={
            "vote": request.json["vote"]
        }
    )

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "comment": comment
    })


@ bp.delete("/comment/<key>")
def delete(key):
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    cur.execute("""
        SELECT * FROM comment WHERE key = %s AND user_key = %s;
    """, (key, user["key"]))
    comment = cur.fetchone()

    if not comment:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    cur.execute("""
        UPDATE comment
        SET status = 'deleted'
        WHERE
            key = %s
            OR %s = ANY(path);
    """, (
        comment["key"],
        comment["key"]
    ))

    log(
        cur=cur,
        user_key=user["key"],
        action="deleted",
        entity_key=comment["key"],
        entity_type="comment",
    )

    db_close(con, cur)
    return get_comments(comment["post_key"], )
