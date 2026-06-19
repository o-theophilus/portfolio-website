import os
import re

from flask import Blueprint, jsonify, request

from ..log import log
from ..tools import (check_code, generate_code, rate_limit, send_mail, session,
                     user_schema)

bp = Blueprint("user_email", __name__)


@bp.post("/user/email/1")
@session(True)
@rate_limit(5, 1)
def email_1_old_email(cur, user):
    email_template = request.json.get("email_template")
    if not email_template:
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    send_mail(
        user["email"],
        "Email Change Confirmation - Code",
        email_template.format(
            name=user["name"],
            code=generate_code(cur, user["key"], user["email"], "change email")
        )
    )

    return jsonify({
        "status": 200
    })


@bp.post("/user/email/2")
@session(True)
@rate_limit(5, 1)
def email_2_old_code(cur, user):
    error = check_code(cur, user["key"], user["email"], "code_1")
    if error:
        return jsonify({
            "status": 400,
            "code_1": error
        })

    return jsonify({
        "status": 200
    })


@bp.post("/user/email/3")
@session(True)
@rate_limit(5, 1)
def email_3_new_email(cur, user):
    email_template = request.json.get("email_template")
    if not email_template:
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    email = request.json.get("email")
    error = None
    if not email:
        error = "This field is required"
    elif not re.match(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", email):
        error = "Invalid email address"
    if error:
        return jsonify({
            "status": 400,
            "email": error
        })

    if user["email"] == email:
        return jsonify({
            "status": 400,
            "email": "please use a different email form your current email"
        })

    cur.execute('SELECT * FROM "user" WHERE email = %s;',
                (email,))
    exist = cur.fetchone()
    if exist:
        return jsonify({
            "status": 400,
            "email": "email is already in use"
        })

    send_mail(
        email,
        "Email Change Confirmation - Code",
        email_template.format(
            name=user["name"],
            code=generate_code(
                cur, user["key"], email, "change email", False)
        )
    )

    return jsonify({
        "status": 200
    })


@bp.post("/user/email/4")
@session(True)
@rate_limit(5, 1)
def email_4_new_code(cur, user):
    error = check_code(cur, user["key"], user["email"], "code_1")
    if error:
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    email = request.json.get("email")
    if not email or not re.match(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", email):
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    if user["email"] == email:
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    cur.execute('SELECT * FROM "user" WHERE email = %s;', (email,))
    exist = cur.fetchone()
    if exist:
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    error = check_code(cur, user["key"], email, "code_2")
    if error:
        return jsonify({
            "status": 400,
            "code_2": error
        })

    if user["email"] == os.environ["MAIL_USERNAME"]:
        cur.execute("DELETE FROM code WHERE user_key = %s;", (user["key"],))
        return jsonify({
            "status": 400,
            "error": "LoL"
        })

    log(
        cur=cur,
        user_key=user["key"],
        action="changed email",
        entity_type="user",
        entity_key=user["key"],
        misc={
            "from": user['email'],
            "to": email
        }
    )

    cur.execute("""
        UPDATE "user" SET email = %s WHERE key = %s RETURNING *;
    """, (email, user["key"]))
    user = cur.fetchone()

    cur.execute("DELETE FROM code WHERE user_key = %s;", (user["key"],))

    return jsonify({
        "status": 200,
        "user": user_schema(user)
    })
