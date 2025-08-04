from flask import Blueprint, send_file, current_app, Response
from PIL import Image, ImageOps
from io import BytesIO
from uuid import uuid4
import os
import PyPDF2
from supabase import create_client


bp = Blueprint("storage", __name__)


def drive():
    sb = create_client(os.environ["STORE_URI"], os.environ["STORE_KEY"])
    return sb.storage.from_('portfolio.website')


def save_test_photo(x, path):
    photo = Image.open(x).convert('RGBA')
    white = Image.new('RGBA', photo.size, (255, 255, 255))
    photo = Image.alpha_composite(white, photo).convert('RGB')

    name = f"{uuid4().hex}_{photo.size[0]}x{photo.size[1]}.jpg"
    photo.save(f"{path}{name}")

    return name


def save_test_file(x, path):
    reader = PyPDF2.PdfReader(x)
    writer = PyPDF2.PdfWriter()

    height = 0
    width = 0
    for i in reader.pages:
        writer.add_page(i)
        height += i.mediabox.height
        if i.mediabox.width > width:
            width = i.mediabox.width

    dim = f"{width}x{height}x{len(reader.pages)}"
    name = f"{uuid4().hex}_{dim}.pdf"

    with open(f"{path}{name}", "wb") as f:
        writer.write(f)
    return name


def get_test_photo(x, path, thumbnail):
    photo = Image.open(f"{path}{x}")
    if thumbnail:
        size = int(thumbnail)
        photo = ImageOps.fit(photo, (size, size), Image.LANCZOS)
    file_io = BytesIO()
    photo.save(file_io, format="JPEG")
    file_io.seek(0)

    return file_io


def get_test_file(x, path):
    file = None
    with open(f"{path}{x}", 'rb') as f:
        file = f.read()
    return file


def delete_test(x, path):
    if os.path.exists(f"{path}{x}"):
        os.remove(f"{path}{x}")
        return True
    return False


def save_live_photo(x, path):
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


def save_live_file(x, path):
    reader = PyPDF2.PdfReader(x)
    writer = PyPDF2.PdfWriter()

    height = 0
    width = 0
    for i in reader.pages:
        writer.add_page(i)
        height += i.mediabox.height
        if i.mediabox.width > width:
            width = i.mediabox.width

    dim = f"{width}x{height}x{len(reader.pages)}"
    name = f"{uuid4().hex}_{dim}.pdf"

    b = BytesIO()
    writer.write(b)

    drive().upload(
        f"{path}{name}",
        b.getvalue(),
        {'content-type': 'application/pdf'}
    )

    return name


def get_live_photo(x, path, thumbnail):
    photo = drive().download(f"{path}{x}")
    photo = Image.open(BytesIO(photo))

    if thumbnail:
        size = int(thumbnail)
        photo = ImageOps.fit(photo, (size, size), Image.LANCZOS)

    file_io = BytesIO()
    photo.save(file_io, format="JPEG")
    file_io.seek(0)

    return file_io


def get_live_file(x, path):
    file = drive().download(f"{path}{x}")
    return BytesIO(file)


def delete_live(x, path):
    return drive().remove([f"{path}{x}"])


def storage(method, x, thumbnail=False, path=""):
    test = False
    if current_app.config["DEBUG"]:
        folder = f"{os.getcwd()}/static/{path}"
        os.makedirs(folder, exist_ok=True)
        test = True

    if method == "save":
        if x.content_type in ['image/jpeg', 'image/png']:
            if test:
                return save_test_photo(x, path)
            else:
                return save_live_photo(x, path)
        else:
            if test:
                return save_test_file(x, path)
            else:
                return save_live_file(x, path)

    elif method == "get":
        if x[-4:] == ".jpg":
            if test:
                return get_test_photo(x, path, thumbnail)
            else:
                return get_live_photo(x, path, thumbnail)
        else:
            if test:
                return get_test_file(x, path)
            else:
                return get_live_file(x, path)

    elif method == "delete":
        if test:
            return delete_test(x, path)
        else:
            return delete_live(x, path)


@bp.get("/file/<filename>")
@bp.get("/file/<filename>/<thumbnail>")
def get_photo(filename, thumbnail=False):
    file = storage("get", filename, thumbnail=thumbnail)

    if filename[-4:] == ".jpg":
        return send_file(file, mimetype="image/jpg")
    else:
        return Response(file, mimetype='application/pdf')
