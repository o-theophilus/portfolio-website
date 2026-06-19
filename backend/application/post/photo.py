from flask import Blueprint, jsonify, request

from ..log import log
from ..storage import storage
from ..tools import rate_limit, session
from .get import post_schema

bp = Blueprint("post_photo", __name__)


@bp.put("/posts/<key>/photo")
@session(True)
@rate_limit(10, 1)
def add_photo(cur, user, key):
    if "post.edit_photo" not in user["access"]:
        return jsonify({
            "status": 403,
            "error": "unauthorized access"
        })

    cur.execute('SELECT * FROM post WHERE key = %s;', (key,))
    post = cur.fetchone()
    if 'file' not in request.files or not post:
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    file = request.files["file"]
    if file.content_type not in ['image/jpeg', 'image/png']:
        return jsonify({
            "status": 400,
            "error": "invalid file"
        })

    old_photo = None
    if post["photo"]:
        old_photo = post["photo"]
        storage.delete(post["photo"], "post")

    file_name = storage.save(file, "post")

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
        action="updated post photo",
        entity_type="post",
        entity_key=post["key"],
        misc={
            "from": old_photo,
            "to": file_name
        }
    )

    return jsonify({
        "status": 200,
        "post": post_schema(post)
    })


@bp.delete("/posts/<key>/photo")
@session(True)
@rate_limit(10, 1)
def delete_photo(cur, user, key):
    if "post.edit_photo" not in user["access"]:
        return jsonify({
            "status": 403,
            "error": "unauthorized access"
        })

    cur.execute('SELECT * FROM post WHERE key = %s;', (key,))
    post = cur.fetchone()
    if not post or not post["photo"]:
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    storage.delete(post["photo"], "post")

    log(
        cur=cur,
        user_key=user["key"],
        action="deleted post photo",
        entity_type="post",
        entity_key=post["key"],
        misc={"photo": post["photo"]}
    )

    if post["status"] == "active":
        log(
            cur=cur,
            user_key=user["key"],
            action="edited post",
            entity_type="post",
            entity_key=post["key"],
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

    return jsonify({
        "status": 200,
        "post": post_schema(post)
    })
