from flask import Blueprint, jsonify, request
from . import token_to_user, db, post_schema, comment_template, rating_template


bp = Blueprint("comment", __name__)


@bp.post("/blog/comment/<key>")
@bp.post("/project/comment/<key>")
def add_comment(key):
    post_type = f"{request.url_rule}"[1:].split("/")[0]

    data = db.data()

    user = token_to_user(data)
    post = db.get(post_type, "key", key, data)
    if not user or not post:
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


@bp.post("/blog/rating/<key>")
@bp.post("/project/rating/<key>")
def add_rating(key):
    post_type = f"{request.url_rule}"[1:].split("/")[0]

    data = db.data()

    user = token_to_user(data)
    post = db.get(post_type, "key", key, data)
    if not user or not post:
        return jsonify({
            "status": 401,
            "message": "invalid request"
        })

    if user["status"] != "verified" or not user["login"]:
        return jsonify({
            "status": 102,
            "message": "unauthorised access"
        })

    rating_value = 0
    if (
        "rating" in request.json
        and type(request.json["rating"]) == int
        and -5 <= request.json["rating"] <= 5
    ):
        rating_value = request.json["rating"]

    rating = None
    for row in data:
        if (
            row["type"] == "rating"
            and row["user_key"] == user["key"]
            and row["post_key"] == post["key"]
        ):
            row["rating"] = rating_value
            rating = row
            break

    if not rating:
        rating = rating_template(
            rating_value,
            user["key"],
            post["key"]
        )
        data.append(rating)

    db.add(rating)

    return jsonify({
        "status": 200,
        "message": "successful",
        "data": {
            "post": post_schema(post, data)
        }
    })
