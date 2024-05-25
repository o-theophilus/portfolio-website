from flask import Blueprint, jsonify, request
from .api import db, token_to_user
from .schema import user_schema, now


bp = Blueprint("user", __name__)


@ bp.post("/user/theme")
def user_theme():
    user = token_to_user()
    if not user:
        return jsonify({
            "status": 401,
            "message": "invalid request"
        })

    if user["setting"]["theme"] == "dark":
        user["setting"]["theme"] = "light"
    else:
        user["setting"]["theme"] = "dark"

    user["updated_at"] = now()
    user = db.add(user)

    return jsonify({
        "status": 200,
        "message": "successful",
        "data": {
            "user": user_schema(user)
        }
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
        or type(request.json["sort_post_reverse"]) != bool
        or "sort_comment_by" not in request.json
        or not request.json["sort_comment_by"]
        or request.json["sort_comment_by"] not in ["date", "vote"]
        or "sort_comment_reverse" not in request.json
        or type(request.json["sort_comment_reverse"]) != bool
    ):
        return jsonify({
            "status": 401,
            "message": "invalid request"
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
        "message": "successful",
        "data": {
            "user": user_schema(user)
        }
    })
