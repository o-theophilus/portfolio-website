from flask import Blueprint, jsonify, current_app, request
from itsdangerous import URLSafeTimedSerializer
from datetime import datetime, timedelta
from . import db
from werkzeug.security import generate_password_hash
from uuid import uuid4
import re
from .mail import send_mail


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


def now(day=0):
    return (datetime.now() + timedelta(days=1) * day).replace(
        microsecond=0).isoformat()


reserved_words = [
    "admin", "omni", "user", "users", "store", "stores", "item",
    "items"]  # property, cart, save


###############################################################################

def user_template(
        name: str,
        email: str,
        password: str,
        status: str = "anonymous",
        roles: list = []
):

    return {
        "type": "user",
        "key": uuid4().hex,
        "version": uuid4().hex,
        "created_at": now(),
        "updated_at": now(),

        "name": name,
        "email": email,
        "password": generate_password_hash(password, method="sha256"),

        "status": status,  # anonymous, verified, deleted
        "login": False,
        "roles": roles,
        "setting": {
                "theme": "dark"
        }
    }


def user_schema(u):
    return {
        "status": u["status"],

        "name": u["name"],
        "email": u["email"],

        "setting": u["setting"],

        "roles": u["roles"],
        "login": u["login"],

    }


def post_template(
        post_type: str,
        title: str,
        slug: str,
):
    return {
        "type": post_type,  # blog, project
        "key": uuid4().hex,
        "version": uuid4().hex,
        "created_at": now(),
        "updated_at": now(),

        "status": "draft",  # draft, publish, deleted
        "slug": slug,
        "title": title,
        "content": "",
        "description": "",
        "format": "markdown",  # markdown, url
        "photos": [],
        "videos": [],
        "tags": []
    }


def post_schema(p, data=[]):
    photos = []
    if "photos" in p:
        for photo in p['photos']:
            photos.append(f"/photo/{photo}")

    comments = []
    # if data:
    for row in data:
        if (
            row["type"] == "comment"
            and row["path"][0] == p["key"]
        ):
            comments.append(row)

    comments = sorted(comments, key=lambda d: d["created_at"], reverse=True)
    comments = [comment_schema(c) for c in comments]

    for comm in comments:
        for row in data:
            if row["type"] == "user" and comm["user_key"] == row["key"]:
                comm["name"] = row["name"]
                continue

    return {
        "key": p["key"],
        "status": p["status"],
        "title": p["title"],
        "format": p["format"],
        "photos": photos,
        "videos": p["videos"] if "videos" in p else [],
        "description": p["description"],
        "content": p["content"],
        "slug": p["slug"],
        "tags": p["tags"],
        "comments": comments,
        "type": p["type"],
        "created_at": p["created_at"],
    }


def comment_template(
        comment: str,
        user_key: str,
        path: list = [],
):
    return {
        "type": "comment",
        "key": uuid4().hex,
        "version": uuid4().hex,
        "created_at": now(),
        "updated_at": now(),

        "comment": comment,
        "user_key": user_key,
        "path": path,

        "status": "active",  # active, deleted
        "upvote": [],
        "downvote": []
    }


def comment_schema(c):
    return {
        "key": c["key"],
        "comment": c["comment"],
        "user_key": c["user_key"],
        "path": c["path"],

        "created_at": c["created_at"],

    }


###############################################################################


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
