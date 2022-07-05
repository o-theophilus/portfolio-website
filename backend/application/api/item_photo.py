from flask import Blueprint, jsonify, request
from .tools import token_to_user
from .photo import upload, remove
from .detabase import get_db, db_add, db_get

bp = Blueprint("item_photo", __name__)


@bp.post("/photo_item/<key>")
def post_item(key):
    db = get_db()

    user = token_to_user(db)
    if not user:
        return jsonify({
            "status": 101,
            "message": "invalid token"
        })

    if 'file' not in request.files or 'id' not in request.form:
        return jsonify({
            "status": 401,
            "message": "invalid request"
        })

    file = request.files["file"]

    ext = file.filename.split(".")[-1]
    if ext.lower() not in ['jpg', 'png', 'gif']:
        return jsonify({
            "status": 201,
            "message": "invalid file type"
        })

    item = db_get(db, "item", "key", key)
    if not item:
        return jsonify({
            "status": 401,
            "message": "invalid request"
        })

    photo = {
        "key": upload(file, "item"),
        "order": len(item["photos"]),
    }

    if len(item["photos"]) == 10:
        return jsonify({
            "status": 201,
            "message": "max image reached"
        })
    item["photos"].append(photo)

    item = db_add(item)

    return jsonify({
        "status": 200,
        "message": "successful",
        "data": {
            "item": item
        }
    })


@bp.put("/photo_item/<key>")
def rearrange(key):
    db = get_db()

    user = token_to_user(db)
    if not user:
        return jsonify({
            "status": 101,
            "message": "invalid token"
        })

    if "photos" not in request.json or not request.json["photos"]:
        return jsonify({
            "status": 401,
            "message": "invalid request"
        })

    item = db_get(db, "item", "key", key)
    if not item:
        return jsonify({
            "status": 401,
            "message": "invalid request"
        })

    photo_keys = request.json["photos"]
    photo_keys = [key.split("/")[-1] for key in photo_keys]

    for photo in item["photos"]:
        photo["order"] = photo_keys.index(photo["key"])

    item = db_add(item)

    return jsonify({
        "status": 200,
        "message": "successful",
        "data": {
            "item": item
        }
    })


@bp.delete("/photo_item/<key>")
def delete(key):
    db = get_db()

    if (
        "active_photo" not in request.json
        or not request.json["active_photo"]
    ):
        return jsonify({
            "status": 401,
            "message": "invalid request"
        })

    item = db_get(db, "item", "key", key)
    if not item:
        return jsonify({
            "status": 401,
            "message": "invalid request"
        })

    temp = []
    i = 0

    active_photo = request.json["active_photo"].split("/")[-1]

    for photo in sorted(item["photos"], key=lambda d: d['order']):
        if photo["key"] != active_photo:
            photo["order"] = i
            i += 1
            temp.append(photo)

    remove(active_photo, "item")
    item["photos"] = temp
    item = db_add(item)

    return jsonify({
        "status": 200,
        "message": "successful",
        "data": {
            "item": item
        }
    })
