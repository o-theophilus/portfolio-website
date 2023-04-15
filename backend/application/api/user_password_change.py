from flask import Blueprint, jsonify, request, current_app
from .tools import token_tool, token_to_user
from .mail import send_mail
from werkzeug.security import generate_password_hash
import re
from . import db

bp = Blueprint("user_password", __name__)


@bp.post("/password")
def password():
    data = db.data()

    user = token_to_user(data)
    if not user:
        return jsonify({
            "status": 101,
            "message": "invalid token"
        })

    if (
       "email_template" not in request.json
        or not request.json["email_template"]
       ):
        return jsonify({
            "status": 401,
            "message": "invalid request"
        })

    message = request.json['email_template'].format(
        token=token_tool().dumps(user["key"]))
    send_mail(user["email"], user["name"], "Welcome!", message)

    return jsonify({
        "status": 200,
        "message": "password change email sent",
    })


@bp.post("/password/<token>")
def password_(token):
    data = db.data()

    try:
        token = token_tool().loads(
            token, max_age=current_app.config["EMAIL_CONFIRM_EXP"])
    except Exception:
        return jsonify({
            "status": 101,
            "message": "invalid token"
        })

    user = token_to_user(db)
    token_user = db.get("user", "key", token, data)
    if (
        not token_user
        or not user
        or token_user["key"] != user["key"]
        or "error_message" not in request.json
    ):
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

    if error != {}:
        return jsonify({
            "status": 201,
            "message": error
        })

    user["password"] = generate_password_hash(
        request.json["password"], method="sha256")
    db.add(user)

    return jsonify({
        "status": 200,
        "message": "successful",
    })
