from flask import Blueprint, request, send_file
from .detabase import photo_drive
from PIL import Image, ImageOps
from io import BytesIO
from uuid import uuid4

bp = Blueprint("photo", __name__)


def upload(photo, type_, width=512, height=512):
    file_name = f"{uuid4().hex}.jpg"
    photo_byte = BytesIO()

    if type_ != "item":
        photo = Image.open(photo).convert('RGBA')
        white = Image.new('RGBA', photo.size, (255, 255, 255))
        photo = Image.alpha_composite(white, photo).convert('RGB')
        photo = ImageOps.fit(photo, (width, height), Image.ANTIALIAS)

        photo.save(photo_byte, format="JPEG")
    else:
        photo.save(photo_byte)

    photo_drive().put(f"{type_}/{file_name}", photo_byte.getvalue())
    return file_name


def remove(photo, type_):
    return photo_drive().delete(f"{type_}/{photo}")


def photo_url(photo, type_):
    return f"{request.host_url}photo/{type_}/{photo}"


@bp.get("/photo/<type_>/<photo>")
def get(type_, photo):

    thumbnail = False
    if type_ == "item_thumbnail":
        type_ = "item"
        thumbnail = True

    photo_file = photo_drive().get(f"{type_}/{photo}")

    if thumbnail:
        temp = Image.open(BytesIO(photo_file.read()))
        temp = ImageOps.fit(temp, (512, 512), Image.ANTIALIAS)

        photo_file = BytesIO()
        temp.save(photo_file, format="JPEG")
        photo_file.seek(0)

    return send_file(photo_file, mimetype="image/jpg")
