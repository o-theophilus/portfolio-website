import re

from flask import Blueprint, jsonify, request

from ..log import log
from ..postgres import db_close, db_open
from ..tools import get_session, reserved_words, user_schema

bp = Blueprint("user", __name__)


@bp.post("/user/theme")
def theme():
    con, cur = db_open()

    session = get_session(cur)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    theme = request.json.get("theme")
    if theme not in ["light", "dark", "system"]:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    log(
        cur=cur,
        user_key=user["key"],
        action="changed theme",
        entity_type="user",
        entity_key=user["key"],
        misc={
            "from": user["theme"],
            "to": theme
        }
    )

    cur.execute("""
        UPDATE "user" SET theme = %s WHERE key = %s RETURNING *
    ;""", (theme, user["key"]))
    user = cur.fetchone()

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "user": user_schema(user)
    })


@bp.put("/user")
def edit_user():
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    error = {}

    name = user["name"]
    username = user["username"]
    phone = user["phone"]

    if "name" in request.json:
        name = ' '.join(request.json.get("name", "").strip().split())
        if not name:
            error['name'] = "This field is required"
        elif name == user["name"]:
            error['name'] = "No changes were made"
        elif len(name) > 100:
            error["name"] = "This field cannot exceed 100 characters"

    if "username" in request.json:
        username = request.json.get("username", "").strip().lower()
        if not username:
            error["username"] = "This field is required"
        elif (
                not re.match(r"^[A-Za-z][A-Za-z0-9-]*$", username)
                or len(username) > 20
        ):
            error["username"] = """'Username can only contain letters,
            numbers, or dash, must start with a letter,
            and be at most 20 characters"""
        elif username == user["username"]:
            error['username'] = "No changes were made"
        elif username in reserved_words:
            error["username"] = "Username is not allowed"
        else:
            cur.execute(
                'SELECT * FROM "user" WHERE username = %s AND key != %s;',
                (username, user["key"]))
            if cur.fetchone():
                error["username"] = "Username already in use"

    if "phone" in request.json:
        phone = request.json.get("phone", "").replace(" ", "")
        if phone == user["phone"]:
            error['phone'] = "No changes were made"
        elif len(phone) > 20:
            error["phone"] = "This field cannot exceed 20 characters"

    if error:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            **error
        })

    cur.execute("""
        UPDATE "user"
        SET name = %s, username = %s, phone = %s WHERE key = %s
        RETURNING *;
    """, (name, username, phone, user["key"]))
    user = cur.fetchone()

    log(
        cur=cur,
        user_key=user["key"],
        action="edited",
        entity_type="user",
        entity_key=user["key"],
        misc=request.json
    )

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "user": user_schema(user)
    })


@bp.post("/report/user/<key>")
def report(key):
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    comment = request.json.get("comment", "").strip()
    tags = request.json.get("tags")

    if type(tags) is not list:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    error = {}
    if not comment:
        error["comment"] = "This field is required"
    elif len(comment) > 500:
        error["comment"] = "This field cannot exceed 500 characters"
    if error:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            **error
        })

    cur.execute("""SELECT * FROM "user" WHERE key = %s;""", (key,))
    reported_user = cur.fetchone()
    if not reported_user:
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    cur.execute("""
        INSERT INTO report (reporter_key, reported_user_key,
            reporter_comment, tags)
        VALUES (%s, %s, %s, %s) RETURNING *;
    """, (user["key"], reported_user["key"], comment, tags))
    report = cur.fetchone()

    log(
        cur=cur,
        user_key=user["key"],
        action="reported user",
        entity_key=report["key"],
        entity_type="report",
        misc={"key": reported_user["key"]}
    )

    db_close(con, cur)
    return jsonify({
        "status": 200
    })
