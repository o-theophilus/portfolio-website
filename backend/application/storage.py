import os
from io import BytesIO
from pathlib import Path
from uuid import uuid4

from flask import Blueprint, abort, send_file
from PIL import Image, ImageOps
from supabase import create_client

bp = Blueprint("storage", __name__)


def drive():
    sb = create_client(os.environ["STORE_URI"], os.environ["STORE_KEY"])
    return sb.storage.from_('portfolio.website')


def save_test(file, path=""):
    photo = Image.open(file).convert('RGBA')
    white = Image.new('RGBA', photo.size, (255, 255, 255))
    photo = Image.alpha_composite(white, photo).convert('RGB')

    filename = f"{uuid4().hex}_{photo.size[0]}x{photo.size[1]}.jpg"
    photo.save(f"static/{path}{filename}")

    return filename


def copy_test(filename, from_path="", to_path=""):
    try:
        photo = Image.open(f"static/{from_path}{filename}")
        photo.save(f"static/{to_path}{filename}")
    except Exception as e:
        abort(400, description=str(e))

    return f"{to_path}{filename}"


def delete_test(filename, path=""):
    if os.path.exists(f"{path}{filename}"):
        os.remove(f"static/{path}{filename}")
        return True
    return False


def get_test(filename, path="", thumbnail=False):
    try:
        photo = Image.open(f"static/{path}{filename}")
    except Exception as e:
        abort(400, description=str(e))

    if thumbnail:
        size = int(thumbnail)
        photo = ImageOps.fit(photo, (size, size), Image.LANCZOS)
    file_io = BytesIO()
    photo.save(file_io, format="JPEG")
    file_io.seek(0)

    return file_io


def get_all_test(path=""):
    folder_path = Path(f"{os.getcwd()}/static/{path}")
    file_names = [file.name for file in folder_path.iterdir()
                  if file.is_file()]
    return file_names


def save_live(file, path=""):
    photo = Image.open(file).convert('RGBA')
    white = Image.new('RGBA', photo.size, (255, 255, 255))
    photo = Image.alpha_composite(white, photo).convert('RGB')

    file_io = BytesIO()
    photo.save(file_io, format="JPEG")
    file_io.seek(0)

    filename = f"{uuid4().hex}_{photo.size[0]}x{photo.size[1]}.jpg"
    drive().upload(
        f"{path}{filename}",
        file_io.getvalue(),
        {'content-type': 'image/jpeg'}
    )

    return filename


def copy_live(filename, from_path="", to_path=""):
    try:
        drive().copy(f"{from_path}{filename}", f"{to_path}{filename}")
    except Exception as e:
        abort(400, description=str(e))

    return f"{to_path}{filename}"


def delete_live(filename, path=""):
    return drive().remove([f"{path}{filename}"])


def get_live(filename, path="", thumbnail=False):
    try:
        photo = drive().download(f"{path}{filename}")
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


def get_all_live(path=""):
    try:
        offset = 0
        limit = 100
        files = []

        while True:
            resp = drive().list(f"{path}", {"limit": limit, "offset": offset})
            files += resp
            offset += limit

            if len(resp) < limit:
                break

    except Exception as e:
        abort(400, description=str(e))
    return [x["name"] for x in files]


test = False


def get_path(path=""):
    if test:
        os.makedirs(f"{os.getcwd()}/static/{path}", exist_ok=True)
    return f"{path}/" if path and not path.endswith("/") else path


class storage:
    @staticmethod
    def save(file, path=""):
        if test:
            return save_test(file, get_path(path))
        else:
            return save_live(file, get_path(path))

    def copy(filename, path="", path2=""):
        if test:
            return copy_test(filename, get_path(path), get_path(path2))
        else:
            return copy_live(filename, get_path(path), get_path(path2))

    @staticmethod
    def delete(filename, path=""):
        if test:
            return delete_test(filename, get_path(path))
        else:
            return delete_live(filename, get_path(path))

    @staticmethod
    def get(filename, path="", thumbnail=False):
        if test:
            return get_test(filename, get_path(path), thumbnail)
        else:
            return get_live(filename, get_path(path), thumbnail)

    @staticmethod
    def get_all(path=""):
        if test:
            return get_all_test(get_path(path))
        else:
            return get_all_live(get_path(path))


@bp.get("/photo/<path>/<filename>")
@bp.get("/photo/<path>/<filename>/<thumbnail>")
def get_photo(filename, path="", thumbnail=False):
    try:
        file = storage.get(filename, path, thumbnail)
    except Exception as e:
        abort(400, description=str(e))
    return send_file(file, mimetype="image/jpg")
