from flask import Blueprint, send_file, current_app, abort
from PIL import Image, ImageOps
from io import BytesIO
from uuid import uuid4
import os
from supabase import create_client
from pathlib import Path


bp = Blueprint("storage", __name__)


def drive():
    sb = create_client(os.environ["STORE_URI"], os.environ["STORE_KEY"])
    return sb.storage.from_('portfolio.website')


def save_test(x, path):
    photo = Image.open(x).convert('RGBA')
    white = Image.new('RGBA', photo.size, (255, 255, 255))
    photo = Image.alpha_composite(white, photo).convert('RGB')

    name = f"{uuid4().hex}_{photo.size[0]}x{photo.size[1]}.jpg"
    photo.save(f"{path}/{name}")

    return name


def get_test(x, path, thumbnail):
    try:
        photo = Image.open(f"{path}/{x}")
    except Exception as e:
        abort(400, description=str(e))

    if thumbnail:
        size = int(thumbnail)
        photo = ImageOps.fit(photo, (size, size), Image.LANCZOS)
    file_io = BytesIO()
    photo.save(file_io, format="JPEG")
    file_io.seek(0)

    return file_io


def get_all_test(path):
    folder_path = Path(f"{os.getcwd()}/{path}")
    file_names = [file.name for file in folder_path.iterdir()
                  if file.is_file()]
    return file_names


def delete_test(x, path):
    if os.path.exists(f"{path}/{x}"):
        os.remove(f"{path}/{x}")
        return True
    return False


def save(x, path):
    photo = Image.open(x).convert('RGBA')
    white = Image.new('RGBA', photo.size, (255, 255, 255))
    photo = Image.alpha_composite(white, photo).convert('RGB')

    file_io = BytesIO()
    photo.save(file_io, format="JPEG")
    file_io.seek(0)

    name = f"{uuid4().hex}_{photo.size[0]}x{photo.size[1]}.jpg"
    drive().upload(
        f"{path}{name}",
        file_io.getvalue(),
        {'content-type': 'image/jpeg'}
    )

    return name


def get(x, path, thumbnail):
    try:
        photo = drive().download(f"{path}{x}")
    except Exception as e:
        abort(400, description=str(e))

    photo = Image.open(BytesIO(photo))

    if thumbnail:
        size = int(thumbnail)
        photo = ImageOps.fit(photo, (size, size), Image.LANCZOS)

    file_io = BytesIO()
    photo.save(file_io, format="JPEG")
    file_io.seek(0)

    return file_io


def get_all(path):
    try:
        files = drive().list(path)
    except Exception as e:
        abort(400, description=str(e))
    return [x["name"] for x in files]


def delete(x, path):
    return drive().remove([f"{path}{x}"])


def storage(method, x=None, path="", thumbnail=False):
    test = current_app.config["DEBUG"]
    if test:
        path = "static/post"
        os.makedirs(f"{os.getcwd()}/{path}", exist_ok=True)
    # test = False

    defs = {
        "save": {
            True: save_test,
            False: save,
        },
        "get": {
            True: lambda x, path: get_test(x, path, thumbnail),
            False: lambda x, path: get(x, path, thumbnail),
        },
        "get_all": {
            True: lambda x, path: get_all_test(path),
            False: lambda x, path: get_all(path),
        },
        "delete": {
            True: delete_test,
            False: delete,
        }
    }

    try:
        return defs[method][test](x, path)
    except Exception as e:
        abort(400, description=str(e))


@bp.get("/file/<x>")
@bp.get("/file/<x>/<thumbnail>")
def get_photo(x, thumbnail=False):
    try:
        file = storage("get", x, thumbnail=thumbnail)
    except Exception as e:
        abort(400, description=str(e))
    return send_file(file, mimetype="image/jpg")
