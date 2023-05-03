from flask import Blueprint, jsonify
from . import db, token_to_user
from .schema import post_schema, rating_schema
from .tag import get_tags
from .comment import get_comments

bp = Blueprint("post_read", __name__)


def add_rating(in_list, data):
    for p in in_list:
        p["rating"] = 0
        for row in data:
            if (
                row["type"] == "rating"
                and row["post_key"] == p["key"]
            ):
                p["rating"] += row["rating"]
    return in_list


@bp.get("/post/<slug>")
def get(slug):
    data = db.data()

    post = db.get("post", "slug", slug, data)
    user = token_to_user(data)
    if (
        not user
        or not post
        or post["status"] == "deleted"
    ):
        return jsonify({
            "status": 401,
            "message": "invalid request"
        })

    ratings = []
    for row in data:
        if (
            row["type"] == "rating"
            and row["post_key"] == post["key"]
        ):
            ratings.append(row)

    comments = get_comments(post["key"], data, user)
    comments = comments.json["data"]["comments"]

    return jsonify({
        "status": 200,
        "message": "successful",
        "data": {
            "post": post_schema(post, data),
            "tags": get_tags(data, post["key"]),
            "comments": comments,
            "ratings": [rating_schema(c) for c in ratings]
        }
    })


@bp.get("/post")
def get_all():
    data = db.data()

    user = token_to_user(data)
    if not user:
        return jsonify({
            "status": 401,
            "message": "invalid request"
        })

    posts = []
    for row in data:
        if (
            row["type"] == "post"
            and row["status"] != "deleted"
            and (
                row["status"] == "publish"
                or "admin" in user["roles"]
            )
        ):
            posts.append(row)

    if user["setting"]["sort_post_by"] == "rating":
        posts = add_rating(posts, data)
    elif user["setting"]["sort_post_by"] == "date":
        user["setting"]["sort_post_by"] = "created_at"
    posts = sorted(
        posts,
        key=lambda d: d[user["setting"]["sort_post_by"]].lower() if type(
            d[user["setting"]["sort_post_by"]]
        ) == str else d[user["setting"]["sort_post_by"]],
        reverse=user["setting"]["sort_post_reverse"])

    return jsonify({
        "status": 200,
        "message": "successful",
        "data": {
            "posts": [post_schema(a) for a in posts],
            "tags": get_tags(posts)
        }
    })
