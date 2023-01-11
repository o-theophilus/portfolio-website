from flask import Blueprint, jsonify
from . import db
from .schema import schema

bp = Blueprint("tag", __name__)


def get_tags(data, key=None):
    tags = []
    for row in data:
        if (
            row["type"] in ["blog", "project"]
            and row["key"] != key
            and row["tags"]
        ):
            tags.append(row["tags"])

    tags = ", ".join(tags).split(", ")
    tags = list(set(tags))
    tags.sort()
    tags = ", ".join(tags)
    return tags


@bp.get("/tag")
def get_all():
    return jsonify({
        "status": 200,
        "message": "successful",
        "data": {
            "tags": get_tags(db.data())
        }
    })


@bp.get("/tag/<tag>")
def get(tag):
    data = db.data()

    blogs = []
    projects = []
    for row in data:
        if tag in row["tags"]:
            if row["type"] == "blog":
                blogs.append(row)
            elif row["type"] == "project":
                projects.append(row)

    return jsonify({
        "status": 200,
        "message": "successful",
        "data": {
            "blogs": [schema(a) for a in blogs],
            "projects": [schema(a) for a in projects],
            "tags": get_tags(data)
        }
    })
