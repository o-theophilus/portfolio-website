from flask import Blueprint, jsonify, request
from . import token_to_user, db
from .schema import rating_schema, rating_template


bp = Blueprint("rating", __name__)


@bp.post("/rating/<key>")
def add_rating(key):

    data = db.data()

    user = token_to_user(data)
    post = db.get_key(key, data)
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
    ratings = []
    for row in data:
        if (
            row["type"] == "rating"
            and row["post_key"] == post["key"]
        ):
            ratings.append(row)
            if row["user_key"] == user["key"]:
                row["rating"] = rating_value
                rating = row

    if not rating:
        rating = rating_template(
            rating_value,
            user["key"],
            post["key"]
        )
        data.append(rating)

    db.add(rating)

    ratings = [rating_schema(c) for c in ratings]

    return jsonify({
        "status": 200,
        "message": "successful",
        "data": {
            "ratings": ratings
        }
    })
