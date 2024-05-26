from flask import Blueprint, jsonify, request
from . import db
from .tools import token_to_user
from .schema import now
from werkzeug.security import generate_password_hash
from uuid import uuid4


bp = Blueprint("user", __name__)


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
        "password": generate_password_hash(password, method="scrypt"),

        "status": status,  # anonymous, verified, deleted
        "login": False,
        "roles": roles,
        "setting": {
            "theme": "dark",
            "sort_post_by": "date",  # rating, date, title
            "sort_post_reverse": False,
            "sort_comment_by": "date",  # vote, date
            "sort_comment_reverse": False
        }
    }


@ bp.post("/user/theme")
def user_theme():
    user = token_to_user()
    if not user:
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    if user["setting"]["theme"] == "dark":
        user["setting"]["theme"] = "light"
    else:
        user["setting"]["theme"] = "dark"

    user["updated_at"] = now()
    user = db.add(user)

    return jsonify({
        "status": 200,
        "user": user_schema(user)
    })


@ bp.post("/setting")
def user_setting():
    user = token_to_user()
    if (
        not user
        or "theme" not in request.json
        or not request.json["theme"]
        or request.json["theme"] not in ["dark", "light"]
        or "sort_post_by" not in request.json
        or not request.json["sort_post_by"]
        or request.json["sort_post_by"] not in ["date", "title", "rating"]
        or "sort_post_reverse" not in request.json
        or type(request.json["sort_post_reverse"]) is not bool
        or "sort_comment_by" not in request.json
        or not request.json["sort_comment_by"]
        or request.json["sort_comment_by"] not in ["date", "vote"]
        or "sort_comment_reverse" not in request.json
        or type(request.json["sort_comment_reverse"]) is not bool
    ):
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    user["setting"]["theme"] = request.json["theme"]
    user["setting"]["sort_post_by"] = request.json["sort_post_by"]
    user["setting"]["sort_post_reverse"] = request.json["sort_post_reverse"]
    user["setting"]["sort_comment_by"] = request.json["sort_comment_by"]
    user["setting"]["sort_comment_reverse"] = request.json[
        "sort_comment_reverse"]
    user["updated_at"] = now()
    db.add(user)

    return jsonify({
        "status": 200,
        "user": user_schema(user)
    })
