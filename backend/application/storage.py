from flask import Blueprint, send_file, current_app, Response
from deta import Deta
from PIL import Image, ImageOps
from io import BytesIO
from uuid import uuid4
import os


bp = Blueprint("storage", __name__)


def drive():
    return Deta(os.environ["DETA_KEY"]).Drive("live")


def save_live_photo(x, folder):
    photo = Image.open(x).convert('RGBA')
    white = Image.new('RGBA', photo.size, (255, 255, 255))
    photo = Image.alpha_composite(white, photo).convert('RGB')

    file_io = BytesIO()
    photo.save(file_io, format="JPEG")

    name = f"{uuid4().hex}_{photo.size[0]}x{photo.size[1]}.jpg"
    drive().put(f"{folder}/{name}", file_io.getvalue())

    return name


def save_test_photo(x, folder):
    photo = Image.open(x).convert('RGBA')
    white = Image.new('RGBA', photo.size, (255, 255, 255))
    photo = Image.alpha_composite(white, photo).convert('RGB')

    name = f"{uuid4().hex}_{photo.size[0]}x{photo.size[1]}.jpg"
    photo.save(f"{folder}/{name}")

    return name


def save_live_file(x, folder):
    name = f"{uuid4().hex}.pdf"
    drive().put(f"{folder}/{name}", x)
    return name


def save_test_file(x, folder):
    name = f"{uuid4().hex}.pdf"
    with open(f"{folder}/{name}", "wb") as f:
        f.write(x.read())
    return name


def get_live_photo(x, folder, thumbnail):
    photo = drive().get(f"{folder}/{x}")
    photo = Image.open(BytesIO(photo.read()))
    if thumbnail:
        size = int(thumbnail)
        photo = ImageOps.fit(photo, (size, size), Image.LANCZOS)
    file_io = BytesIO()
    photo.save(file_io, format="JPEG")
    file_io.seek(0)

    return file_io


def get_test_photo(x, folder, thumbnail):
    photo = Image.open(f"{folder}/{x}")
    if thumbnail:
        size = int(thumbnail)
        photo = ImageOps.fit(photo, (size, size), Image.LANCZOS)
    file_io = BytesIO()
    photo.save(file_io, format="JPEG")
    file_io.seek(0)

    return file_io


def get_live_file(x, folder):
    file = drive().get(f"{folder}/{x}")
    return BytesIO(file.read())


def get_test_file(x, folder):
    file = None
    with open(f"{folder}/{x}", 'rb') as f:
        file = f.read()
    return file


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

    if method == "save":
        if x.content_type in ['image/jpeg', 'image/png']:
            if test:
                return save_test_photo(x, folder)
            else:
                return save_live_photo(x, folder)
        else:
            if test:
                return save_test_file(x, folder)
            else:
                return save_live_file(x, folder)

    elif method == "get":
        if x[-4:] == ".jpg":
            if test:
                return get_test_photo(x, folder, thumbnail)
            else:
                return get_live_photo(x, folder, thumbnail)
        else:
            if test:
                return get_test_file(x, folder)
            else:
                return get_live_file(x, folder)

    elif method == "delete":
        if test:
            return delete_test(x, folder)
        else:
            return delete_live(x, folder)


@bp.get("/file/<filename>")
@bp.get("/file/<filename>/<thumbnail>")
def get_photo(filename, thumbnail=False):
    file = storage("get", filename, thumbnail=thumbnail)

    if filename[-4:] == ".jpg":
        return send_file(file, mimetype="image/jpg")
    else:
        return Response(file, mimetype='application/pdf')
