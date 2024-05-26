from flask import Blueprint, jsonify, request
from . import db
from .tools import reserved_words, token_to_user
from .schema import now, post_schema
import re
from uuid import uuid4

bp = Blueprint("post", __name__)


def post_template(
        title: str,
        slug: str,
):
    return {
        "type": "post",
        "key": uuid4().hex,
        "version": uuid4().hex,
        "created_at": now(),
        "updated_at": now(),

        "status": "draft",  # draft, publish, deleted
        "slug": slug,
        "title": title,
        "content": "",
        "description": "",
        # "format": "markdown",  # markdown, url
        "photos": [],
        "videos": [],
        "tags": []
    }


@bp.post("/post")
def add_post():

    if "title" not in request.json or not request.json["title"]:
        return jsonify({
            "status": 400,
            "title": "cannot be empty"
        })

    data = db.data()

    user = token_to_user(data)
    if "admin" not in user["roles"]:
        return jsonify({
            "status": 400,
            "error": "unauthorised access"
        })

    slug = re.sub('-+', '-', re.sub(
        '[^a-zA-Z0-9]', '-', request.json["title"].lower()))

    slug_in_use = db.get("post", "slug", slug, data)
    if slug_in_use or slug in reserved_words:
        slug = f"{slug}-{str(uuid4().hex)[:10]}"

    post = db.add(post_template(
        request.json["title"],
        slug
    ))

    return jsonify({
        "status": 200,
        "post": post_schema(post, data)
    })


@bp.put("/post/title/<key>")
def update_title(key):
    if "title" not in request.json or not request.json["title"]:
        return jsonify({
            "status": 400,
            "title": "cannot be empty"
        })

    data = db.data()

    user = token_to_user(data)
    if "admin" not in user["roles"]:
        return jsonify({
            "status": 400,
            "error": "unauthorised access"
        })

    post = db.get_key(key, data)
    if not post:
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    slug = re.sub('-+', '-', re.sub(
        '[^a-zA-Z0-9]', '-', request.json["title"].lower()))

    slug_in_use = db.get(post["type"], "slug", slug, data)

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
        "post": post_schema(post, data)
    })


@bp.put("/post/description/<key>")
def update_description(key):

    data = db.data()

    user = token_to_user(data)
    if "admin" not in user["roles"]:
        return jsonify({
            "status": 400,
            "error": "unauthorised access"
        })

    post = db.get_key(key, data)
    if not post or "description" not in request.json:
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    post["updated_at"] = now()
    post["description"] = request.json["description"]

    db.add(post)

    return jsonify({
        "status": 200,
        "post": post_schema(post, data)
    })


@bp.put("/post/content/<key>")
def update_content(key):
    if "content" not in request.json or not request.json["content"]:
        return jsonify({
            "status": 400,
            "content": "cannot be empty"
        })

    data = db.data()

    user = token_to_user(data)
    if "admin" not in user["roles"]:
        return jsonify({
            "status": 400,
            "error": "unauthorised access"
        })

    post = db.get_key(key, data)
    if not post:
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    post["updated_at"] = now()
    post["content"] = request.json["content"]

    count = post["content"].count("{#video}")
    if count == 0:
        post["videos"] = []
    else:
        post["videos"] = post["videos"][:count]

    db.add(post)

    return jsonify({
        "status": 200,
        "post": post_schema(post, data)
    })


@bp.put("/post/date/<key>")
def update_date(key):
    error = {}
    if "date" not in request.json or not request.json["date"]:
        error["date"] = "cannot be empty"
    if "time" not in request.json or not request.json["time"]:
        error["time"] = "cannot be empty"

    if error != {}:
        return jsonify({
            "status": 400,
            **error
        })

    data = db.data()

    user = token_to_user(data)
    if "admin" not in user["roles"]:
        return jsonify({
            "status": 400,
            "error": "unauthorised access"
        })

    post = db.get_key(key, data)
    if not post:
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    post["updated_at"] = now()
    post["created_at"] = f"{request.json['date']}T{request.json['time']}"

    db.add(post)

    return jsonify({
        "status": 200,
        "post": post_schema(post, data)
    })


@bp.put("/post/tags/<key>")
def update_tags(key):

    data = db.data()

    user = token_to_user(data)
    if "admin" not in user["roles"]:
        return jsonify({
            "status": 400,
            "error": "unauthorised access"
        })

    post = db.get_key(key, data)
    if not post or "tags" not in request.json:
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    post["updated_at"] = now()
    post["tags"] = request.json["tags"]

    db.add(post)

    return jsonify({
        "status": 200,
        "post": post_schema(post, data)
    })


@ bp.put("/post/status/<key>")
def update_status(key):

    data = db.data()

    user = token_to_user(data)
    if "admin" not in user["roles"]:
        return jsonify({
            "status": 400,
            "error": "unauthorised access"
        })

    post = db.get_key(key, data)
    if (
        not post
        or "status" not in request.json or not request.json["status"]
        or request.json["status"] not in ["draft", "publish", "deleted"]
        or request.json["status"] == post["status"]
    ):
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    post["updated_at"] = now()
    post["status"] = request.json["status"]

    db.add(post)

    return jsonify({
        "status": 200,
        "post": post_schema(post, data)
    })


@ bp.put("/post/videos/<key>")
def update_videos(key):

    data = db.data()

    user = token_to_user(data)
    if "admin" not in user["roles"]:
        return jsonify({
            "status": 400,
            "error": "unauthorised access"
        })

    post = db.get_key(key, data)
    if (
        not post or "videos" not in request.json
        or type(request.json["videos"]) != "list"
    ):
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    post["updated_at"] = now()
    post["videos"] = request.json["videos"]

    db.add(post)

    return jsonify({
        "status": 200,
        "post": post_schema(post, data)
    })


@ bp.delete("/post/<key>")
def delete(key):

    data = db.data()

    user = token_to_user(data)
    if "admin" not in user["roles"]:
        return jsonify({
            "status": 400,
            "error": "unauthorised access"
        })

    post = None
    to_delete = []

    for row in data:
        if (
            row["key"] == key
            and row["type"] == "post"
        ):
            post = row
        elif (
            row["type"] == "comment"
            and row["path"][0] == key
            and row["status"] != "deleted"
        ):
            to_delete.append(row)

    if not post or post["status"] == "deleted":
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    to_delete.append(post)
    for row in to_delete:
        row["status"] = "deleted"
        row["updated_at"] = now()

    while len(to_delete) > 0:
        db.add_many(to_delete[:25])
        to_delete = to_delete[25:]

    return jsonify({
        "status": 200,
        "error": "successful"
    })
