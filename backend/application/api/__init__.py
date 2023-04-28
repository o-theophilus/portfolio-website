from flask import Blueprint, jsonify, current_app, request
from itsdangerous import URLSafeTimedSerializer
from . import db
import re
from .mail import send_mail
from .schema import user_template


bp = Blueprint("api", __name__)


def token_tool():
    return URLSafeTimedSerializer(
        current_app.config["SECRET_KEY"],
        current_app.config["SECURITY_PASSWORD_SALT"]
    )


def token_to_user(data=None):
    if (
        "Authorization" not in request.headers or
        not request.headers["Authorization"]
    ):
        return None

    token = request.headers["Authorization"]
    try:
        token = token_tool().loads(token)
    except Exception:
        return None

    return db.get("user", "key", token, data)


reserved_words = [
    "admin", "omni", "user", "users", "store", "stores", "item",
    "items"]  # property, cart, save


def create_default_admin():
    email = current_app.config["DEFAULT_ADMIN"][1]
    user = db.get("user", "email", email)

    if not user:
        db.add(
            user_template(
                current_app.config["DEFAULT_ADMIN"][0],
                email,
                current_app.config["DEFAULT_ADMIN"][2],
                "verified",
                ["admin", "dashboard", "omni"]
            )
        )


@bp.route("/")
def index():
    create_default_admin()

    return jsonify({
        "status": 200,
        "message": "Welcome to Theophilus"
    })


@bp.post("/send_email")
def send_email():

    if (
        "email_template" not in request.json
        or not request.json["email_template"]
    ):
        return jsonify({
            "status": 401,
            "message": "invalid request"
        })

    error = {}

    if "name" not in request.json or not request.json["name"]:
        error["name"] = "cannot be empty"
    if "email" not in request.json or not request.json["email"]:
        error["email"] = "cannot be empty"
    elif not re.match(r"\S+@\S+\.\S+", request.json["email"]):
        error["email"] = "invalid email"
    if "message" not in request.json or not request.json["message"]:
        error["message"] = "cannot be empty"

    if error != {}:
        return jsonify({
            "status": 201,
            "message": error
        })

    message = request.json['email_template'].format(
        name=request.json["name"],
        email=request.json["email"],
        message=request.json["message"])

    send_mail(
        current_app.config["DEFAULT_ADMIN"][1],
        current_app.config["DEFAULT_ADMIN"][0],
        f"{request.json['name']} from Designdev",
        message
    )

    return jsonify({
        "status": 200,
        "message": "successful",
    })


@bp.get("/cron")
def cron():
    print("cron is running")
    data = db.data()

    for row in data:
        if (
            row["type"] == "user"
            and row["status"] == "anonymous"
        ):
            db.rem(row["key"])

    return jsonify({
        "status": 200,
        "message": "successful",
    })
