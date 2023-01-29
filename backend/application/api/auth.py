from flask import Blueprint, jsonify, request, current_app
from .schema import user_schema, user as _user
from . import db
from . import token_tool, token_to_user
from uuid import uuid4
from werkzeug.security import check_password_hash, generate_password_hash

bp = Blueprint("auth", __name__)


@bp.post("/init")
def init():
    data = db.data()
    omni(data)

    token = request.headers["Authorization"]
    user = token_to_user(data)

    if not user:
        temp = uuid4().hex
        _user["key"] = temp
        _user["name"] = temp
        _user["email"] = temp
        _user["password"] = temp
        user = db.add(_user)
        token = token_tool().dumps(user["key"])

    return jsonify({
        "status": 200,
        "message": "successful",
        "data": {
            "user": user_schema(user),
            "token": token
        }
    })


def omni(data):
    email = current_app.config["ADMIN_EMAIL"]
    user = db.get("user", "email", email, data)
    if not user:
        temp = uuid4().hex
        _user["key"] = temp
        _user["name"] = "Meji Admin"
        _user["email"] = email
        _user["password"] = generate_password_hash(
            current_app.config["ADMIN_PASSWORD"],
            method="sha256"
        )
        _user["roles"] = ["admin", "dashboard", "omni"]
        _user["status"] = "verified"

        db.add(_user)


@bp.post("/login")
def login():
    data = db.data()

    anon_user = token_to_user(data)
    if not anon_user:
        return jsonify({
            "status": 101,
            "message": "invalid token"
        })

    error = {}
    if "email" not in request.json or not request.json["email"]:
        error["email"] = "This field is required"
    if "password" not in request.json or not request.json["password"]:
        error["password"] = "This field is required"

    if error != {}:
        return jsonify({
            "status": 201,
            "message": error
        })

    user = db.get("user", "email", request.json["email"], data)

    if (
        not user or not check_password_hash(
            user["password"],
            request.json["password"]
        )
    ):
        return jsonify({
            "status": 201,
            "message": "Your email or password is incorrect"
        })

    # if anon_user["status"] == "anon":
    #     db.rem(anon_user["key"])

    user["login"] = True
    db.add(user)

    return jsonify({
        "status": 200,
        "message": "successful",
        "data": {
            "user": user_schema(user),
            "token": token_tool().dumps(user["key"])
        }
    })


# @bp.post("/user")
# def signup():
#     db = get_db()

#     user = token_to_user(db)
#     if not user:
#         return jsonify({
#             "status": 101,
#             "message": "invalid token"
#         })

#     if (
#         "mail_content" not in request.json
#         or not request.json["mail_content"]
#     ):
#         return jsonify({
#             "status": 401,
#             "message": "invalid request"
#         })

#     if user["login"]:
#         return jsonify({
#             "status": 401,
#             "message": "invalid request"
#         })

#     error = {}

#     if "name" not in request.json or not request.json["name"]:
#         error["name"] = "this field is required"

#     if "email" not in request.json or not request.json["email"]:
#         error["email"] = "this field is required"
#     elif not re.match(r"\S+@\S+\.\S+", request.json["email"]):
#         error["email"] = "Please enter a valid email"

#     elif db_get(db, "user", "email", request.json["email"]):
#         error["email"] = "email taken"

#     if "password" not in request.json or not request.json["password"]:
#         error["password"] = "this field is required"
#     elif (
#         not re.search("[a-z]", request.json["password"]) or
#         not re.search("[A-Z]", request.json["password"]) or
#         not re.search("[0-9]", request.json["password"]) or
#         len(request.json["password"]) not in range(8, 19)
#     ):
#         error["password"] = """Password must include at least 1 lowercase
#         letter, 1 uppercase letter, 1 number and must contain 8 - 18
#         characters"""

#     if "confirm" not in request.json or not request.json["confirm"]:
#         error["confirm"] = "This field is required"
#     elif (
#             request.json["password"]
#             and "password" not in error
#             and request.json["confirm"] != request.json["password"]
#     ):
#         error["confirm"] = 'Password and confirm password does not match'

#     if error != {}:
#         return jsonify({
#             "status": 201,
#             "message": error
#         })

#     if user["status"] != "anon":
#         user = _user
#         user["key"] = uuid4().hex

#     user["name"] = request.json["name"]
#     user["email"] = request.json["email"]
#     user["password"] = generate_password_hash(
#         request.json["password"], method="sha256")
#     user["status"] = "not_confirm"
#     user["date_u"] = now(),
#     user["v"]: uuid4().hex

#     user = db_add(user)
#     token = token_tool().dumps(user["key"])
#     mail = request.json['mail_content'].format(token=token)
#     send_mail(user["email"], "Welcome!", mail)

#     return jsonify({
#         "status": 200,
#         "message": "successful",
#         "data": {
#             "user": user_schema(user, db)
#         }
#     })


# @bp.delete("/logout")
# def logout():
#     db = get_db()

#     user = token_to_user(db)
#     if user:
#         user["login"] = False

#     user = db_add(_user)

#     return jsonify({
#         "status": 200,
#         "message": "successful",
#         "data": {
#             "user": user_schema(user, db),
#             "token": token_tool().dumps(user["key"])
#         }
#     })
