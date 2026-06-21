from flask import Blueprint, request

from ..storage import storage
from ..tools import log, rate_limit, session
from .get import post_schema

bp = Blueprint("post_photo", __name__)


@bp.put("/posts/<key>/photo")
@session(True)
@rate_limit(10, 1)
@log("post")
def add_photo(cur, user, key):
    if "post.edit_photo" not in user["access"]:
        return {
            "status": 403,
            "error": "unauthorized access"
        }, 403

    cur.execute('SELECT * FROM post WHERE key = %s;', (key,))
    post = cur.fetchone()
    if 'file' not in request.files or not post:
        return {
            "status": 400,
            "error": "Invalid request"
        }, 400

    file = request.files["file"]
    if file.content_type not in ['image/jpeg', 'image/png']:
        return {
            "status": 422,
            "error": "invalid file"
        }, 422

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

    return {
        "status": 200,
        "post": post_schema(post),
        "log": {
            "entity_key": post["key"],
            "misc": {
                "from": old_photo,
                "to": file_name
            }
        }
    }, 200


@bp.delete("/posts/<key>/photo")
@session(True)
@rate_limit(10, 1)
@log("post")
def delete_photo(cur, user, key):
    if "post.edit_photo" not in user["access"]:
        return {
            "status": 403,
            "error": "unauthorized access"
        }, 403

    cur.execute('SELECT * FROM post WHERE key = %s;', (key,))
    post = cur.fetchone()
    if not post or not post["photo"]:
        return {
            "status": 400,
            "error": "Invalid request"
        }, 400

    storage.delete(post["photo"], "post")

    misc = {
        "photo": post["photo"],
    }
    if post["status"] == "active":
        misc["status"] = "draft"

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

    return {
        "status": 200,
        "post": post_schema(post),
        "log": {
            "entity_key": post["key"],
            "misc": misc
        }
    }, 200
