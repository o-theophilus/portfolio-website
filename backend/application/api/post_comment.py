from flask import Blueprint, jsonify, request
from . import token_to_user, db, comment_template, comment_schema


bp = Blueprint("comment", __name__)


@bp.post("/comment/<key>")
def comment_add(key):
    data = db.data()

    owner = db.get_key(key)
    user = token_to_user(data)
    if (
        not user or not owner
        or owner["type"] not in ["blog", "project", "comment"]
    ):
        return jsonify({
            "status": 401,
            "message": "invalid request"
        })

    if user["status"] != "verified" or not user["login"]:
        return jsonify({
            "status": 102,
            "message": "unauthorised access"
        })

    if "comment" not in request.json or not request.json["comment"]:
        return jsonify({
            "status": 201,
            "message": {"comment": "cannot be empty"}
        })

    path = [owner["key"]]
    if owner["type"] == "comment":
        path = [*owner["path"], owner["key"]]

    comment = db.add(comment_template(
        request.json["comment"],
        user["key"],
        path,
    ))

    return jsonify({
        "status": 200,
        "message": "successful",
        "data": {
            "comment": comment_schema(comment, data)
        }
    })


@bp.post("/comment/vote/<key>")
def comment_upvote(key):
    data = db.data()

    user = token_to_user(data)
    comment = db.get("comment", "key", key, data)
    if (
        not user or not comment
        or "vote" not in request.json
        or not request.json["vote"]
        or request.json["vote"] not in ["up", "down"]
    ):
        return jsonify({
            "status": 401,
            "message": "invalid request"
        })

    if user["status"] != "verified" or not user["login"]:
        return jsonify({
            "status": 102,
            "message": "unauthorised access"
        })

    if user["key"] in comment["upvote"]:
        comment["upvote"].remove(user["key"])
    elif user["key"] in comment["downvote"]:
        comment["downvote"].remove(user["key"])

    comment[f"{request.json['vote']}vote"].append(user["key"])
    comment = db.add(comment)

    return jsonify({
        "status": 200,
        "message": "successful",
        "data": {
            "comment": comment_schema(comment, data)
        }
    })
