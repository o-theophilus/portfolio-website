from flask import Blueprint, jsonify, request
from uuid import uuid4
import re
import os
from werkzeug.security import generate_password_hash, check_password_hash
from ..tools import (
    get_session, user_schema, send_mail, generate_code,
    reserved_words, check_code)
from ..postgres import db_open, db_close
from ..log import log
from ..storage import storage

bp = Blueprint("auth", __name__)


def anon(cur):
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


def delete_user(cur, user):
    cur.execute("""
        DELETE FROM report WHERE user_key = %s OR entity_key = %s;
    """, (user["key"], user["key"]))

    cur.execute("""
        UPDATE block
        SET admin_key = (SELECT key FROM "user" WHERE email = %s)
        WHERE admin_key = %s
    ;""", (os.environ["MAIL_USERNAME"], user["key"]))

    cur.execute("""
        DELETE FROM "like" WHERE user_key = %s;
    """, (user["key"],))

    cur.execute("""
        DELETE FROM code WHERE user_key = %s;
    """, (user["key"],))

    cur.execute("""
        DELETE FROM session WHERE user_key = %s;
    """, (user["key"],))

    cur.execute("""
        WITH RECURSIVE to_delete AS (
            SELECT key
            FROM comment
            WHERE user_key = %s

            UNION ALL

            SELECT c.key
            FROM comment c
            INNER JOIN to_delete td ON c.parent_key = td.key
        )
        DELETE FROM comment
        WHERE key IN (SELECT key FROM to_delete);
    """, (user["key"],))

    cur.execute("""
        UPDATE post
        SET author_key = (SELECT key FROM "user" WHERE email = %s)
        WHERE key = %s
    ;""", (os.environ["MAIL_USERNAME"], user["key"]))

    cur.execute("""
        DELETE FROM "user" WHERE key = %s;
    """, (user["key"],))
    storage("delete", user["photo"])


@bp.post("/init")
def init():
    con, cur = db_open()

    session = get_session(cur)

    if session["status"] == 200:
        user = session["user"]
        token = request.headers.get("Authorization")
        login = session["login"]

    else:
        user = anon(cur)
        token = new_token(cur, user["key"])
        login = False

        log(
            cur=cur,
            user_key=user["key"],
            action="created",
            entity_key="auth",
            entity_type="account",
        )

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "user": user_schema(user),
        "token": token,
        "login": login,
    })


@bp.post("/signup")
def signup():
    con, cur = db_open()

    session = get_session(cur)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    name = ' '.join(request.json.get("name", "").strip().split())
    email = request.json.get("email", "").strip()
    password = request.json.get("password")
    confirm_password = request.json.get("confirm_password")
    email_template = request.json.get("email_template")

    if session["login"] or not email_template:
        db_close(con, cur)
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
        if email_user and email_user["status"] == "confirmed":
            error["email"] = "Email already in use"

    if not password:
        error["password"] = "This field is required"
    elif (
        not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]+$", password)
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

    if error != {}:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            **error
        })

    if email_user:
        user = email_user
    elif user["status"] != "anonymous":
        user = anon(cur)

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
        entity_key="auth",
        entity_type="account",
    )

    send_mail(
        user["email"],
        "Welcome to my portfolio website! Complete your signup with this Code",
        email_template.format(
            name=user["name"],
            code=generate_code(cur, user["key"], user["email"], "signup")
        )
    )

    db_close(con, cur)
    return jsonify({
        "status": 200
    })


@bp.post("/confirm")
def confirm():
    con, cur = db_open()

    email = request.json.get("email")

    error = None
    if not email or not re.match(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", email):
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    cur.execute('SELECT * FROM "user" WHERE email = %s;', (email,))
    user = cur.fetchone()
    if not user or user["status"] != 'signedup':
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    error = check_code(cur, user["key"], user["email"])
    if error:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": error
        })

    cur.execute("""
        UPDATE "user" SET status = 'confirmed' WHERE key = %s;
    """, (user["key"],))

    log(
        cur=cur,
        user_key=user["key"],
        action="confirmed_email",
        entity_key="auth",
        entity_type="account",
    )

    cur.execute("DELETE FROM code WHERE user_key = %s;", (user["key"],))

    db_close(con, cur)
    return jsonify({
        "status": 200
    })


@bp.post("/login")
def login():
    con, cur = db_open()

    session = get_session(cur)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    out_user = session["user"]

    email_template = request.json.get("email_template")
    if session["login"] or not email_template:
        db_close(con, cur)
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
    if error != {}:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            **error
        })

    in_user = None
    if out_user["email"] == email:
        in_user = out_user
    else:
        cur.execute("""
            SELECT * FROM "user" WHERE email = %s OR username = %s;
        """, (email, email))
        in_user = cur.fetchone()

    if (
        not in_user
        or in_user["status"] not in ['signedup', 'confirmed']
        or not check_password_hash(in_user["password"], password)
    ):
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "your email or password is incorrect"
        })

    cur.execute("SELECT * FROM block WHERE user_key = %s;", (in_user["key"],))
    if cur.fetchone():
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "account blocked"
        })

    if in_user["status"] == "signedup":
        send_mail(
            in_user["email"],
            "Welcome to my portfolio website! \
            Complete your signup with this Code",
            email_template.format(
                name=in_user["name"],
                code=generate_code(
                    cur, in_user["key"], in_user["email"], "login")
            )
        )
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "not confirmed"
        })

    cur.execute("""
        DELETE FROM session WHERE user_key = %s;
        DELETE FROM "user" WHERE key = %s AND status = 'anonymous';
    """, (out_user["key"], out_user["key"]))

    token = new_token(cur, in_user["key"], True, remember)

    log(
        cur=cur,
        user_key=in_user["key"],
        action="logged_in",
        entity_key="auth",
        entity_type="account",
        misc={
            "from": out_user["key"],
            "name": out_user["name"]
        }
    )
    log(
        cur=cur,
        user_key=out_user["key"],
        action="logged_out",
        entity_key="auth",
        entity_type="account",
        misc={
            "to": in_user["key"],
            "name": in_user["name"]
        }
    )

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "token": token
    })


@bp.delete("/logout")
def logout():
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]
    anon_user = anon(cur)

    cur.execute("""
        DELETE FROM session WHERE user_key = %s;
    """, (user["key"],))

    token = new_token(cur, anon_user["key"])

    log(
        cur=cur,
        user_key=user["key"],
        action="logged_out",
        entity_key="auth",
        entity_type="account",
        misc={
            "to": anon_user["key"],
            "name": anon_user["name"]
        }
    )
    log(
        cur=cur,
        user_key=anon_user["key"],
        action="created",
        entity_key="auth",
        entity_type="account",
        misc={
            "from": user["key"],
            "name": user["name"]
        }
    )

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "user": user_schema(anon_user),
        "token": token
    })


@bp.delete("/deactivate")
def deactivate():
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    password = request.json.get("password")
    note = request.json.get("note")
    email_template = request.json.get("email_template")

    if not email_template:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    error = {}
    if not password:
        error["password"] = "This field is required"
    elif not check_password_hash(user["password"], password):
        error["password"] = "Incorrect password"
    if error != {}:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            **error
        })

    delete_user(cur, user)
    anon_user = anon(cur)
    token = new_token(cur, anon_user["key"])

    log(
        cur=cur,
        user_key=user["key"],
        action="deleted_account",
        entity_key="auth",
        entity_type="account",
        misc={"note": note} if note else {}
    )
    log(
        cur=cur,
        user_key=anon_user["key"],
        action="created",
        entity_key="auth",
        entity_type="account",
        misc={
            "from": user["key"],
            "name": user["name"]
        }
    )

    send_mail(
        user["email"],
        "You've Successfully Deleted Your Account",
        email_template.format(name=user["name"])
    )

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "user": user_schema(anon_user),
        "token": token
    })
