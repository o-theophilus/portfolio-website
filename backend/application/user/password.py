from flask import Blueprint, jsonify, request
import re
from werkzeug.security import generate_password_hash, check_password_hash
from ..postgres import db_open, db_close
from ..tools import get_session, send_mail, generate_code, check_code
from ..log import log


bp = Blueprint("user_password", __name__)


@bp.post("/user/password/1")
def password_1_email():
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    email_template = request.json.get("email_template")
    if not email_template:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    send_mail(
        user["email"],
        "Password Change Confirmation - Code",
        email_template.format(
            name=user["name"],
            code=generate_code(
                cur, user["key"], user["email"], "change password")
        )
    )

    db_close(con, cur)
    return jsonify({
        "status": 200
    })


@bp.post("/user/password/2")
def password_2_code():
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

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


@bp.post("/user/password/3")
def password_3_password():
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

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
        entity_type="user",
        entity_key=user["key"]
    )

    cur.execute("DELETE FROM code WHERE user_key = %s;", (user["key"],))

    db_close(con, cur)
    return jsonify({
        "status": 200
    })
