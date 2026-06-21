import os
import re

from flask import Blueprint, request
from werkzeug.security import check_password_hash, generate_password_hash

from ..tools import (access_pass, check_code, generate_code, log, rate_limit,
                     send_mail, session)

bp = Blueprint("password_forgot", __name__)


@bp.post("/forgot/1")
@session(False)
@rate_limit(10, 1)
@log("user")
def forgot_1_email(cur, _user):
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
    if error:
        return {
            "status": 422,
            "email": error
        }, 422

    cur.execute("""
        SELECT * FROM "user" WHERE email = %s
    ;""", (email,))
    user = cur.fetchone()
    if not user or user["status"] not in ['signedup', 'active']:
        return {
            "status": 404,
            "email": "there is no user registered with this email"
        }, 404

    send_mail(
        user["email"],
        "Password Change Confirmation - Code",
        email_template.format(
            name=user["name"],
            code=generate_code(
                cur, user["key"], user["email"], "forgot password")
        )
    )

    return {
        "status": 200
    }, 200


@bp.post("/forgot/2")
@session(False)
@rate_limit(10, 1)
@log("user")
def forgot_2_code(cur, _user):
    email = request.json.get("email")
    if not email or not re.match(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", email):
        return {
            "status": 422,
            "error": "Invalid request"
        }, 422

    cur.execute("""
        SELECT * FROM "user"
        WHERE email = %s AND status IN ('signedup', 'active');
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
            "code": error
        }, 422

    return {
        "status": 200
    }, 200


@bp.post("/forgot/3")
@session(False)
@rate_limit(10, 1)
@log("user")
def edit(cur, _user):
    email = request.json.get("email")

    if not email or not re.match(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", email):
        return {
            "status": 422,
            "error": "Invalid request"
        }, 422

    cur.execute("""
        SELECT * FROM "user"
        WHERE email = %s AND status IN ('signedup', 'active');
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
            "error": "Invalid request"
        }, 422

    password = request.json.get("password")
    confirm_password = request.json.get("confirm_password")

    error = {}
    if not password:
        error["password"] = "This field is required"
    elif (
        not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[^\s]+$", password)
        or len(password) not in range(8, 19)
    ):
        error["password"] = """Password must include at least 1 lowercase
        letter, 1 uppercase letter, 1 number and must contain 8 - 18
        characters"""
    elif check_password_hash(user["password"], password):
        error["password"
              ] = "New password should be different from old password"
    if not confirm_password:
        error["confirm_password"] = "This field is required"
    elif password and confirm_password != password:
        error["confirm_password"] = """Password and confirm_password password
         does not match"""
    if error:
        return {
            "status": 422,
            **error
        }, 422

    cur.execute("""
        UPDATE "user" SET password = %s WHERE key = %s;
    """, (
        generate_password_hash(password, method="scrypt"),
        user["key"]
    ))

    log = {}
    if user["status"] != "active":
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

        log = {
            "misc": {
                "action": "activated"
            }
        }

    cur.execute("DELETE FROM code WHERE user_key = %s;", (user["key"],))

    return {
        "status": 200,
        "log": log
    }, 200
