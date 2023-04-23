from flask import Blueprint, jsonify, request
from . import db, token_to_user
from .schema import post_schema, comment_schema, rating_schema
from .tag import get_tags

bp = Blueprint("post_read", __name__)


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

    comments = []
    ratings = []
    for row in data:
        if (
            row["type"] == "comment"
            and row["path"][0] == post["key"]
        ):
            comments.append(row)
        elif (
            row["type"] == "rating"
            and row["post_key"] == post["key"]
        ):
            ratings.append(row)

    comments = [comment_schema(c, data) for c in comments]
    comments = sorted(comments, key=lambda d: d["created_at"], reverse=False)
    ratings = [rating_schema(c) for c in ratings]

    # people = [
    #     {
    #         'name': 'Alice',
    #         'age': 25
    #     }, {
    #         'name': 'Bob',
    #         'age': 30
    #     }, {
    #         'name': 'Charlie',
    #         'age': 20
    #     }, {
    #         'name': 'Alice',
    #         'age': 20
    #      }
    # ]
    # sorted_people = sorted(people, key=lambda p: (p['name'], p['age']))
    # print(sorted_people)

    return jsonify({
        "status": 200,
        "message": "successful",
        "data": {
            "post": post_schema(post, data),
            "tags": get_tags(data, post["key"]),
            "comments": comments,
            "ratings": ratings
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
