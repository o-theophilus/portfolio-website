from flask import Blueprint, jsonify, request
from uuid import uuid4
import os
from ..postgres import db_open, db_close
from ..log import log
from ..tools import get_session, user_schema


bp = Blueprint("action", __name__)


@bp.put("/admin/action/<key>")
def action(key):
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    cur.execute("""SELECT * FROM "user" WHERE key = %s;""", (key,))
    e_user = cur.fetchone()
    if (
        not e_user or user["key"] == e_user["key"]
        or e_user["email"] == os.environ["MAIL_USERNAME"]
    ):
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    _actions = request.json.get("actions")
    note = request.json.get("note")

    error = {}
    if not _actions or type(_actions) is not list or _actions == []:
        error["actions"] = "select action"
    if not note:
        error["note"] = "This field is required"
    if error != {}:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            **error
        })

    actions = []
    error = None
    if "reset_name" in _actions:
        if "user:reset_name" in user["access"]:
            actions.append("name")
        else:
            error = "unauthorized access"
    if "reset_username" in _actions:
        if "user:reset_username" in user["access"]:
            actions.append("username")
        else:
            error = "unauthorized access"
    if "reset_photo" in _actions:
        if "user:reset_photo" in user["access"]:
            actions.append("photo")
        else:
            error = "unauthorized access"

    if actions == []:
        error = "Invalid request"
    if error:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": error
        })

    _key = uuid4().hex
    cur.execute("""
        UPDATE "user" SET name = %s, username = %s, photo = %s
        WHERE key = %s RETURNING *;
    """, (
        f"user {_key[-8:]}" if "name" in actions else e_user["name"],
        f"user_{_key[:8]}" if "username" in actions else e_user["username"],
        None if "photo" in actions else e_user["photo"],
        e_user["key"]
    ))
    e_user = cur.fetchone()

    log(
        cur=cur,
        user_key=user["key"],
        action="reset",
        entity_type="user",
        entity_key=e_user["key"],
        misc={
            "field(s)": ", ".join(actions),
            "note": note
        }
    )

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "user": user_schema(e_user)
    })
