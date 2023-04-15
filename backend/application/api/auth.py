from flask import Blueprint, jsonify, request, current_app
from . import (db, token_tool, token_to_user, user_schema,
               user_template)
from uuid import uuid4
from werkzeug.security import check_password_hash
from .mail import send_mail
import re

bp = Blueprint("auth", __name__)


@bp.post("/init")
def init():
    token = request.headers["Authorization"]
    user = token_to_user()

    if not user:
        temp = uuid4().hex
        user = db.add(user_template(temp, temp, temp))
        token = token_tool().dumps(user["key"])

    return jsonify({
        "status": 200,
        "message": "successful",
        "data": {
            "user": user_schema(user),
            "token": token
        }
    })


@bp.post("/signup")
def signup():
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
        or "error_message" not in request.json
        or user["status"] != "anonymous"
        or user["login"]
    ):
        return jsonify({
            "status": 401,
            "message": "invalid request"
        })

    error = {}

    if "name" not in request.json or not request.json["name"]:
        error["name"] = request.json["error_message"]["empty"]
    if "email" not in request.json or not request.json["email"]:
        error["email"] = request.json["error_message"]["empty"]
    elif not re.match(r"\S+@\S+\.\S+", request.json["email"]):
        error["email"] = request.json["error_message"]["email"]
    elif db.get("user", "email", request.json["email"], data):
        error["email"] = "email taken"
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

    new_user = db.add(user_template(
        request.json["name"],
        request.json["email"],
        request.json["password"]
    ))

    message = request.json['email_template'].format(
        token=token_tool().dumps(new_user["key"]),
        name=new_user["name"])
    send_mail(new_user["email"], new_user["name"], "Welcome!", message)

    return jsonify({
        "status": 200,
        "message": "successful",
        "data": {
            "user": user_schema(new_user)
        }
    })


@bp.get("/confirm/<token>")
def confirm(token):
    try:
        token = token_tool().loads(
            token, max_age=current_app.config["EMAIL_CONFIRM_EXP"])
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

    if user["status"] == "verified":
        return jsonify({
            "status": 201,
            "message": "user already confirmed",
            "data": {
                "user": user_schema(user)
            }
        })

    user["status"] = "verified"
    user = db.add(user)

    return jsonify({
        "status": 200,
        "message": "user confirmed",
        "data": {
            "user": user_schema(user)
        }
    })


@bp.post("/login")
def login():
    data = db.data()

    anon_user = token_to_user(data)
    if not anon_user:
        return jsonify({
            "status": 101,
            "message": "invalid token"
        })
    elif (anon_user["status"] != "anonymous"
          or "error_message" not in request.json
          ):
        return jsonify({
            "status": 401,
            "message": "invalid request"
        })

    error = {}
    if "email" not in request.json or not request.json["email"]:
        error["email"] = request.json["error_message"]["empty"]
    if "password" not in request.json or not request.json["password"]:
        error["password"] = request.json["error_message"]["empty"]

    if error != {}:
        return jsonify({
            "status": 201,
            "message": error
        })

    if ("email_template" not in request.json
            or not request.json["email_template"]):
        return jsonify({
            "status": 401,
            "message": "invalid request"
        })

    user = db.get("user", "email", request.json["email"], data)

    if (
        not user
        or not check_password_hash(
            user["password"],
            request.json["password"]
        )
    ):
        return jsonify({
            "status": 201,
            "message": {
                "form": "your email or password is incorrect"
            }
        })

    if user["status"] != "verified":
        message = request.json['email_template'].format(
            token=token_tool().dumps(user["key"]),
            name=user["name"])
        send_mail(user["email"], user["name"], "Welcome!", message)

        return jsonify({
            "status": 202,
            "message": "not confirmed",
            "data": {
                "user": user_schema(user)
            }
        })

    user["login"] = True
    user = db.add(user)
    db.rem(anon_user["key"])

    return jsonify({
        "status": 200,
        "message": "successful",
        "data": {
            "user": user_schema(user),
            "token": token_tool().dumps(user["key"])
        }
    })


@bp.delete("/login")
def logout():
    user = token_to_user()

    if user and user["status"] == "anonymous":
        return jsonify({
            "status": 401,
            "message": "invalid request"
        })

    user["login"] = False

    temp = uuid4().hex
    user_ = user_template(temp, temp, temp)

    db.add_many([user, user_])

    return jsonify({
        "status": 200,
        "message": "successful",
        "data": {
            "user": user_schema(user_),
            "token": token_tool().dumps(user_["key"])
        }
    })
