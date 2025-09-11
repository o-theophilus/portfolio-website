from flask import Blueprint, jsonify, request
import os
from werkzeug.security import check_password_hash
from ..postgres import db_open, db_close
from ..log import log
from ..tools import get_session, user_schema


bp = Blueprint("access", __name__)


access_pass = {
    "user": [
        ['view', 1],
        ['reset_name', 2],
        ['reset_username', 2],
        ['reset_photo', 2],
        ['block', 2],
        ['set_access', 3]
    ],
    "admin": [
        ['manage_files', 3]
    ],
    "post": [
        ['add', 2],
        ['edit_photo', 2],
        ['edit_title', 2],
        ['edit_date', 2],
        ['edit_description', 2],
        ['edit_content', 2],
        ['edit_files', 2],
        ['edit_tags', 2],
        ['edit_status', 2],
        ['edit_author', 2],
        ['edit_highlight', 2]
    ],
    "report": [
        ['view', 1],
        ['resolve', 3]
    ],
    "block": [
        ['view', 1],
        ['block', 3],
        ['unblock', 3]
    ],
    "log": [
        ['view', 1]
    ]
}


@bp.get("/admin/access")
@bp.get("/admin/access/<search>")
def get_access(search=None):
    _all = [f"{x}:{y[0]}" for x in access_pass for y in access_pass[x]]
    if search:
        _all = [x for x in _all if x.find(search) != -1]

    return jsonify({
        "status": 200,
        "access": _all
    })


@bp.put("/admin/access/<key>")
def set_access(key):
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    me = session["user"]

    if "user:set_access" not in me["access"]:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "unauthorized access"
        })

    cur.execute('SELECT * FROM "user" WHERE key = %s;', (key,))
    user = cur.fetchone()

    access = request.json.get("access")

    if (
        not user
        or me["key"] == user["key"]
        or not access
        or type(access) is not list
        or user["email"] == os.environ["MAIL_USERNAME"]
        or user["status"] != "confirmed"
    ):
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    password = request.json.get("password")

    error = None
    if not password:
        error = "This field is required"
    elif not check_password_hash(me["password"], password):
        error = "incorrect password"
    if error:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "password": error
        })

    cur.execute("""
        UPDATE "user" SET access = %s WHERE key = %s;
    """, (access, user["key"]))

    log(
        cur=cur,
        user_key=me["key"],
        action="changed_access",
        entity_key=user["key"],
        entity_type="admin",
        misc={"from": user["access"], "to": access}
    )

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "user": user_schema(user)
    })
