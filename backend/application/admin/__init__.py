import os
from uuid import uuid4

from flask import Blueprint, jsonify, request
from werkzeug.security import check_password_hash

from ..log import log
from ..postgres import db_close, db_open
from ..tools import get_session, user_schema

bp = Blueprint("admin", __name__)


@bp.put("/admin/action/<key>")
def perform_action(key):
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
    comment = request.json.get("comment")

    error = {}
    if not _actions or type(_actions) is not list or _actions == []:
        error["actions"] = "select action"
    if not comment:
        error["comment"] = "This field is required"
    if error:
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
            "comment": comment
        }
    )

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "user": user_schema(e_user)
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
