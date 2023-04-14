from flask import Blueprint, jsonify, request
from . import token_to_user, db, post_schema, comment_template


bp = Blueprint("comment", __name__)


@bp.post("/blog/comment/<key>")
@bp.post("/project/comment/<key>")
def add_comment(key):
    post_type = f"{request.url_rule}"[1:].split("/")[0]

    data = db.data()

    user = token_to_user(data)
    if not user:
        return jsonify({
            "status": 401,
            "message": "invalid request"
        })

    post = db.get(post_type, "key", key, data)
    if not post:
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

    comment_path = [post["key"]]
    if ("for_comment_key" in request.json
            and request.json["for_comment_key"]):
        sub_comment = db.get(
            "comment", "key", request.json["for_comment_key"], data)
        if sub_comment:
            comment_path = [*sub_comment["path"], sub_comment["key"]]

    comment = db.add(comment_template(
        request.json["comment"],
        user["key"],
        comment_path,
    ))
    data.append(comment)

    return jsonify({
        "status": 200,
        "message": "successful",
        "data": {
            "post": post_schema(post, data)
        }
    })
