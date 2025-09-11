from flask import Blueprint, jsonify, request
from ..postgres import db_open, db_close
from ..tools import get_session, user_schema
from ..log import log
from ..storage import storage


bp = Blueprint("user_photo", __name__)


@bp.put("/user/photo")
def add_photo():
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    if 'file' not in request.files:
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
    if user["photo"]:
        old_photo = user["photo"]
        storage("delete", user["photo"])

    file_name = storage("save", file)

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
        action="updated_photo",
        entity_type="user",
        entity_key=user["key"],
        misc={
            "from": old_photo,
            "to": file_name
        }
    )

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "user": user_schema(user)
    })


@bp.delete("/user/photo")
def delete_photo():
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    if not user["photo"]:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    storage("delete", user["photo"])

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
        action="deleted_photo",
        entity_type="user",
        entity_key=user["key"],
        misc={"photo": user["photo"]}
    )

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "user": user_schema(user)
    })
