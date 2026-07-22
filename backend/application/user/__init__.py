import os
import re
from uuid import uuid4

from flask import Blueprint, request
from werkzeug.security import check_password_hash

from ..tools import log, rate_limit, reserved_words, session, user_schema

bp = Blueprint("user", __name__)


@bp.post("/user/theme")
@session(True)
@rate_limit(20, 1)
@log("user")
def theme(cur, user):
    theme = request.json.get("theme")
    if theme not in ["light", "dark", "system"]:
        return {
            "error": "Invalid request"
        }, 422

    misc = {
        "from": user["theme"],
        "to": theme
    }

    cur.execute("""
        UPDATE "user" SET theme = %s WHERE key = %s RETURNING *
    ;""", (theme, user["key"]))
    user = cur.fetchone()

    return {
        "user": user_schema(user),
        "log": {
            "misc": misc
        }
    }, 200


@bp.put("/user")
@session(True)
@rate_limit(20, 1)
def edit(cur, user):
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
        return {
            **error
        }, 400

    cur.execute("""
        UPDATE "user"
        SET name = %s, username = %s, phone = %s WHERE key = %s
        RETURNING *;
    """, (name, username, phone, user["key"]))
    user = cur.fetchone()

    return {
        "user": user_schema(user),
        "log": {
            "misc": request.json
        }
    }, 200


@bp.put("/users/<key>/action")
@session(True)
@rate_limit(10, 1)
@log("user")
def reset(cur, user, key):
    cur.execute("""SELECT * FROM "user" WHERE key = %s;""", (key,))
    user2 = cur.fetchone()
    if (
        not user2 or user["key"] == user2["key"]
        or user2["email"] == os.environ["MAIL_USERNAME"]
    ):
        return {
            "error": "Invalid request"
        }, 404

    _actions = request.json.get("actions")
    comment = request.json.get("comment")

    error = {}
    if not _actions or type(_actions) is not list or _actions == []:
        error["actions"] = "select action"
    if not comment:
        error["comment"] = "This field is required"
    if error:
        return {
            **error
        }, 422

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
        return {
            "error": error
        }, 403

    _key = uuid4().hex
    cur.execute("""
        UPDATE "user" SET name = %s, username = %s, photo = %s
        WHERE key = %s RETURNING *;
    """, (
        f"user {_key[-8:]}" if "name" in actions else user2["name"],
        f"user_{_key[:8]}" if "username" in actions else user2["username"],
        None if "photo" in actions else user2["photo"],
        user2["key"]
    ))
    user2 = cur.fetchone()

    return {
        "user": user_schema(user2),
        "log": {
            "entity_key": user2["key"],
            "misc": {
                "field(s)": ", ".join(actions),
                "comment": comment
            }
        }
    }, 200


@bp.put("/users/<key>/access")
@session(True)
@rate_limit(10, 1)
@log("user")
def edit_access(cur, user, key):
    if "user.edit_access" not in user["access"]:
        return {
            "error": "unauthorized access"
        }, 403

    cur.execute('SELECT * FROM "user" WHERE key = %s;', (key,))
    user2 = cur.fetchone()
    if (
        not user2
        or user2["key"] == user["key"]
        or user2["email"] == os.environ["MAIL_USERNAME"]
        or user2["status"] != "active"
    ):
        return {
            "error": "Invalid request"
        }, 404

    access = request.json.get("access")
    password = request.json.get("password")

    if not access or type(access) is not list:
        return {
            "error": "Invalid request"
        }, 422

    error = None
    if not password:
        error = "This field is required"
    elif not check_password_hash(user["password"], password):
        error = "incorrect password"
    if error:
        return {
            "password": error
        }, 422

    cur.execute("""
        UPDATE "user" SET access = %s WHERE key = %s;
    """, (access, user2["key"]))

    return {
        "user": user_schema(user2),
        "log": {
            "entity_key": user2["key"],
            "misc": {
                "from": user2["access"],
                "to": access
            }
        }
    }, 200
