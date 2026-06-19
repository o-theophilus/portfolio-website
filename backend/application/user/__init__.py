import os
import re
from uuid import uuid4

from flask import Blueprint, jsonify, request
from werkzeug.security import check_password_hash

from ..log import log
from ..tools import rate_limit, reserved_words, session, user_schema

bp = Blueprint("user", __name__)


@bp.post("/user/theme")
@session(True)
@rate_limit(20, 1)
def theme(cur, user):
    theme = request.json.get("theme")
    if theme not in ["light", "dark", "system"]:
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

    return jsonify({
        "status": 200,
        "user": user_schema(user)
    })


@bp.put("/user")
@session(True)
@rate_limit(20, 1)
def edit_user(cur, user):
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

    return jsonify({
        "status": 200,
        "user": user_schema(user)
    })


# TODO: user report and comment report can be unified
@bp.post("/users/<key>/report")
@session(True)
@rate_limit(20, 1)
def report(cur, user, key):
    comment = request.json.get("comment", "").strip()
    tags = request.json.get("tags")

    if type(tags) is not list:
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
        return jsonify({
            "status": 400,
            **error
        })

    cur.execute("""SELECT * FROM "user" WHERE key = %s;""", (key,))
    user2 = cur.fetchone()
    if not user2:
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    cur.execute("""
        INSERT INTO report (reporter_key, reporter_comment,
            tags, reported_key)
        VALUES (%s, %s, %s, %s) RETURNING *;
    """, (user["key"], comment, tags, user2["key"]))
    report = cur.fetchone()

    log(
        cur=cur,
        user_key=user["key"],
        action="reported user",
        entity_type="user",
        entity_key=user2["key"],
        misc={
            "report_key": report["key"]
        }
    )

    return jsonify({
        "status": 200
    })


@bp.post("/users/<key>/block")
@session(True)
@rate_limit(20, 1)
def block(cur, user, key):
    comment = request.json.get("comment", "").strip()

    if "user.block" not in user["access"]:
        return jsonify({
            "status": 403,
            "error": "unauthorized access"
        })

    cur.execute("""SELECT * FROM "user" WHERE key = %s;""", (key,))
    user2 = cur.fetchone()

    cur.execute("""SELECT * FROM block WHERE user_key = %s;""", (key,))
    block = cur.fetchone()

    if (
        not user2
        or user2["key"] == user["key"]
        or user2["status"] != "active"
        or user2["email"] == os.environ["MAIL_USERNAME"]
        or block
    ):
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
        return jsonify({
            "status": 400,
            **error
        })

    cur.execute("""
        INSERT INTO block (admin_key, user_key, comment)
        VALUES (%s, %s, %s);
    """, (user["key"], user2["key"], comment))

    cur.execute("""
        DELETE FROM session WHERE user_key = %s;
    """, (user2["key"],))

    log(
        cur=cur,
        user_key=user["key"],
        action="blocked user",
        entity_type="user",
        entity_key=user2["key"],
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
    user2 = cur.fetchone()

    return jsonify({
        "status": 200,
        "user": user_schema(user2)
    })


@bp.delete("/users/<key>/block")
@session(True)
@rate_limit(20, 1)
def unblock(cur, user, key):
    comment = request.json.get("comment", "").strip()

    if "block.unblock" not in user["access"]:
        return jsonify({
            "status": 403,
            "error": "unauthorized access"
        })

    cur.execute("""SELECT * FROM "user" WHERE key = %s;""", (key,))
    user2 = cur.fetchone()

    if (
        not user2
        or user2["key"] == user["key"]
        or user2["status"] != "active"
        or user2["email"] == os.environ["MAIL_USERNAME"]
    ):
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
        return jsonify({
            "status": 400,
            **error
        })

    cur.execute("DELETE FROM block WHERE user_key = %s;", (user2["key"],))

    log(
        cur=cur,
        user_key=user["key"],
        action="unblocked user",
        entity_type="user",
        entity_key=user2["key"],
        misc={"comment":  comment}
    )

    return jsonify({
        "status": 200,
    })


@bp.put("/users/<key>/action")
@session(True)
@rate_limit(10, 1)
def perform_action(cur, user, key):
    cur.execute("""SELECT * FROM "user" WHERE key = %s;""", (key,))
    user2 = cur.fetchone()
    if (
        not user2 or user["key"] == user2["key"]
        or user2["email"] == os.environ["MAIL_USERNAME"]
    ):
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
        return jsonify({
            "status": 403,
            "error": error
        })

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

    log(
        cur=cur,
        user_key=user["key"],
        action="reset profile",
        entity_type="user",
        entity_key=user2["key"],
        misc={
            "field(s)": ", ".join(actions),
            "comment": comment
        }
    )

    return jsonify({
        "status": 200,
        "user": user_schema(user2)
    })


@bp.put("/users/<key>/access")
@session(True)
@rate_limit(10, 1)
def set_access(cur, user, key):
    if "user.set_access" not in user["access"]:
        return jsonify({
            "status": 403,
            "error": "unauthorized access"
        })

    cur.execute('SELECT * FROM "user" WHERE key = %s;', (key,))
    user2 = cur.fetchone()

    access = request.json.get("access")

    if (
        not user2
        or user["key"] == user2["key"]
        or not access
        or type(access) is not list
        or user2["email"] == os.environ["MAIL_USERNAME"]
        or user2["status"] != "active"
    ):
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    password = request.json.get("password")

    error = None
    if not password:
        error = "This field is required"
    elif not check_password_hash(user["password"], password):
        error = "incorrect password"
    if error:
        return jsonify({
            "status": 400,
            "password": error
        })

    cur.execute("""
        UPDATE "user" SET access = %s WHERE key = %s;
    """, (access, user2["key"]))

    log(
        cur=cur,
        user_key=user["key"],
        action="changed access",
        entity_type="user",
        entity_key=user2["key"],
        misc={"from": user2["access"], "to": access}
    )

    return jsonify({
        "status": 200,
        "user": user_schema(user2)
    })
