from flask import Blueprint, jsonify
from . import db
from .schema import post_schema

bp = Blueprint("tag", __name__)


def get_tags(data, key=None):
    tags = []
    for row in data:
        if (
            row["type"] in ["blog", "project"]
            and row["key"] != key
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

    blogs = []
    projects = []
    for row in data:
        if "tags" in row and tag in row["tags"]:
            if row["type"] == "blog":
                blogs.append(row)
            elif row["type"] == "project":
                projects.append(row)

    return jsonify({
        "status": 200,
        "message": "successful",
        "data": {
            "blogs": [post_schema(a) for a in blogs],
            "projects": [post_schema(a) for a in projects],
            "tags": get_tags(data)
        }
    })
