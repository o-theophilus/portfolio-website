from flask import Blueprint, jsonify, request
from . import reserved_words, now
import re
from uuid import uuid4
from . import db
from .schema import post, schema

bp = Blueprint("post", __name__)


@bp.post("/blog")
@bp.post("/project")
def add_post():
    if "title" not in request.json or not request.json["title"]:
        return jsonify({
            "status": 201,
            "message": "this field is required"
        })

    post_type = f"{request.url_rule}"[1:]

    slug = re.sub('-+', '-', re.sub(
        '[^a-zA-Z0-9]', '-', request.json["title"].lower()))

    slug_in_use = db.get(post_type, "slug", slug)
    if slug_in_use or slug in reserved_words:
        slug = f"{slug}-{str(uuid4().hex)[:10]}"

    post["key"] = uuid4().hex
    post["version"] = uuid4().hex
    post["title"] = request.json["title"]
    post["slug"] = slug
    post["type"] = post_type

    db.add(post)

    return jsonify({
        "status": 200,
        "message": "successful",
        "data": {
            "post": schema(post)
        }
    })


@bp.put("/blog/title/<slug>")
@bp.put("/project/title/<slug>")
def update_title(slug):
    post_type = f"{request.url_rule}"[1:].split("/")[0]
    data = db.data()

    post = db.get(post_type, "slug", slug, data)
    if not post:
        return jsonify({
            "status": 401,
            "message": "invalid request"
        })

    if "title" not in request.json or not request.json["title"]:
        return jsonify({
            "status": 201,
            "message": "this field is required"
        })

    slug = re.sub('-+', '-', re.sub(
        '[^a-zA-Z0-9]', '-', request.json["title"].lower()))

    slug_in_use = db.get(post_type, "slug", slug, data)

    if (
        (slug_in_use and slug_in_use['key'] != post["key"])
        or slug in reserved_words
    ):
        slug = f"{slug}-{str(uuid4().hex)[:10]}"

    post["updated_at"] = now()
    post["title"] = request.json["title"]
    post["slug"] = slug

    db.add(post)

    return jsonify({
        "status": 200,
        "message": "successful",
        "data": {
            "post": schema(post)
        }
    })


@bp.put("/blog/description/<slug>")
@bp.put("/project/description/<slug>")
def update_description(slug):
    post_type = f"{request.url_rule}"[1:].split("/")[0]

    post = db.get(post_type, "slug", slug)
    if not post:
        return jsonify({
            "status": 401,
            "message": "invalid request"
        })

    if "description" not in request.json or not request.json["description"]:
        return jsonify({
            "status": 201,
            "message": "this field is required"
        })

    post["updated_at"] = now()
    post["description"] = request.json["description"]

    db.add(post)

    return jsonify({
        "status": 200,
        "message": "successful",
        "data": {
            "post": schema(post)
        }
    })


@bp.put("/blog/tags/<slug>")
@bp.put("/project/tags/<slug>")
def update_tags(slug):
    post_type = f"{request.url_rule}"[1:].split("/")[0]

    post = db.get(post_type, "slug", slug)
    if not post:
        return jsonify({
            "status": 401,
            "message": "invalid request"
        })

    post["updated_at"] = now()
    post["tags"] = request.json["tags"]

    db.add(post)

    return jsonify({
        "status": 200,
        "message": "successful",
        "data": {
            "post": schema(post)
        }
    })


@bp.put("/blog/content/<slug>")
@bp.put("/project/content/<slug>")
def update_content(slug):
    post_type = f"{request.url_rule}"[1:].split("/")[0]

    post = db.get(post_type, "slug", slug)
    if not post:
        return jsonify({
            "status": 401,
            "message": "invalid request"
        })

    error = {}
    if "format" not in request.json or not request.json["format"]:
        error["format"] = "this field is required"
    if "content" not in request.json or not request.json["content"]:
        error["content"] = "this field is required"

    if len(error):
        return jsonify({
            "status": 201,
            "message": error
        })

    post["updated_at"] = now()
    post["format"] = request.json["format"]
    post["content"] = request.json["content"]

    db.add(post)

    return jsonify({
        "status": 200,
        "message": "successful",
        "data": {
            "post": schema(post)
        }
    })


@bp.put("/blog/status/<slug>")
@bp.put("/project/status/<slug>")
def update_status(slug):
    post_type = f"{request.url_rule}"[1:].split("/")[0]

    post = db.get(post_type, "slug", slug)
    if not post:
        return jsonify({
            "status": 401,
            "message": "invalid request"
        })

    if "status" not in request.json or not request.json["status"]:
        return jsonify({
            "status": 201,
            "message": "this field is required"
        })

    post["updated_at"] = now()
    post["status"] = request.json["status"]

    db.add(post)

    return jsonify({
        "status": 200,
        "message": "successful",
        "data": {
            "post": schema(post)
        }
    })


@bp.delete("/blog/<slug>")
@bp.delete("/project/<slug>")
def delete(slug):
    post_type = f"{request.url_rule}"[1:].split("/")[0]
    post = db.get(post_type, "slug", slug)

    if not post:
        return jsonify({
            "status": 401,
            "message": "invalid request"
        })

    db.rem(post["key"])

    return jsonify({
        "status": 200,
        "message": "successful"
    })
