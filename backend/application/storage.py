from flask import Blueprint, send_file
from deta import Deta
from PIL import Image, ImageOps
from io import BytesIO
from uuid import uuid4
import os
from werkzeug.datastructures import FileStorage


bp = Blueprint("storage", __name__)


def drive():
    name = "live"
    return Deta(os.environ["DETA_KEY"]).Drive(name)


def storage(
    x=None,
    folder="post",
    delete=False,
    thumbnail=False,
):
    if type(x) is str:
        if delete:
            return drive().delete(f"{folder}/{x}")

        photo = drive().get(f"{folder}/{x}")
        photo = Image.open(BytesIO(photo.read()))
        if thumbnail:
            size = int(thumbnail)
            photo = ImageOps.fit(photo, (size, size), Image.LANCZOS)
        file_io = BytesIO()
        photo.save(file_io, format="JPEG")
        file_io.seek(0)

        return file_io

    if isinstance(x, FileStorage):
        photo = Image.open(x).convert('RGBA')
        white = Image.new('RGBA', photo.size, (255, 255, 255))
        photo = Image.alpha_composite(white, photo).convert('RGB')

        if thumbnail:
            photo.thumbnail((1024, 1024), Image.LANCZOS)

        file_io = BytesIO()
        photo.save(file_io, format="JPEG")

        name = f"{uuid4().hex}_{photo.size[0]}x{photo.size[1]}.jpg"
        drive().put(f"{folder}/{name}", file_io.getvalue())

        return name


@bp.get("/photo/<key>")
@bp.get("/photo/<key>/<thumbnail>")
def get_photo(key, thumbnail=False):
    photo = storage(key, thumbnail=thumbnail)
    return send_file(photo, mimetype="image/jpg")
