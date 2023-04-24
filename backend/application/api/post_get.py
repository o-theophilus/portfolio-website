from flask import Blueprint, jsonify, request
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


@bp.get("/blog/<slug>")
@bp.get("/project/<slug>")
def get(slug):
    data = db.data()

    post_type = f"{request.url_rule}"[1:].split("/")[0]
    post = db.get(post_type, "slug", slug, data)

    user = token_to_user(data)
    if not post or not user:
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


@bp.get("/blog")
@bp.get("/project")
def get_all():
    data = db.data()
    post_type = f"{request.url_rule}"[1:]
    posts = db.get_type(post_type, data)

    user = token_to_user(data)
    if not user or "admin" not in user["roles"]:
        temp = []
        for p in posts:
            if p["status"] == "publish":
                temp.append(p)
        posts = temp

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


@bp.get("/post")
def get_blog_project():
    data = db.data()

    blogs = []
    projects = []
    for row in data:
        if "type" in row and "status" in row and row["status"] == "publish":
            if row["type"] == "blog":
                blogs.append(row)
            elif row["type"] == "project":
                projects.append(row)

    return jsonify({
        "status": 200,
        "message": "successful",
        "data": {
            "blogs": [post_schema(a) for a in blogs],
            "projects": [post_schema(a) for a in projects]
        }
    })
