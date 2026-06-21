import os
import re
from uuid import uuid4

from flask import Blueprint, request
from werkzeug.security import check_password_hash, generate_password_hash

from ..post.get import get_tags
from ..storage import storage
from ..tools import (access_pass, check_code, generate_code, log, rate_limit,
                     reserved_words, send_mail, session, user_schema)

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
@session(False)
def init(cur, _session):

    if _session["status"] == 200:
        user = _session["user"]
        token = request.headers.get("Authorization")
        login = user.pop("login")

    else:
        user = new_user(cur)
        token = new_token(cur, user["key"])
        login = False

        cur.execute("""
            INSERT INTO log (
                user_key, action, entity_type
            ) VALUES (%s, %s, %s);
        """, (user["key"], "auth.init", "user"))

    tags = get_tags(cur)

    return {
        "status": 200,
        "user": user_schema(user),
        "token": token,
        "login": login,
        "tags": tags,
    }, 200


@bp.post("/signup")
@session(False)
@rate_limit(10, 1)
@log("user")
def signup(cur, user):
    if user["login"]:
        return {
            "status": 401,
            "error": "Invalid request"
        }, 401

    name = ' '.join(request.json.get("name", "").strip().split())
    email = request.json.get("email", "").strip()
    password = request.json.get("password")
    confirm_password = request.json.get("confirm_password")
    email_template = request.json.get("email_template")

    if not email_template:
        return {
            "status": 422,
            "error": "Invalid request"
        }, 422

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
        return {
            "status": 422,
            **error
        }, 422

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

    send_mail(
        user["email"],
        "Welcome to my portfolio website! Complete your signup with this Code",
        email_template.format(
            name=user["name"],
            code=generate_code(cur, user["key"], user["email"], "signup")
        )
    )

    return {
        "status": 200
    }, 200


@bp.post("/confirm")
@session(False)
@rate_limit(10, 1)
@log("user")
def confirm(cur, _user):
    email = request.json.get("email")
    if not email or not re.match(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", email):
        return {
            "status": 422,
            "error": "Invalid request"
        }, 422

    cur.execute("""
        SELECT * FROM "user"
        WHERE email = %s AND status = 'signedup';
    """, (email,))
    user = cur.fetchone()
    if not user:
        return {
            "status": 404,
            "error": "Invalid request"
        }, 404

    error = check_code(cur, user["key"], user["email"])
    if error:
        return {
            "status": 422,
            "error": error
        }, 422

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

    cur.execute("DELETE FROM code WHERE user_key = %s;", (user["key"],))

    return {
        "status": 200
    }, 200


@bp.post("/login")
@session(False)
@rate_limit(10, 1)
@log("user")
def login(cur, user):
    if user["login"]:
        return {
            "status": 401,
            "error": "Invalid request"
        }, 401

    email_template = request.json.get("email_template")
    email = request.json.get("email")
    password = request.json.get("password")
    remember = request.json.get("remember", False)

    if not email_template:
        return {
            "status": 422,
            "error": "Invalid request"
        }, 422

    error = {}
    if not email:
        error["email"] = "This field is required"
    if not password:
        error["password"] = "This field is required"
    if error:
        return {
            "status": 422,
            **error
        }, 422

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
        return {
            "status": 401,
            "error": "your email or password is incorrect"
        }, 401

    cur.execute("SELECT * FROM block WHERE user_key = %s;", (user2["key"],))
    if cur.fetchone():
        return {
            "status": 401,
            "error": "account blocked"
        }, 401

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
        return {
            "status": 401,
            "error": "not active"
        }, 401

    cur.execute("""
        DELETE FROM session WHERE user_key = %s;
        DELETE FROM "user" WHERE key = %s AND status = 'anonymous';
    """, (user["key"], user["key"]))

    token = new_token(cur, user2["key"], True, remember)

    return {
        "status": 200,
        "token": token,
        "log": {
            "misc": {
                "from_key": user["key"],
                "from_name": user["name"]
            }
        }
    }, 200


@bp.delete("/logout")
@session(True)
@rate_limit(10, 1)
@log("user")
def logout(cur, user):
    cur.execute("""
        DELETE FROM session WHERE user_key = %s;
    """, (user["key"],))

    user2 = new_user(cur)
    token = new_token(cur, user2["key"])

    return {
        "status": 200,
        "user": user_schema(user2),
        "token": token,
        "log": {
            "misc": {
                "to_key": user2["key"],
                "to_name": user2["name"]
            }
        }
    }, 200


@bp.delete("/deactivate")
@session(True)
@rate_limit(10, 1)
@log("user")
def deactivate(cur, user):
    password = request.json.get("password")
    note = request.json.get("note")
    email_template = request.json.get("email_template")

    if not email_template:
        return {
            "status": 422,
            "error": "Invalid request"
        }, 422

    error = {}
    if not password:
        error["password"] = "This field is required"
    elif not check_password_hash(user["password"], password):
        error["password"] = "Incorrect password"
    if error:
        return {
            "status": 401,
            **error
        }, 401

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

    send_mail(
        user["email"],
        "You've Successfully Deleted Your Account",
        email_template.format(name=user["name"])
    )

    return {
        "status": 200,
        "user": user_schema(user2),
        "token": token,
        "log": {
            "misc": {
                "note": note,
                "to_key": user2["key"],
                "to_name": user2["name"]
            }
        }
    }, 200
