from flask import Blueprint, jsonify, request
from . import token_to_user, db
from .schema import comment_template, comment_schema


bp = Blueprint("comment", __name__)


@bp.get("/comment/<key>")
def get_comments(key, data=None, user=None):
    data = data if data else db.data()
    user = user if user else token_to_user(data)
    if not user:
        return jsonify({
            "status": 401,
            "message": "invalid request"
        })

    setting = user["setting"]

    comments = []
    for row in data:
        if (
            row["type"] == "comment"
            and row["status"] != "deleted"
            and row["path"][0] == key
        ):
            if setting["sort_comment_by"] == "vote":
                row["vote"] = len(row["upvote"]) - len(row["downvote"])
            comments.append(row)

    if setting["sort_comment_by"] == "date":
        setting["sort_comment_by"] = "created_at"
    comments = sorted(
        comments,
        key=lambda d: d[setting["sort_comment_by"]],
        reverse=setting["sort_comment_reverse"])

    return jsonify({
        "status": 200,
        "message": "successful",
        "data": {
            "comments": [comment_schema(c, data) for c in comments]
        }
    })


@bp.post("/comment/<key>")
def add(key):
    if "comment" not in request.json or not request.json["comment"]:
        return jsonify({
            "status": 201,
            "message": {
                "comment": "cannot be empty"
            }
        })

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

    path = [owner["key"]]
    if owner["type"] == "comment":
        path = [*owner["path"], owner["key"]]

    comment = db.add(comment_template(
        request.json["comment"],
        user["key"],
        path,
    ))

    data.append(comment)
    return get_comments(comment["path"][0], data, user)


@bp.post("/comment/vote/<key>")
def vote(key):
    data = db.data()

    user = token_to_user(data)
    comment = db.get("comment", "key", key, data)
    if (
        not user or not comment
        or comment["status"] == "deleted"
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
    db.add(comment)

    for row in data:
        if row["key"] == comment["key"]:
            row = comment

    return get_comments(comment["path"][0], data, user)


@bp.delete("/comment/<key>")
def delete(key):
    data = db.data()

    user = token_to_user(data)

    comment = None
    to_delete = []

    for row in data:
        if (
            row["key"] == key
            and row["type"] == "comment"
        ):
            comment = row
        elif (
            row["type"] == "comment"
            and key in row["path"]
        ):
            to_delete.append(row)

    if (
        not user or not comment
        or comment["status"] == "deleted"
        or comment["user_key"] != user["key"]
    ):
        return jsonify({
            "status": 401,
            "message": "invalid request"
        })

    to_delete.append(comment)
    for row in to_delete:
        row["status"] = "deleted"

    while len(to_delete) > 0:
        db.add_many(to_delete[:25])
        to_delete = to_delete[25:]

    for row in data:
        for rox in to_delete:
            if row["key"] == rox["key"]:
                row = rox

    return get_comments(comment["path"][0], data, user)
