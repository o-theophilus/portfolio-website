import os
import re
from uuid import uuid4

from flask import Blueprint, jsonify, request
from werkzeug.security import check_password_hash, generate_password_hash

from ..log import log
from ..post.get import get_tags
from ..postgres import db_close, db_open
from ..storage import storage
from ..tools import (access_pass, check_code, generate_code, get_session,
                     rate_limit, reserved_words, send_mail, session,
                     user_schema)

bp = Blueprint("auth", __name__)


def new_user(cur):
    key = uuid4().hex
    cur.execute("""
        INSERT INTO "user" (name, username, email, password)
        VALUES (%s, %s, %s, %s)
        RETURNING *;
    """, (
        f"user {key[-8:]}",
        f"user_{key[:8]}",
        uuid4().hex,
        generate_password_hash(uuid4().hex, method="scrypt")))
    return cur.fetchone()


def new_token(cur, user_key, login=False, remember=False):
    cur.execute("""
        INSERT INTO session (user_key, login, remember) VALUES (%s, %s, %s)
        RETURNING *;
    """, (user_key, login, remember))

    return cur.fetchone()["key"]


@bp.post("/init")
def init():
    con, cur = db_open()

    session = get_session(cur)

    if session["status"] == 200:
        user = session["user"]
        token = request.headers.get("Authorization")
        login = session["login"]

    else:
        user = new_user(cur)
        token = new_token(cur, user["key"])
        login = False

        log(
            cur=cur,
            user_key=user["key"],
            action="created",
            entity_type="user",
            entity_key=user["key"]
        )

    tags = get_tags(cur)

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "user": user_schema(user),
        "token": token,
        "login": login,
        "tags": tags
    })


@bp.post("/signup")
@session(False)
@rate_limit(10, 1)
def signup(cur, user):
    name = ' '.join(request.json.get("name", "").strip().split())
    email = request.json.get("email", "").strip()
    password = request.json.get("password")
    confirm_password = request.json.get("confirm_password")
    email_template = request.json.get("email_template")

    if session["login"] or not email_template:
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    error = {}

    if not name:
        error["name"] = "This field is required"
    elif len(name) > 100:
        error["name"] = "This field cannot exceed 100 characters"

    email_user = None
    if not email:
        error["email"] = "This field is required"
    elif not re.match(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", email):
        error["email"] = "Invalid email address"
    elif len(email) > 255:
        error["email"] = "This field cannot exceed 255 characters"
    else:
        cur.execute('SELECT * FROM "user" WHERE email = %s;', (email,))
        email_user = cur.fetchone()
        if email_user and email_user["status"] != "signedup":
            error["email"] = "Email already in use"

    if not password:
        error["password"] = "This field is required"
    elif (
        not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[^\s]+$", password)
        or len(password) not in range(8, 19)
    ):
        error["password"] = """Password must include at least 1 lowercase
        letter, 1 uppercase letter, 1 number and must contain 8 - 18
        characters"""

    if not confirm_password:
        error["confirm_password"] = "This field is required"
    elif password and confirm_password != password:
        error["confirm_password"] = """Password and confirm password does not
        match"""

    if error:
        return jsonify({
            "status": 400,
            **error
        })

    if email_user:
        user = email_user
    elif user["status"] != "anonymous":
        user = new_user(cur)

    username = re.sub(
        '-+', '-', re.sub('[^a-zA-Z0-9]', '-', name.lower()))[:20]
    cur.execute(
        """SELECT * FROM "user" WHERE email != %s AND username = %s;""",
        (email, username))
    if cur.fetchone() or username in reserved_words:
        username = f"{username[:11]}-{str(uuid4().hex)[:8]}"

    cur.execute("""
        UPDATE "user"
        SET name = %s, username = %s, email = %s,
            password = %s, status = 'signedup'
        WHERE key = %s
        RETURNING *;
    """, (
        name,
        username,
        email,
        generate_password_hash(password, method="scrypt"),
        user["key"]
    ))
    user = cur.fetchone()

    log(
        cur=cur,
        user_key=user["key"],
        action="signedup",
        entity_type="user",
        entity_key=user["key"]
    )

    send_mail(
        user["email"],
        "Welcome to my portfolio website! Complete your signup with this Code",
        email_template.format(
            name=user["name"],
            code=generate_code(cur, user["key"], user["email"], "signup")
        )
    )

    return jsonify({
        "status": 200
    })


@bp.post("/confirm")
@session(False)
@rate_limit(10, 1)
def confirm(cur, _user):
    email = request.json.get("email")

    error = None
    if not email or not re.match(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", email):
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    cur.execute('SELECT * FROM "user" WHERE email = %s;', (email,))
    user = cur.fetchone()
    if not user or user["status"] != 'signedup':
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    error = check_code(cur, user["key"], user["email"])
    if error:
        return jsonify({
            "status": 400,
            "error": error
        })

    cur.execute("""
        UPDATE "user"
        SET status = 'active', access = %s
        WHERE key = %s;
    """, (
        [f"{x}.{y[0]}" for x in access_pass for y in access_pass[x]] if (
            user["email"] == os.environ["MAIL_USERNAME"]
        ) else user["access"],
        user["key"]
    ))

    log(
        cur=cur,
        user_key=user["key"],
        action="activated account",
        entity_type="user",
        entity_key=user["key"]
    )

    cur.execute("DELETE FROM code WHERE user_key = %s;", (user["key"],))

    return jsonify({
        "status": 200
    })


@bp.post("/login")
@session(False)
@rate_limit(10, 1)
def login(cur, user):
    email_template = request.json.get("email_template")
    if session["login"] or not email_template:
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    email = request.json.get("email")
    password = request.json.get("password")
    remember = request.json.get("remember", False)

    error = {}
    if not email:
        error["email"] = "This field is required"
    if not password:
        error["password"] = "This field is required"
    if error:
        return jsonify({
            "status": 400,
            **error
        })

    user2 = None
    if user["email"] == email:
        user2 = user
    else:
        cur.execute("""
            SELECT * FROM "user" WHERE email = %s OR username = %s;
        """, (email, email))
        user2 = cur.fetchone()

    if (
        not user2
        or user2["status"] not in ['signedup', 'active']
        or not check_password_hash(user2["password"], password)
    ):
        return jsonify({
            "status": 400,
            "error": "your email or password is incorrect"
        })

    cur.execute("SELECT * FROM block WHERE user_key = %s;", (user2["key"],))
    if cur.fetchone():
        return jsonify({
            "status": 400,
            "error": "account blocked"
        })

    if user2["status"] == "signedup":
        send_mail(
            user2["email"],
            "Welcome to my portfolio website! \
            Complete your signup with this Code",
            email_template.format(
                name=user2["name"],
                code=generate_code(
                    cur, user2["key"], user2["email"], "login")
            )
        )
        return jsonify({
            "status": 400,
            "error": "not active"
        })

    cur.execute("""
        DELETE FROM session WHERE user_key = %s;
        DELETE FROM "user" WHERE key = %s AND status = 'anonymous';
    """, (user["key"], user["key"]))

    token = new_token(cur, user2["key"], True, remember)

    log(
        cur=cur,
        user_key=user2["key"],
        action="logged in",
        entity_type="user",
        entity_key=user2["key"],
        misc={
            "key": user["key"],
            "name": user["name"]
        }
    )
    log(
        cur=cur,
        user_key=user["key"],
        action="logged out",
        entity_type="user",
        entity_key=user["key"],
        misc={
            "key": user2["key"],
            "name": user2["name"]
        }
    )

    return jsonify({
        "status": 200,
        "token": token
    })


@bp.delete("/logout")
@session(True)
@rate_limit(10, 1)
def logout(cur, user):
    user2 = new_user(cur)

    cur.execute("""
        DELETE FROM session WHERE user_key = %s;
    """, (user["key"],))

    token = new_token(cur, user2["key"])

    log(
        cur=cur,
        user_key=user["key"],
        action="logged out",
        entity_type="user",
        entity_key=user["key"],
        misc={
            "key": user2["key"],
            "name": user2["name"]
        }
    )
    log(
        cur=cur,
        user_key=user2["key"],
        action="created",
        entity_type="user",
        entity_key=user2["key"],
        misc={
            "from": user["key"],
            "name": user["name"]
        }
    )

    return jsonify({
        "status": 200,
        "user": user_schema(user2),
        "token": token
    })


@bp.delete("/deactivate")
@session(True)
@rate_limit(10, 1)
def deactivate(cur, user):
    password = request.json.get("password")
    note = request.json.get("note")
    email_template = request.json.get("email_template")

    if not email_template:
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    error = {}
    if not password:
        error["password"] = "This field is required"
    elif not check_password_hash(user["password"], password):
        error["password"] = "Incorrect password"
    if error:
        return jsonify({
            "status": 400,
            **error
        })

    cur.execute("""
        UPDATE post
        SET author_key = (SELECT key FROM "user" WHERE email = %s)
        WHERE author_key = %s;
    """, (os.environ["MAIL_USERNAME"], user["key"]))
    cur.execute("""
        UPDATE block
        SET admin_key = (SELECT key FROM "user" WHERE email = %s)
        WHERE admin_key = %s;
    """, (os.environ["MAIL_USERNAME"], user["key"]))
    cur.execute("""DELETE FROM "user" WHERE key = %s;""", (user["key"],))

    storage.delete(user["photo"], "user")
    user2 = new_user(cur)
    token = new_token(cur, user2["key"])

    log(
        cur=cur,
        user_key=user["key"],
        action="deleted account",
        entity_type="user",
        entity_key=user["key"],
        misc={"note": note} if note else {}
    )
    log(
        cur=cur,
        user_key=user2["key"],
        action="created",
        entity_type="user",
        entity_key=user2["key"],
        misc={
            "key": user["key"],
            "name": user["name"]
        }
    )

    send_mail(
        user["email"],
        "You've Successfully Deleted Your Account",
        email_template.format(name=user["name"])
    )

    return jsonify({
        "status": 200,
        "user": user_schema(user2),
        "token": token
    })
