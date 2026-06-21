from flask import Blueprint, request

from ..storage import storage
from ..tools import log, rate_limit, session, user_schema

bp = Blueprint("user_photo", __name__)


@bp.put("/user/photo")
@session(True)
@rate_limit(10, 1)
@log("user")
def add(cur, user):
    if 'file' not in request.files:
        return {
            "status": 422,
            "error": "Invalid request"
        }, 422

    file = request.files["file"]
    if file.content_type not in ['image/jpeg', 'image/png']:
        return {
            "status": 422,
            "error": "invalid file"
        }, 422

    old_photo = None
    if user["photo"]:
        old_photo = user["photo"]
        storage.delete(user["photo"], "user")

    file_name = storage.save(file, "user")

    cur.execute("""
        UPDATE "user"
        SET photo = %s
        WHERE key = %s
        RETURNING *;
    """, (
        file_name,
        user["key"]
    ))
    user = cur.fetchone()

    return {
        "status": 200,
        "user": user_schema(user),
        "log": {
            "misc": {
                "from": old_photo,
                "to": file_name
            }
        }
    }, 200


@bp.delete("/user/photo")
@session(True)
@rate_limit(10, 1)
@log("user")
def remove(cur, user):
    if not user["photo"]:
        return {
            "status": 422,
            "error": "Invalid request"
        }, 422

    storage.delete(user["photo"], "user")

    cur.execute("""
        UPDATE "user"
        SET photo = NULL
        WHERE key = %s
        RETURNING *;
    """, (user["key"],))
    user = cur.fetchone()

    return {
        "status": 200,
        "user": user_schema(user),
        "log": {
            "misc": {
                "photo": user["photo"]
            }
        }
    }, 200
