from flask import Blueprint, jsonify, request
import re
from werkzeug.security import generate_password_hash, check_password_hash
from ..tools import send_mail, generate_code, check_code
from ..postgres import db_open, db_close
from ..log import log

bp = Blueprint("auth_forgot", __name__)


@bp.post("/forgot/1")
def forgot_1_email():
    con, cur = db_open()

    email_template = request.json.get("email_template")
    if not email_template:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    email = request.json.get("email")

    error = None
    if email:
        error = "This field is required"
    elif not re.match(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", email):
        error = "Invalid email address"
    if error:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "email": error
        })

    cur.execute("""
        SELECT * FROM "user" WHERE email = %s
    ;""", (email,))
    user = cur.fetchone()
    if not user or user["status"] not in ['signedup', 'confirmed']:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "email": "there is no user registered with this email"
        })

    send_mail(
        user["email"],
        "Password Change Confirmation - Code",
        email_template.format(
            name=user["name"],
            code=generate_code(
                cur, user["key"], user["email"], "forgot password")
        )
    )

    db_close(con, cur)
    return jsonify({
        "status": 200
    })


@bp.post("/forgot/2")
def forgot_2_code():
    con, cur = db_open()

    email = request.json.get("email")
    if not email or not re.match(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", email):
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    cur.execute("""SELECT * FROM "user" WHERE email = %s;""", (email,))
    user = cur.fetchone()
    if not user or user["status"] not in ['signedup', 'confirmed']:
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
            "code": error
        })

    db_close(con, cur)
    return jsonify({
        "status": 200
    })


@bp.post("/forgot/3")
def forgot_3_password():
    con, cur = db_open()

    email = request.json.get("email")

    if not email or not re.match(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", email):
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    cur.execute("""
        SELECT * FROM "user" WHERE email = %s
    ;""", (email,))
    user = cur.fetchone()
    if not user or user["status"] not in ['signedup', 'confirmed']:
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
            "error": "Invalid request"
        })

    password = request.json.get("password")
    confirm_password = request.json.get("confirm_password")

    error = {}
    if not password:
        error["password"] = "This field is required"
    elif (
        not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]+$", password)
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
    if error != {}:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            **error
        })

    cur.execute("""
        UPDATE "user" SET password = %s WHERE key = %s;
    """, (
        generate_password_hash(password, method="scrypt"),
        user["key"]
    ))
    log(
        cur=cur,
        user_key=user["key"],
        action="changed_password",
        entity_key="auth",
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
            entity_key="auth",
            entity_type="account",
        )

    cur.execute("DELETE FROM code WHERE user_key = %s;", (user["key"],))

    db_close(con, cur)
    return jsonify({
        "status": 200
    })
