from flask import Blueprint, jsonify, request
from ..tools import get_session
from ..postgres import db_open, db_close
from ..storage import storage
from ..log import log
from .get import post_schema

bp = Blueprint("post_photo", __name__)


@bp.put("/post/photo/<key>")
def add_photo(key):
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    if "post:edit_photo" not in user["access"]:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "unauthorized access"
        })

    cur.execute('SELECT * FROM post WHERE key = %s;', (key,))
    post = cur.fetchone()
    if 'file' not in request.files or not post:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    file = request.files["file"]
    if file.content_type not in ['image/jpeg', 'image/png']:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid file"
        })

    old_photo = None
    if post["photo"]:
        old_photo = post["photo"]
        storage("delete", post["photo"])

    file_name = storage("save", file)

    cur.execute("""
        UPDATE post
        SET photo = %s
        WHERE key = %s
        RETURNING *;
    """, (
        file_name,
        post["key"]
    ))
    post = cur.fetchone()

    log(
        cur=cur,
        user_key=user["key"],
        action="updated_photo",
        entity_type="post",
        entity_key=post["key"],
        misc={
            "from": old_photo,
            "to": file_name
        }
    )

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "post": post_schema(post)
    })


@bp.delete("/post/photo/<key>")
def delete_photo(key):
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    if "post:edit_photo" not in user["access"]:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "unauthorized access"
        })

    cur.execute('SELECT * FROM post WHERE key = %s;', (key,))
    post = cur.fetchone()
    if not post or not post["photo"]:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    storage("delete", post["photo"])

    log(
        cur=cur,
        user_key=user["key"],
        action="deleted_photo",
        entity_type="post",
        entity_key=post["key"],
        misc={"photo": post["photo"]}
    )

    if post["status"] == "active":
        log(
            cur=cur,
            user_key=user["key"],
            action="edited",
            entity_key=post["key"],
            entity_type="post",
            misc={"status": "draft"}
        )

    cur.execute("""
        UPDATE post
        SET photo = NULL, status = %s
        WHERE key = %s
        RETURNING *;
    """, (
        "draft" if post["status"] == "active" else post["status"],
        post["key"]
    ))
    post = cur.fetchone()

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "post": post_schema(post)
    })
