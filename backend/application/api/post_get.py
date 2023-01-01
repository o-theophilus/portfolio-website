from flask import Blueprint, jsonify, request
from . import db
from .schema import schema

bp = Blueprint("post_read", __name__)


def get_all_tags(data, key=None):
    all_tags = []
    for row in data:
        if (
            row["type"] in ["blog", "project"]
            and row["key"] != key
            and row["tags"]
        ):
            all_tags.append(row["tags"])

    all_tags = ", ".join(all_tags).split(", ")
    all_tags = list(set(all_tags))
    all_tags.sort()
    all_tags = ", ".join(all_tags)
    return all_tags


@bp.get("/blog/<slug>")
@bp.get("/project/<slug>")
def get(slug):
    data = db.data()

    post_type = f"{request.url_rule}"[1:].split("/")[0]
    post = db.get(post_type, "slug", slug, data)

    if not post:
        return jsonify({
            "status": 401,
            "message": "invalid request"
        })

    return jsonify({
        "status": 200,
        "message": "successful",
        "data": {
            "post": schema(post),
            "all_tags": get_all_tags(data, post["key"])
        }
    })


@bp.get("/blog")
@bp.get("/project")
def get_all():
    data = db.data()

    post_type = f"{request.url_rule}"[1:]
    posts = db.get_type(post_type, data)

    return jsonify({
        "status": 200,
        "message": "successful",
        "data": {
            "posts": [schema(a) for a in posts],
            "all_tags": get_all_tags(data)
        }
    })


# @bp.get("/blog_project")
# def get_blog_projects():
#     data = db.db()

#     blogs = []
#     projects = []
#     for row in data:
#         if "type" in row:
#             if row["type"] == "blog":
#                 blogs.append(row)
#             elif row["type"] == "project":
#                 projects.append(row)

#     return jsonify({
#         "status": 200,
#         "message": "successful",
#         "data": {
#             "blogs": [schema(a) for a in blogs],
#             "projects": [schema(a) for a in projects]
#         }
#     })
