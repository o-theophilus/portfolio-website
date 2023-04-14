from flask import Blueprint, jsonify, request
from . import (reserved_words, now, token_to_user, db, post_template,
               post_schema)
import re
from uuid import uuid4

bp = Blueprint("post", __name__)


@bp.post("/blog")
@bp.post("/project")
def add_post():
    data = db.data()

    user = token_to_user(data)
    if "admin" not in user["roles"]:
        return jsonify({
            "status": 102,
            "message": "unauthorised access"
        })

    if "title" not in request.json or not request.json["title"]:
        return jsonify({
            "status": 201,
            "message": "cannot be empty"
        })

    post_type = f"{request.url_rule}"[1:]

    slug = re.sub('-+', '-', re.sub(
        '[^a-zA-Z0-9]', '-', request.json["title"].lower()))

    slug_in_use = db.get(post_type, "slug", slug, data)
    if slug_in_use or slug in reserved_words:
        slug = f"{slug}-{str(uuid4().hex)[:10]}"

    post = db.add(post_template(
        post_type,
        request.json["title"],
        slug
    ))

    return jsonify({
        "status": 200,
        "message": "successful",
        "data": {
            "post": post_schema(post)
        }
    })


@bp.put("/blog/title/<slug>")
@bp.put("/project/title/<slug>")
def update_title(slug):
    post_type = f"{request.url_rule}"[1:].split("/")[0]
    data = db.data()

    user = token_to_user(data)
    if "admin" not in user["roles"]:
        return jsonify({
            "status": 102,
            "message": "unauthorised access"
        })

    post = db.get(post_type, "slug", slug, data)
    if not post:
        return jsonify({
            "status": 401,
            "message": "invalid request"
        })

    if "title" not in request.json or not request.json["title"]:
        return jsonify({
            "status": 201,
            "message": "cannot be empty"
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
            "post": post_schema(post)
        }
    })


@bp.put("/blog/description/<slug>")
@bp.put("/project/description/<slug>")
def update_description(slug):
    post_type = f"{request.url_rule}"[1:].split("/")[0]

    data = db.data()

    user = token_to_user(data)
    if "admin" not in user["roles"]:
        return jsonify({
            "status": 102,
            "message": "unauthorised access"
        })

    post = db.get(post_type, "slug", slug, data)
    if not post:
        return jsonify({
            "status": 401,
            "message": "invalid request"
        })

    if "description" not in request.json or not request.json["description"]:
        return jsonify({
            "status": 201,
            "message": "cannot be empty"
        })

    post["updated_at"] = now()
    post["description"] = request.json["description"]

    db.add(post)

    return jsonify({
        "status": 200,
        "message": "successful",
        "data": {
            "post": post_schema(post)
        }
    })


@bp.put("/blog/content/<slug>")
@bp.put("/project/content/<slug>")
def update_content(slug):
    post_type = f"{request.url_rule}"[1:].split("/")[0]

    data = db.data()

    user = token_to_user(data)
    if "admin" not in user["roles"]:
        return jsonify({
            "status": 102,
            "message": "unauthorised access"
        })

    post = db.get(post_type, "slug", slug, data)
    if not post:
        return jsonify({
            "status": 401,
            "message": "invalid request"
        })

    error = {}
    if "format" not in request.json or not request.json["format"]:
        error["format"] = "cannot be empty"
    if "content" not in request.json or not request.json["content"]:
        error["content"] = "cannot be empty"

    if len(error):
        return jsonify({
            "status": 201,
            "message": error
        })

    post["updated_at"] = now()
    post["format"] = request.json["format"]
    post["content"] = request.json["content"]

    count = post["content"].count("{#video}")
    if count == 0:
        post["videos"] = []
    else:
        post["videos"] = post["videos"][:count]

    db.add(post)

    return jsonify({
        "status": 200,
        "message": "successful",
        "data": {
            "post": post_schema(post)
        }
    })


@bp.put("/blog/date/<slug>")
@bp.put("/project/date/<slug>")
def update_date(slug):
    post_type = f"{request.url_rule}"[1:].split("/")[0]

    data = db.data()

    user = token_to_user(data)
    if "admin" not in user["roles"]:
        return jsonify({
            "status": 102,
            "message": "unauthorised access"
        })

    error = {}

    if "date" not in request.json or not request.json["date"]:
        error["date"] = "cannot be empty"

    if "time" not in request.json or not request.json["time"]:
        error["time"] = "cannot be empty"

    if error != {}:
        return jsonify({
            "status": 201,
            "message": error
        })

    post = db.get(post_type, "slug", slug, data)
    if not post:
        return jsonify({
            "status": 401,
            "message": "invalid request"
        })

    post["updated_at"] = now()
    post["created_at"] = f"{request.json['date']}T{request.json['time']}"

    db.add(post)

    return jsonify({
        "status": 200,
        "message": "successful",
        "data": {
            "post": post_schema(post)
        }
    })


@bp.put("/blog/tags/<slug>")
@bp.put("/project/tags/<slug>")
def update_tags(slug):
    post_type = f"{request.url_rule}"[1:].split("/")[0]

    data = db.data()

    user = token_to_user(data)
    if "admin" not in user["roles"]:
        return jsonify({
            "status": 102,
            "message": "unauthorised access"
        })

    post = db.get(post_type, "slug", slug, data)
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
            "post": post_schema(post)
        }
    })


@ bp.put("/blog/status/<slug>")
@ bp.put("/project/status/<slug>")
def update_status(slug):
    post_type = f"{request.url_rule}"[1:].split("/")[0]

    data = db.data()

    user = token_to_user(data)
    if "admin" not in user["roles"]:
        return jsonify({
            "status": 102,
            "message": "unauthorised access"
        })

    post = db.get(post_type, "slug", slug, data)
    if not post:
        return jsonify({
            "status": 401,
            "message": "invalid request"
        })

    if "post_status" not in request.json or not request.json["post_status"]:
        return jsonify({
            "status": 401,
            "message": "invalid request"
        })

    status = request.json["post_status"]
    if (status not in ["draft", "publish", "deleted"]
            or status == post["status"]):
        return jsonify({
            "status": 401,
            "message": "invalid request"
        })

    post["updated_at"] = now()
    post["status"] = status

    db.add(post)

    return jsonify({
        "status": 200,
        "message": "successful",
        "data": {
            "post": post_schema(post)
        }
    })


@ bp.put("/blog/videos/<slug>")
@ bp.put("/project/videos/<slug>")
def update_videos(slug):
    post_type = f"{request.url_rule}"[1:].split("/")[0]

    data = db.data()

    user = token_to_user(data)
    if "admin" not in user["roles"]:
        return jsonify({
            "status": 102,
            "message": "unauthorised access"
        })

    if "videos" not in request.json:
        return jsonify({
            "status": 201,
            "message": "invalid request"
        })

    post = db.get(post_type, "slug", slug, data)
    if not post:
        return jsonify({
            "status": 401,
            "message": "invalid request"
        })

    post["updated_at"] = now()
    post["videos"] = request.json["videos"]

    db.add(post)

    return jsonify({
        "status": 200,
        "message": "successful",
        "data": {
            "post": post_schema(post)
        }
    })


@ bp.delete("/blog/<slug>")
@ bp.delete("/project/<slug>")
def delete(slug):
    post_type = f"{request.url_rule}"[1:].split("/")[0]

    data = db.data()

    user = token_to_user(data)
    if "admin" not in user["roles"]:
        return jsonify({
            "status": 102,
            "message": "unauthorised access"
        })

    post = db.get(post_type, "slug", slug, data)

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
