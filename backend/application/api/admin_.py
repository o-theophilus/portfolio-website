from flask import Blueprint, jsonify, request
from . import token_to_user, db
from .schema import now, post_schema
from uuid import uuid4

bp = Blueprint("admin", __name__)


def get_setting(data):
    for row in data:
        if row["type"] == "setting":
            return row
    return None


@bp.get("/admin")
def admin():
    data = db.data()

    user = token_to_user(data)
    if not user or "admin" not in user["roles"]:
        return jsonify({
            "status": 102,
            "message": "unauthorised access"
        })

    setting = get_setting(data)
    if not setting:
        setting = db.add({
            "type": "setting",
            "key": uuid4().hex,
            "version": uuid4().hex,
            "created_at": now(),
            "updated_at": now(),
            "featured_posts": []
        })

    return jsonify({
        "status": 200,
        "message": "successful",
        "data": {
            "setting": {
                "featured_posts": setting["featured_posts"]
            }
        }
    })


@bp.get("/featured_post")
def get():
    data = db.data()

    setting = get_setting(data)

    posts = []
    if setting:
        for slug in setting["featured_posts"]:
            for row in data:
                if (
                    row["type"] == "post"
                    and row["slug"] == slug
                    and row["status"] == "publish"
                ):
                    posts.append(row)

    return jsonify({
        "status": 200,
        "message": "successful",
        "data": {
            "posts": [post_schema(a) for a in posts]
        }
    })


@bp.post("/featured_post")
def featured_post():
    if (
        "featured_posts" not in request.json
        or type(request.json["featured_posts"]) != list
    ):
        return jsonify({
            "status": 401,
            "message": "invalid request"
        })

    data = db.data()

    user = token_to_user(data)
    if not user or "admin" not in user["roles"]:
        return jsonify({
            "status": 102,
            "message": "unauthorised access"
        })

    setting = get_setting(data)

    slugs = []
    for slug in request.json["featured_posts"]:
        for row in data:
            if (
                row["type"] == "post"
                and row["slug"] == slug
                and row["status"] == "publish"
            ):
                slugs.append(row["slug"])

    setting["featured_posts"] = slugs
    db.add(setting)

    return jsonify({
        "status": 200,
        "message": "successful",
        "data": {
            "setting": setting
        }
    })


@bp.get("/slug")
def slug():
    data = db.data()

    slugs = []
    for row in data:
        if row["type"] == "post" and row["status"] == "publish":
            slugs.append(row["slug"])

    return jsonify({
        "status": 200,
        "message": "successful",
        "data": {
            "slugs": slugs
        }
    })
