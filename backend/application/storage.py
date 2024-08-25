from flask import Blueprint, send_file, current_app
from deta import Deta
from PIL import Image, ImageOps
from io import BytesIO
from uuid import uuid4
import os


bp = Blueprint("storage", __name__)


def drive():
    return Deta(os.environ["DETA_KEY"]).Drive("live")


def save_live(x, folder, thumbnail):
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


def save_test(x, folder, thumbnail):
    photo = Image.open(x).convert('RGBA')
    white = Image.new('RGBA', photo.size, (255, 255, 255))
    photo = Image.alpha_composite(white, photo).convert('RGB')

    if thumbnail:
        photo.thumbnail((1024, 1024), Image.LANCZOS)

    name = f"{uuid4().hex}_{photo.size[0]}x{photo.size[1]}.jpg"
    photo.save(f"{folder}/{name}")

    return name


def get_live(x, folder, thumbnail):
    photo = drive().get(f"{folder}/{x}")
    photo = Image.open(BytesIO(photo.read()))
    if thumbnail:
        size = int(thumbnail)
        photo = ImageOps.fit(photo, (size, size), Image.LANCZOS)
    file_io = BytesIO()
    photo.save(file_io, format="JPEG")
    file_io.seek(0)

    return file_io


def get_test(x, folder, thumbnail):
    photo = Image.open(f"{folder}/{x}")
    if thumbnail:
        size = int(thumbnail)
        photo = ImageOps.fit(photo, (size, size), Image.LANCZOS)
    file_io = BytesIO()
    photo.save(file_io, format="JPEG")
    file_io.seek(0)

    return file_io


def delete_live(x, folder):
    return drive().delete(f"{folder}/{x}")


def delete_test(x, folder):
    if os.path.exists(f"{folder}/{x}"):
        os.remove(f"{folder}/{x}")
        return True
    return False


def storage(method, x, thumbnail=False, folder="post"):
    test = False
    if current_app.config["DEBUG"]:
        folder = f"{os.getcwd()}/static/{folder}"
        os.makedirs(folder, exist_ok=True)
        test = True

    if method == "save" and test:
        return save_test(x, folder, thumbnail)
    elif method == "save":
        return save_live(x, folder, thumbnail)
    elif method == "get" and test:
        return get_test(x, folder, thumbnail)
    elif method == "get":
        return get_live(x, folder, thumbnail)
    elif method == "delete" and test:
        return delete_test(x, folder)
    elif method == "delete":
        return delete_live(x, folder)


@bp.get("/photo/<key>")
@bp.get("/photo/<key>/<thumbnail>")
def get_photo(key, thumbnail=False):
    photo = storage("get", key, thumbnail=thumbnail)
    return send_file(photo, mimetype="image/jpg")
