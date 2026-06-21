import os
import re

from flask import Blueprint, request

from ..tools import (check_code, generate_code, log, rate_limit, send_mail,
                     session, user_schema)

bp = Blueprint("user_email", __name__)


@bp.post("/user/email/1")
@session(True)
@rate_limit(5, 1)
def email_1_old_email(cur, user):
    email_template = request.json.get("email_template")
    if not email_template:
        return {
            "status": 422,
            "error": "Invalid request"
        }, 422

    send_mail(
        user["email"],
        "Email Change Confirmation - Code",
        email_template.format(
            name=user["name"],
            code=generate_code(cur, user["key"], user["email"], "change email")
        )
    )

    return {
        "status": 200
    }, 200


@bp.post("/user/email/2")
@session(True)
@rate_limit(5, 1)
def email_2_old_code(cur, user):
    error = check_code(cur, user["key"], user["email"], "code_1")
    if error:
        return {
            "status": 422,
            "code_1": error
        }, 422

    return {
        "status": 200
    }, 200


@bp.post("/user/email/3")
@session(True)
@rate_limit(5, 1)
def email_3_new_email(cur, user):
    email_template = request.json.get("email_template")
    if not email_template:
        return {
            "status": 422,
            "error": "Invalid request"
        }, 422

    email = request.json.get("email")
    error = None
    if not email:
        error = "This field is required"
    elif not re.match(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", email):
        error = "Invalid email address"
    elif user["email"] == email:
        error = "please use a different email form your current email"
    if error:
        return {
            "status": 422,
            "email": error
        }, 422

    cur.execute('SELECT * FROM "user" WHERE email = %s;', (email,))
    if cur.fetchone():
        return {
            "status": 422,
            "email": "email is already in use"
        }, 422

    send_mail(
        email,
        "Email Change Confirmation - Code",
        email_template.format(
            name=user["name"],
            code=generate_code(
                cur, user["key"], email, "change email", False)
        )
    )

    return {
        "status": 200
    }, 200


@bp.post("/user/email/4")
@session(True)
@rate_limit(5, 1)
@log("user")
def edit(cur, user):
    error = check_code(cur, user["key"], user["email"], "code_1")
    if error:
        return {
            "status": 422,
            "error": "Invalid request"
        }, 422

    email = request.json.get("email")
    if (
        not email
        or not re.match(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", email)
        or user["email"] == email
    ):
        return {
            "status": 422,
            "error": "Invalid request"
        }, 422

    cur.execute('SELECT * FROM "user" WHERE email = %s;', (email,))
    if cur.fetchone():
        return {
            "status": 422,
            "error": "Invalid request"
        }, 422

    error = check_code(cur, user["key"], email, "code_2")
    if error:
        return {
            "status": 422,
            "code_2": error
        }, 422

    if user["email"] == os.environ["MAIL_USERNAME"]:
        cur.execute("DELETE FROM code WHERE user_key = %s;", (user["key"],))
        return {
            "status": 400,
            "error": "LoL"
        }, 400

    misc = {
        "from": user['email'],
        "to": email
    }

    cur.execute("""
        UPDATE "user" SET email = %s WHERE key = %s RETURNING *;
    """, (email, user["key"]))
    user = cur.fetchone()

    cur.execute("DELETE FROM code WHERE user_key = %s;", (user["key"],))

    return {
        "status": 200,
        "user": user_schema(user),
        "log": {
            "misc": misc
        }
    }, 200
