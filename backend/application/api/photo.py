from flask import Blueprint, jsonify, request, send_file
from . import db, token_to_user, dd
from .schema import post_schema
from PIL import Image, ImageOps
from io import BytesIO

bp = Blueprint("photo", __name__)


@bp.get("/photo/<name>")
@bp.get("/photo/<name>/<thumbnail>")
def get(name, thumbnail=None):
    photo = dd.get(name, "post")

    if not photo:
        return jsonify({
            "status": 201,
            "message": "not found"
        })

    if thumbnail:
        temp = Image.open(BytesIO(photo.read()))
        temp = ImageOps.fit(temp, (512, 512), Image.ANTIALIAS)

        photo = BytesIO()
        temp.save(photo, format="JPEG")
        photo.seek(0)

    return send_file(photo, mimetype="image/jpg")


@bp.post("/photo/<key>")
def post_many(key):
    if 'files' not in request.files:
        return jsonify({
            "status": 401,
            "message": "invalid request"
        })

    data = db.data()

    user = token_to_user(data)
    if "admin" not in user["roles"]:
        return jsonify({
            "status": 102,
            "message": "unauthorised access"
        })

    files = request.files.getlist("files")

    for file in files:
        media, format = file.content_type.split("/")
        if media not in ["image", "video"] or format in ['svg+xml', 'x-icon']:
            return jsonify({
                "status": 201,
                "message": "invalid file type"
            })

    post = db.get_key(key, data)
    count = post["content"].count("{#photo}") + 1
    if not post or len(post["photos"]) + len(files) > count:
        return jsonify({
            "status": 401,
            "message": "invalid request"
        })

    for file in files:
        filename = dd.add(file, "post", True)
        post["photos"].append(filename)
    db.add(post)

    return jsonify({
        "status": 200,
        "message": "successful",
        "data": {
            "post": post_schema(post)
        }
    })


@bp.put("/photo/<key>")
def arrange(key):

    data = db.data()

    user = token_to_user(data)
    if "admin" not in user["roles"]:
        return jsonify({
            "status": 102,
            "message": "unauthorised access"
        })

    def get_photo_names():
        return [p.split("/")[-1] for p in request.json["photos"]]

    post = db.get_key(key, data)
    if (
        not post
        or "photos" not in request.json
        or type(request.json["photos"]) != "list"
        or set(post["photos"]) != set(get_photo_names())
    ):
        return jsonify({
            "status": 401,
            "message": "invalid request"
        })

    post["photos"] = get_photo_names()
    db.add(post)

    return jsonify({
        "status": 200,
        "message": "successful",
        "data": {
            "post": post_schema(post)
        }
    })


@bp.delete("/photo/<key>")
def delete(key):

    data = db.data()

    user = token_to_user(data)
    if "admin" not in user["roles"]:
        return jsonify({
            "status": 102,
            "message": "unauthorised access"
        })

    def active_photo():
        return request.json["active_photo"].split("/")[-1]

    post = db.get_key(key, data)
    if (
        not post
        or "active_photo" not in request.json
        or not request.json["active_photo"]
        or active_photo() not in post["photos"]
    ):
        return jsonify({
            "status": 401,
            "message": "invalid request"
        })

    post["photos"].remove(active_photo())
    dd.rem(active_photo(), "post")

    db.add(post)

    return jsonify({
        "status": 200,
        "message": "successful",
        "data": {
            "post": post_schema(post)
        }
    })
