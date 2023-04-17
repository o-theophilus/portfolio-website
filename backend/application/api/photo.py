from flask import Blueprint, jsonify, request, send_file
from . import db, token_to_user, dd, post_schema
from PIL import Image, ImageOps
from io import BytesIO

bp = Blueprint("photo", __name__)


@bp.get("/photo/<name>")
@bp.get("/photo/<name>/<thumbnail>")
def get(name, thumbnail=None):
    photo = dd.get(name, "post")

    # if not photo:
    #     return jsonify({
    #         "status": 201,
    #         "message": "not found"
    #     })

    if thumbnail:
        temp = Image.open(BytesIO(photo.read()))
        temp = ImageOps.fit(temp, (512, 512), Image.ANTIALIAS)

        photo = BytesIO()
        temp.save(photo, format="JPEG")
        photo.seek(0)

    return send_file(photo, mimetype="image/jpg")


@bp.post("/blog/photo_many/<slug>")
@bp.post("/project/photo_many/<slug>")
def post_many(slug):
    data = db.data()

    user = token_to_user(data)
    if "admin" not in user["roles"]:
        return jsonify({
            "status": 102,
            "message": "unauthorised access"
        })

    post_type = f"{request.url_rule}"[1:].split("/")[0]

    if 'files' not in request.files or 'slug' not in request.form:
        return jsonify({
            "status": 401,
            "message": "invalid request"
        })

    files = request.files.getlist("files")

    for file in files:
        media, format = file.content_type.split("/")
        if media not in ["image", "video"] or format in ['svg+xml', 'x-icon']:
            return jsonify({
                "status": 201,
                "message": "invalid file type"
            })

    post = db.get(post_type, "slug", slug, data)
    if not post:
        return jsonify({
            "status": 401,
            "message": "invalid request"
        })

    count = post["content"].count("{#photo}") + 1
    if len(post["photos"]) + len(files) > count:
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

# @bp.post("/blog/photo/<slug>")
# @bp.post("/project/photo/<slug>")
# def post(slug):
#     data = db.data()

#     user = token_to_user(data)
#     if "admin" not in user["roles"]:
#         return jsonify({
#             "status": 102,
#             "message": "unauthorised access"
#         })

#     post_type = f"{request.url_rule}"[1:].split("/")[0]

#     if 'photo' not in request.files or 'slug' not in request.form:
#         return jsonify({
#             "status": 401,
#             "message": "invalid request"
#         })

#     photo = request.files["photo"]

#     ext = photo.filename.split(".")[-1]
#     if ext.lower() not in ['jpg', 'png', 'gif']:
#         return jsonify({
#             "status": 201,
#             "message": "invalid file type"
#         })

#     post = db.get(post_type, "slug", slug, data)
#     if not post:
#         return jsonify({
#             "status": 401,
#             "message": "invalid request"
#         })

#     count = post["content"].count("{#photo}")
#     if len(post["photos"]) > count:
#         return jsonify({
#             "status": 401,
#             "message": "invalid request"
#         })

#     photo_name = dd.add(photo, "post", True)
#     post["photos"].append(photo_name)

#     db.add(post)

#     return jsonify({
#         "status": 200,
#         "message": "successful",
#         "data": {
#             "post": post_schema(post)
#         }
#     })


@bp.put("/blog/photo/<slug>")
@bp.put("/project/photo/<slug>")
def arrange(slug):
    post_type = f"{request.url_rule}"[1:].split("/")[0]

    data = db.data()

    user = token_to_user(data)
    if "admin" not in user["roles"]:
        return jsonify({
            "status": 102,
            "message": "unauthorised access"
        })

    if "photos" not in request.json or not request.json["photos"]:
        return jsonify({
            "status": 401,
            "message": "invalid request"
        })

    post = db.get(post_type, "slug", slug, data)
    if not post:
        return jsonify({
            "status": 401,
            "message": "invalid request"
        })

    photos = [p.split("/")[-1] for p in request.json["photos"]]

    if set(post["photos"]) != set(photos):
        return jsonify({
            "status": 401,
            "message": "invalid request"
        })

    post["photos"] = photos
    db.add(post)

    return jsonify({
        "status": 200,
        "message": "successful",
        "data": {
            "post": post_schema(post)
        }
    })


@bp.delete("/blog/photo/<slug>")
@bp.delete("/project/photo/<slug>")
def delete(slug):
    post_type = f"{request.url_rule}"[1:].split("/")[0]

    data = db.data()

    user = token_to_user(data)
    if "admin" not in user["roles"]:
        return jsonify({
            "status": 102,
            "message": "unauthorised access"
        })

    if "active_photo" not in request.json or not request.json["active_photo"]:
        return jsonify({
            "status": 401,
            "message": "invalid request"
        })

    post = db.get(post_type, "slug", slug, data)
    if not post:
        return jsonify({
            "status": 401,
            "message": "invalid request"
        })

    ap = request.json["active_photo"]
    ap = ap.split("/")[-1]

    photos = [p for p in post["photos"] if p != ap]
    if len(photos) == len(post["photos"]):
        return jsonify({
            "status": 401,
            "message": "invalid request"
        })

    dd.rem(ap, "post")
    post["photos"] = photos
    db.add(post)

    return jsonify({
        "status": 200,
        "message": "successful",
        "data": {
            "post": post_schema(post)
        }
    })
