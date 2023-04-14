from flask import Blueprint, jsonify, request, current_app
from .mail import send_mail
from werkzeug.security import generate_password_hash, check_password_hash
import re
from . import db, token_tool, user_schema

bp = Blueprint("user_password_forgot", __name__)


@bp.post("/password_forgot1")
def password_forgot1():

    if (
       "email_template" not in request.json
        or not request.json["email_template"]
       ):
        return jsonify({
            "status": 401,
            "message": "invalid request"
        })

    error = {}
    if "email" not in request.json or not request.json["email"]:
        error["email"] = 'cannot be empty'
    elif not re.match(r"\S+@\S+\.\S+", request.json["email"]):
        error["email"] = 'invalid email'

    if error != {}:
        return jsonify({
            "status": 201,
            "message": error
        })

    user = db.get("user", "email", request.json["email"])
    if not user:
        return jsonify({
            "status": 201,
            "message": {"email": "no user registered with this email"}
        })

    message = request.json['email_template'].format(
        token=token_tool().dumps(user["key"]),
        name=user["name"]
    )
    send_mail(user["email"], "Welcome!", message)

    return jsonify({
        "status": 200,
        "message": "password change email sent",
    })


@bp.post("/password_forgot2")
def password_forgot2():
    if "token" not in request.json or not request.json["token"]:
        return jsonify({
            "status": 401,
            "message": "invalid request"
        })

    try:
        token = token_tool().loads(
            request.json["token"],
            max_age=current_app.config["EMAIL_CONFIRM_EXP"])
    except Exception:
        return jsonify({
            "status": 101,
            "message": "invalid token"
        })

    user = db.get("user", "key", token)
    if not user:
        return jsonify({
            "status": 101,
            "message": "invalid token"
        })

    error = {}

    if "password" not in request.json or not request.json["password"]:
        error["password"] = request.json["error_message"]["empty"]
    elif (
        not re.search("[a-z]", request.json["password"]) or
        not re.search("[A-Z]", request.json["password"]) or
        not re.search("[0-9]", request.json["password"]) or
        len(request.json["password"]) not in range(8, 19)
    ):
        error["password"] = request.json["error_message"]["password"]
    elif ("confirm_password" not in request.json
          or not request.json["confirm_password"]):
        error["confirm_password"] = request.json["error_message"]["empty"]
    elif request.json["confirm_password"] != request.json["password"]:
        error["confirm_password"] = request.json["error_message"][
            "confirm_password"]
    elif check_password_hash(user["password"], request.json["password"]):
        error["password"] = "must be different from old password"

    if error != {}:
        return jsonify({
            "status": 201,
            "message": error
        })

    user["password"] = generate_password_hash(
        request.json["password"], method="sha256")
    user = db.add(user)

    return jsonify({
        "status": 200,
        "message": "successful",
        "data": {
            "user": user_schema(user)
        }
    })
