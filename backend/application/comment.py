from flask import Blueprint, jsonify, request
from .tools import get_session
from uuid import uuid4
from .postgres import db_close, db_open
from .log import log
from datetime import datetime, timezone

bp = Blueprint("comment", __name__)


@bp.get("/comment/<key>")
def get_comments(key, cur=None):
    close_conn = not cur
    if not cur:
        con, cur = db_open()

    order = "latest"
    if "order" in request.args:
        order = request.args["order"]

    order_by = {
        'latest': 'comment.date',
        'oldest': 'comment.date',
        'likes': 'likes_count',
        'dislikes': 'dislikes_count',
        'most_liked': 'most_liked',
        'reply': 'reply_count',
        'most_reaction': 'total_reactions',
    }

    order_dir = {
        'latest': 'DESC',
        'oldest': 'ASC',
        'likes': 'DESC',
        'dislikes': 'DESC',
        'most_liked': 'DESC',
        'reply': 'DESC',
        'most_reaction': 'DESC',
    }

    cur.execute(f"""
        WITH stats AS (
            SELECT
                key,
                COALESCE(array_length(likes, 1), 0) AS likes_count,
                COALESCE(array_length(dislikes, 1), 0) AS dislikes_count,
                COALESCE(array_length(likes, 1), 0)
                    - COALESCE(array_length(dislikes, 1), 0) AS most_liked
            FROM comment
            WHERE post_key = %s
        ),
        reply AS (
            SELECT parent_key AS key, COUNT(*) AS reply_count
            FROM comment
            WHERE parent_key IS NOT NULL AND post_key = %s
            GROUP BY parent_key
        )

        SELECT
            comment.key,
            comment.comment,
            comment.parent_key,
            comment.likes,
            comment.dislikes,
            comment.date,
            jsonb_build_object(
                'key', "user".key,
                'name', "user".name,
                'photo', "user".photo
            ) AS user,

            stats.likes_count AS likes_count,
            stats.dislikes_count AS dislikes_count,
            stats.most_liked AS most_liked,
            COALESCE(reply.reply_count, 0) AS reply_count,
            (stats.likes_count + stats.dislikes_count
                + COALESCE(reply.reply_count, 0)) AS total_reactions


        FROM comment
        LEFT JOIN stats ON comment.key = stats.key
        LEFT JOIN reply ON comment.key = reply.key
        LEFT JOIN "user" ON comment.user_key = "user".key

        WHERE comment.post_key = %s

        ORDER BY {order_by[order]} {order_dir[order]};
    """, (key, key, key))

    comments = cur.fetchall()
    for x in comments:
        x["user"]["photo"] = (
            f"{request.host_url}file/{x['user']['photo']}"
            if x["user"]["photo"] else None
        )

    if close_conn:
        db_close(con, cur)
    return jsonify({
        "status": 200,
        "comments": comments,
        "order_by": list(order_by.keys()),
    })


@bp.post("/comment/<key>")
def create(key):
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    cur.execute("""
        SELECT * FROM post WHERE slug = %s OR key = %s;
    """, (key, key))
    post = cur.fetchone()

    if not post:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    if "comment" not in request.json or not request.json["comment"]:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "comment": "This field is required"
        })

    parent_key = None
    if "parent_key" in request.json and request.json["parent_key"]:
        cur.execute("""
            SELECT * FROM comment WHERE key = %s;
        """, (request.json["parent_key"],))
        if not cur.fetchone():
            db_close(con, cur)
            return jsonify({
                "status": 400,
                "error": "Invalid request"
            })
        parent_key = request.json["parent_key"]

    cur.execute("""
        INSERT INTO comment (
            key, created_at, user_key, post_key, comment, parent_key)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING *;
    """, (
        uuid4().hex,
        datetime.now(timezone.utc),
        user["key"],
        post["key"],
        request.json["comment"],
        parent_key
    ))
    comment = cur.fetchone()

    log(
        cur=cur,
        user_key=user["key"],
        action="created",
        entity_key=comment["key"],
        entity_type="comment",
        misc={
            "post_key": post["key"]
        }
    )

    comments = get_comments(post["key"], cur)
    db_close(con, cur)
    return comments


@bp.post("/comment/like/<key>")
def like(key):
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    cur.execute("""
        SELECT
            comment.key,
            comment.post_key,
            comment.comment,
            comment.parent_key,
            comment.likes,
            comment.dislikes,
            log.date,
            jsonb_build_object(
                'key', "user".key,
                'name', "user".name,
                'photo', "user".photo
            ) AS user

        FROM comment
        LEFT JOIN log ON
            comment.key = log.entity_key
            AND log.action = 'created'
            AND log.entity_type = 'comment'
        LEFT JOIN "user" ON comment.user_key = "user".key
        WHERE comment.key = %s;
    """, (key,))
    comment = cur.fetchone()

    if (
        not comment
        or "like" not in request.json
        or type(request.json["like"]) is not bool
    ):
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    comment["user"]["photo"] = (
        f"{request.host_url}file/{comment['user']['photo']}"
        if comment["user"]["photo"] else None
    )

    if request.json["like"]:
        if user["key"] in comment["dislikes"]:
            comment["dislikes"].remove(user["key"])
        if user["key"] in comment["likes"]:
            comment["likes"].remove(user["key"])
        else:
            comment["likes"].append(user["key"])
    else:
        if user["key"] in comment["likes"]:
            comment["likes"].remove(user["key"])
        if user["key"] in comment["dislikes"]:
            comment["dislikes"].remove(user["key"])
        else:
            comment["dislikes"].append(user["key"])

    cur.execute("""
        UPDATE comment SET likes = %s, dislikes = %s WHERE key = %s;
    """, (comment["likes"], comment["dislikes"], comment["key"]))

    log(
        cur=cur,
        user_key=user["key"],
        action='liked' if request.json['like'] else 'disliked',
        entity_key=comment["key"],
        entity_type="comment",
        misc={
            "post_key": comment["post_key"]
        }
    )

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "comment": comment

    })


@bp.delete("/comment/<key>")
def delete(key):
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    cur.execute("""
        SELECT * FROM comment WHERE key = %s AND user_key = %s;
    """, (key, user["key"]))
    comment = cur.fetchone()

    if not comment:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    cur.execute("""
        DELETE FROM comment WHERE key = %s OR parent_key = %s;
    """, (comment["key"], comment["key"]))

    log(
        cur=cur,
        user_key=user["key"],
        action="deleted",
        entity_key=comment["key"],
        entity_type="comment",
        misc={
            "post_key": comment["post_key"]
            # TODO: add children comment keys
        }
    )

    comments = get_comments(comment["post_key"], cur)
    db_close(con, cur)
    return comments
