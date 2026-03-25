import os
import re
from uuid import uuid4

from flask import Blueprint, jsonify, request
from werkzeug.security import check_password_hash

from ..log import log
from ..postgres import db_close, db_open
from ..tools import get_session, reserved_words, user_schema
from .get import get_blocked_users

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
        action="edited profile",
        entity_type="user",
        entity_key=user["key"],
        misc=request.json
    )

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "user": user_schema(user)
    })


# TODO: user report and comment report can be unified
@bp.post("/users/<key>/report")
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
        INSERT INTO report (reporter_key, reporter_comment,
            tags, entity_key, entity_type)
        VALUES (%s, %s, %s, %s, 'user') RETURNING *;
    """, (user["key"], comment, tags, reported_user["key"]))
    report = cur.fetchone()

    log(
        cur=cur,
        user_key=user["key"],
        action="reported user",
        entity_type="user",
        entity_key=reported_user["key"],
        misc={
            "entity_type": "report",
            "entity_key": report["key"]
        }
    )

    db_close(con, cur)
    return jsonify({
        "status": 200
    })


@bp.post("/users/<key>/block")
def block(key):
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    me = session["user"]

    comment = request.json.get("comment", "").strip()

    if "user.block" not in me["access"]:
        db_close(con, cur)
        return jsonify({
            "status": 403,
            "error": "unauthorized access"
        })

    cur.execute("""SELECT * FROM "user" WHERE key = %s;""", (key,))
    user = cur.fetchone()

    cur.execute("""SELECT * FROM block WHERE user_key = %s;""", (key,))
    block = cur.fetchone()

    if (
        not user
        or user["key"] == me["key"]
        or user["status"] != "active"
        or user["email"] == os.environ["MAIL_USERNAME"]
        or block
    ):
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

    cur.execute("""
        INSERT INTO block (admin_key, user_key, comment)
        VALUES (%s, %s, %s);
    """, (me["key"], user["key"], comment))

    cur.execute("""
        DELETE FROM session WHERE user_key = %s;
    """, (user["key"],))

    log(
        cur=cur,
        user_key=me["key"],
        action="blocked user",
        entity_type="user",
        entity_key=user["key"],
        misc={"comment":  comment}
    )

    cur.execute("""
        SELECT
            "user".*,
            CASE WHEN block.user_key IS NOT NULL
                THEN true ELSE false END AS blocked
        FROM "user"
        LEFT JOIN block ON "user".key = block.user_key
        WHERE "user".key::TEXT = %s OR "user".username = %s;
    """, (key, key))
    user = cur.fetchone()

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "user": user_schema(user)
    })


@bp.delete("/users/<key>/block")
def unblock(key):
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    me = session["user"]

    comment = request.json.get("comment", "").strip()

    if "block.unblock" not in me["access"]:
        db_close(con, cur)
        return jsonify({
            "status": 403,
            "error": "unauthorized access"
        })

    cur.execute("""SELECT * FROM "user" WHERE key = %s;""", (key,))
    user = cur.fetchone()

    if (
        not user
        or user["key"] == me["key"]
        or user["status"] != "active"
        or user["email"] == os.environ["MAIL_USERNAME"]
    ):
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

    cur.execute("DELETE FROM block WHERE user_key = %s;", (user["key"],))

    log(
        cur=cur,
        user_key=me["key"],
        action="unblocked user",
        entity_type="user",
        entity_key=user["key"],
        misc={"comment":  comment}
    )

    blocks = get_blocked_users(cur).json["blocks"]

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "blocks": blocks
    })


@bp.put("/users/<key>/action")
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
        if "user.reset_name" in user["access"]:
            actions.append("name")
        else:
            error = "unauthorized access"
    if "reset_username" in _actions:
        if "user.reset_username" in user["access"]:
            actions.append("username")
        else:
            error = "unauthorized access"
    if "reset_photo" in _actions:
        if "user.reset_photo" in user["access"]:
            actions.append("photo")
        else:
            error = "unauthorized access"

    if actions == []:
        error = "Invalid request"
    if error:
        db_close(con, cur)
        return jsonify({
            "status": 403,
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
        action="reset profile",
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


@bp.put("/users/<key>/access")
def set_access(key):
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    me = session["user"]

    if "user.set_access" not in me["access"]:
        db_close(con, cur)
        return jsonify({
            "status": 403,
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
        or user["status"] != "active"
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
        action="changed access",
        entity_type="user",
        entity_key=user["key"],
        misc={"from": user["access"], "to": access}
    )

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "user": user_schema(user)
    })
