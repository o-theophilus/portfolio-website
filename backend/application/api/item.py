from flask import Blueprint, jsonify, request
from .tools import reserved_words, now
import re
from uuid import uuid4
from .detabase import get_db, db_get, db_add, db_delete

bp = Blueprint("item", __name__)


@bp.post("/project")
def project_create():
    return create("project").json


@bp.post("/blog")
def blog_create():
    return create("blog").json


def create(type_):
    db = get_db()

    error = {}
    if "type" not in request.json or not request.json["type"]:
        error["type"] = "This field is required"
    if "title" not in request.json or not request.json["title"]:
        error["title"] = "This field is required"
    if "description" not in request.json or not request.json["description"]:
        error["description"] = "This field is required"
    if "photo" not in request.json or not request.json["photo"]:
        error["photo"] = "This field is required"
    if "content" not in request.json or not request.json["content"]:
        error["content"] = "This field is required"
    if "format" not in request.json or not request.json["format"]:
        error["format"] = "This field is required"

    if error != {}:
        return jsonify({
            "status": 201,
            "message": error
        })

    slug = re.sub('-+', '-', re.sub(
        '[^a-zA-Z0-9]', '-', request.json["title"].lower()))

    item = db_get(db, type_, "slug", slug)
    if item or slug in reserved_words:
        slug = f"{slug}-{str(uuid4().hex)[:10]}"

    item = {
        "key": uuid4().hex,
        "version": uuid4().hex,
        "status": "draft",
        "type": type_,

        "created_at": now(),
        "updated_at": now(),

        "title": request.json["title"],
        "slug": slug,
        "photo": None,
        "tags": [],
        "format": request.json["format"],
        "description": request.json["description"],
        "content": request.json["content"],
    }

    db_add(item)

    return jsonify({
        "status": 200,
        "message": "successful",
        "data": {
            "item": item
        }
    })


@bp.get("/<type_>/<slug>")
def get(type_, slug):
    db = get_db()

    item = db_get(db, type_, "slug", slug)
    if not item:
        return jsonify({
            "status": 401,
            "message": "invalid request"
        })

    return jsonify({
        "status": 200,
        "message": "successful",
        "data": {
            "item": item
        }
    })


@bp.put("/<type_>/<slug>")
def update(type_, slug):
    db = get_db()

    item = db_get(db, type_, "slug", slug)
    if not item:
        return jsonify({
            "status": 401,
            "message": "invalid request"
        })

    error = {}
    if "type" not in request.json or not request.json["type"]:
        error["type"] = "This field is required"
    if "title" not in request.json or not request.json["title"]:
        error["title"] = "This field is required"
    if "description" not in request.json or not request.json["description"]:
        error["description"] = "This field is required"
    if "photo" not in request.json or not request.json["photo"]:
        error["photo"] = "This field is required"
    if "content" not in request.json or not request.json["content"]:
        error["content"] = "This field is required"
    if "format" not in request.json or not request.json["format"]:
        error["format"] = "This field is required"

    if error != {}:
        return jsonify({
            "status": 201,
            "message": error
        })

    slug = re.sub('-+', '-', re.sub(
        '[^a-zA-Z0-9]', '-', request.json["title"].lower()))

    slug_in_use = db_get(db, type_, "slug", slug)

    if (
        (slug_in_use and slug_in_use['key'] != item["key"])
        or slug in reserved_words
    ):
        slug = f"{slug}-{str(uuid4().hex)[:10]}"

    item["updated_at"] = now()
    item["title"] = request.json["title"]
    item["slug"] = slug
    item["format"] = request.json["format"]
    item["description"] = request.json["description"]
    item["content"] = request.json["content"]

    db_add(item)

    return jsonify({
        "status": 200,
        "message": "successful",
        "data": {
            "item": item
        }
    })


@bp.put("/<type_>/_/<slug>")
def change_status(type_, slug):
    db = get_db()

    if "status" not in request.json or not request.json["status"]:
        return jsonify({
            "status": 401,
            "message": "invalid request"
        })

    item = db_get(db, type_, "slug", slug)
    if not item:
        return jsonify({
            "status": 401,
            "message": "invalid request"
        })

    item["status"] = request.json["status"]
    item["updated_at"] = now()

    item = db_add(item)

    return jsonify({
        "status": 200,
        "message": "successful",
        "data": {
            "item": item
        }
    })


@bp.delete("/<type_>/<slug>")
def delete(type_, slug):
    db = get_db()

    item = db_get(db, type_, "slug", slug)
    if not item:
        return jsonify({
            "status": 401,
            "message": "invalid request"
        })

    db_delete(item["key"])

    return jsonify({
        "status": 200,
        "message": "successful"
    })
