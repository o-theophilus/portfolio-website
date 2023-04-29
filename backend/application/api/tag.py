from flask import Blueprint, jsonify
from . import db, token_to_user
from .schema import post_schema

bp = Blueprint("tag", __name__)


def get_tags(data, key=None):
    user = token_to_user(data)

    tags = []
    for row in data:
        if (
            row["type"] == "post"
            and row["status"] != "deleted"
            and row["key"] != key
            and (
                row["status"] == "publish"
                or user and "admin" in user["roles"]
            )
        ):
            tags = [*tags, *row["tags"]]

    tags = list(set(tags))
    tags.sort()
    return tags


@bp.get("/tags")
def get_all():
    return jsonify({
        "status": 200,
        "message": "successful",
        "data": {
            "tags": get_tags(db.data())
        }
    })


@bp.get("/tags/<tag>")
def get(tag):
    data = db.data()

    user = token_to_user(data)
    posts = []
    for row in data:
        if (
            row["type"] == "post"
            and row["status"] != "deleted"
            and tag in row["tags"]
            and (
                row["status"] == "publish"
                or user and "admin" in user["roles"]
            )
        ):
            posts.append(row)

    return jsonify({
        "status": 200,
        "message": "successful",
        "data": {
            "posts": [post_schema(a) for a in posts],
            "tags": get_tags(data)
        }
    })
