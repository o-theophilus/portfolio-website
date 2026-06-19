from flask import Blueprint, jsonify, request

from ..log import log
from ..storage import storage
from ..tools import rate_limit, session, user_schema

bp = Blueprint("user_photo", __name__)


@bp.put("/user/photo")
@session(True)
@rate_limit(10, 1)
def add_photo(cur, user):
    if 'file' not in request.files:
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

    log(
        cur=cur,
        user_key=user["key"],
        action="updated profile photo",
        entity_type="user",
        entity_key=user["key"],
        misc={
            "from": old_photo,
            "to": file_name
        }
    )

    return jsonify({
        "status": 200,
        "user": user_schema(user)
    })


@bp.delete("/user/photo")
@session(True)
@rate_limit(10, 1)
def delete_photo(cur, user):
    if not user["photo"]:
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    storage.delete(user["photo"], "user")

    cur.execute("""
        UPDATE "user"
        SET photo = NULL
        WHERE key = %s
        RETURNING *;
    """, (user["key"],))
    user = cur.fetchone()

    log(
        cur=cur,
        user_key=user["key"],
        action="deleted profile photo",
        entity_type="user",
        entity_key=user["key"],
        misc={"photo": user["photo"]}
    )

    return jsonify({
        "status": 200,
        "user": user_schema(user)
    })
