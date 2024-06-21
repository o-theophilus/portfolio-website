from flask import Blueprint, jsonify, request
from .tools import (
    token_tool, token_to_user, user_schema, send_mail,
    generate_otp, check_otp)
from uuid import uuid4
import re
from werkzeug.security import generate_password_hash, check_password_hash
from .postgres import db_open, db_close
from .log import log
from .admin import get_highlight

bp = Blueprint("account", __name__)

max_age = 3600


@bp.post("/init")
def init():
    con, cur = db_open()

    token = request.headers["Authorization"]
    user = token_to_user(cur)

    if not user or user["status"] == "confirmed" and not user["login"]:
        key = uuid4().hex
        cur.execute("""
                INSERT INTO "user" (key, name, email, password)
                VALUES (%s, %s, %s, %s)
                RETURNING *;
            """, (
            key,
            f"user_{key[-4:]}",
            uuid4().hex,
            generate_password_hash(uuid4().hex, method="scrypt"))
        )
        user = cur.fetchone()

        log(
            cur=cur,
            user_key=user["key"],
            action="created",
            entity_type="account",
        )

        token = token_tool().dumps(user["key"])

    cur.execute("SELECT * FROM save WHERE save.user_key = %s;", (user["key"],))
    saves = cur.fetchall()

    posts = get_highlight(cur)

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "user": user_schema(
            user,
            saves=[x['item_key'] for x in saves],
        ),
        "token": token,
        "posts": posts
    })


@bp.post("/signup")
def signup():
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    if (
        user["login"]
        or "email_template" not in request.json
        or not request.json["email_template"]
    ):
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    error = {}

    if "name" not in request.json or not request.json["name"]:
        error["name"] = "cannot be empty"

    if "email" not in request.json or not request.json["email"]:
        error["email"] = "cannot be empty"
    elif not re.match(r"\S+@\S+\.\S+", request.json["email"]):
        error["email"] = "Please enter a valid email"
    else:
        cur.execute('SELECT * FROM "user" WHERE email = %s;', (
            request.json["email"],))
        if cur.fetchone():
            error["email"] = "email taken"

    if "password" not in request.json or not request.json["password"]:
        error["password"] = "cannot be empty"
    elif (
        not re.search("[a-z]", request.json["password"])
        or not re.search("[A-Z]", request.json["password"])
        or not re.search("[0-9]", request.json["password"])
        or len(request.json["password"]) not in range(8, 19)
    ):
        error["password"] = """password must include at least 1 lowercase
        letter, 1 uppercase letter, 1 number and must contain 8 - 18
        characters"""

    if "confirm_password" not in request.json or not request.json[
            "confirm_password"]:
        error["confirm_password"] = "cannot be empty"
    elif (
            request.json["password"]
            and request.json["confirm_password"] != request.json["password"]
    ):
        error["confirm_password"] = """password and confirm password does not
        match"""

    if error != {}:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            **error
        })

    if user["status"] != "anonymous":
        key = uuid4().hex
        cur.execute("""
            INSERT INTO "user" (key, name, email, password)
            VALUES (%s, %s, %s, %s)
            RETURNING *;
        """, (
            key,
            f"user_{key[-4:]}",
            uuid4().hex,
            generate_password_hash(uuid4().hex, method="scrypt")))

    cur.execute("""
        UPDATE "user"
        SET name = %s, email = %s, password = %s, status = 'signedup'
        WHERE key = %s
        RETURNING *;
    """, (
        request.json["name"],
        request.json["email"],
        generate_password_hash(request.json["password"], method="scrypt"),
        user["key"]
    ))
    user = cur.fetchone()

    log(
        cur=cur,
        user_key=user["key"],
        action="signedup",
        entity_type="account",
    )

    send_mail(
        user["email"],
        "Welcome to my portfolio website! Complete your signup with this OTP",
        request.json['email_template'].format(
            name=user["name"],
            otp=generate_otp(cur, user["key"], user["email"], "signup")
        )
    )

    db_close(con, cur)
    return jsonify({
        "status": 200
    })


@bp.post("/confirm")
def confirm():
    con, cur = db_open()

    error = None
    if (
        "email" not in request.json
        or not request.json["email"]
        or not re.match(r"\S+@\S+\.\S+", request.json["email"])
    ):
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    cur.execute("""
        SELECT * FROM "user" WHERE email = %s
    ;""", (request.json["email"],))
    user = cur.fetchone()
    if not user or user["status"] != 'signedup':
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    error = check_otp(cur, user["key"], user["email"])
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
        entity_type="account",
    )

    cur.execute("DELETE FROM otp WHERE user_key = %s;", (user["key"],))

    db_close(con, cur)
    return jsonify({
        "status": 200
    })


@bp.post("/login")
def login():
    con, cur = db_open()

    out_user = token_to_user(cur)
    if not out_user:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    if (
        out_user["login"]
        or "email_template" not in request.json
        or not request.json["email_template"]
    ):
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    error = {}
    if "email" not in request.json or not request.json["email"]:
        error["email"] = "cannot be empty"
    if "password" not in request.json or not request.json["password"]:
        error["password"] = "cannot be empty"

    if error != {}:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            **error
        })

    in_user = None
    if out_user["email"] == request.json["email"]:
        in_user = out_user
    else:
        cur.execute('SELECT * FROM "user" WHERE email = %s;',
                    (request.json["email"],))
        in_user = cur.fetchone()

    if (
        not in_user
        or in_user["status"] not in ['signedup', 'confirmed']
        or not check_password_hash(
            in_user["password"], request.json["password"])
    ):
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "your email or password is incorrect"
        })

    if in_user["status"] != "confirmed":
        send_mail(
            in_user["email"],
            "Welcome to my portfolio website! \
            Complete your signup with this OTP",
            request.json['email_template'].format(
                name=in_user["name"],
                otp=generate_otp(
                    cur, in_user["key"], in_user["email"], "login")
            )
        )
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "not confirmed"
        })

    cur.execute("""
        UPDATE "user" SET login = %s
        WHERE key = %s RETURNING *;""", (
        True, in_user["key"]
    ))
    cur.execute("""
        UPDATE "user"
        SET status = 'deleted', login = %s
        WHERE key = %s AND status = 'anonymous'
        RETURNING *;""", (
        False, out_user["key"]
    ))

    log(
        cur=cur,
        user_key=in_user["key"],
        action="logged_in",
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
        entity_type="account",
        misc={
            "to": in_user["key"],
            "name": in_user["name"]
        }
    )

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "token": token_tool().dumps(in_user["key"])
    })


@bp.delete("/logout")
def logout():
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    cur.execute("""
        UPDATE "user" SET login = %s
        WHERE key = %s RETURNING *;""", (
        False, user["key"]
    ))

    key = uuid4().hex
    cur.execute("""
        INSERT INTO "user" (
            key, name, email, password, setting_theme
        ) VALUES (%s, %s, %s, %s, %s) RETURNING *;
    """, (
        key, f"user_{key[-4:]}", uuid4().hex,
        generate_password_hash(uuid4().hex, method="scrypt"),
        user["setting_theme"]
    ))
    anon_user = cur.fetchone()

    log(
        cur=cur,
        user_key=user["key"],
        action="logged_out",
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
        "token": token_tool().dumps(anon_user["key"])
    })


@bp.post("/forgot/1")
def forgot_1_email():
    con, cur = db_open()

    if (
        "email_template" not in request.json
        or not request.json["email_template"]
    ):
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    error = None
    if "email" not in request.json or not request.json["email"]:
        error = "cannot be empty"
    elif not re.match(r"\S+@\S+\.\S+", request.json["email"]):
        error = "invalid email"
    if error:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "email": error
        })

    cur.execute("""
        SELECT * FROM "user" WHERE email = %s
    ;""", (request.json["email"],))
    user = cur.fetchone()
    if not user or user["status"] not in ['signedup', 'confirmed']:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "email": "there is no user registered with this email"
        })

    send_mail(
        user["email"],
        "Password Change Confirmation - One-Time Password (OTP)",
        request.json['email_template'].format(
            name=user["name"],
            otp=generate_otp(
                cur, user["key"], user["email"], "forgot password")
        )
    )

    db_close(con, cur)
    return jsonify({
        "status": 200
    })


@bp.post("/forgot/2")
def forgot_2_otp():
    con, cur = db_open()

    if (
        "email" not in request.json or not request.json["email"]
        or not re.match(r"\S+@\S+\.\S+", request.json["email"])
    ):
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    cur.execute("""
        SELECT * FROM "user" WHERE email = %s
    ;""", (request.json["email"],))
    user = cur.fetchone()
    if not user or user["status"] not in ['signedup', 'confirmed']:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    error = check_otp(cur, user["key"], user["email"])
    if error:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "otp": error
        })

    db_close(con, cur)
    return jsonify({
        "status": 200
    })


@bp.post("/forgot/3")
def forgot_3_password():
    con, cur = db_open()

    if (
        "email" not in request.json or not request.json["email"]
        or not re.match(r"\S+@\S+\.\S+", request.json["email"])
    ):
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    cur.execute("""
        SELECT * FROM "user" WHERE email = %s
    ;""", (request.json["email"],))
    user = cur.fetchone()
    if not user or user["status"] not in ['signedup', 'confirmed']:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    error = check_otp(cur, user["key"], user["email"])
    if error:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    error = {}
    if "password" not in request.json or not request.json["password"]:
        error["password"] = "cannot be empty"
    elif (
        not re.search("[a-z]", request.json["password"])
        or not re.search("[A-Z]", request.json["password"])
        or not re.search("[0-9]", request.json["password"])
        or len(request.json["password"]) not in range(8, 19)
    ):
        error["password"] = """Password must include at least 1 lowercase
        letter, 1 uppercase letter, 1 number and must contain 8 - 18
        characters"""
    elif check_password_hash(user["password"], request.json["password"]):
        error["password"
              ] = "New password should be different from old password"

    if (
        "confirm_password" not in request.json
        or not request.json["confirm_password"]
    ):
        error["confirm_password"] = "cannot be empty"
    elif (
            request.json["password"]
            and request.json["confirm_password"] != request.json["password"]
    ):
        error["confirm_password"] = """Password and confirm_password password
         does not match"""
    if error != {}:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            **error
        })

    cur.execute("""
        UPDATE "user" SET password = %s WHERE key = %s;
    """, (
        generate_password_hash(request.json["password"], method="scrypt"),
        user["key"]
    ))
    log(
        cur=cur,
        user_key=user["key"],
        action="changed_password",
        entity_type="account"
    )

    if user["status"] != "confirmed":
        cur.execute("""
            UPDATE "user" SET status = 'confirmed' WHERE key = %s;
        """, (user["key"],))
        log(
            cur=cur,
            user_key=user["key"],
            action="confirmed_email",
            entity_type="account",
        )

    cur.execute("DELETE FROM otp WHERE user_key = %s;", (user["key"],))

    db_close(con, cur)
    return jsonify({
        "status": 200
    })
