from flask import current_app
from deta import Deta
from PIL import Image
from io import BytesIO
from uuid import uuid4
# from os.path import splitext


def drive():
    name = "live"
    if current_app.config["DEBUG"]:
        name = "test"
    return Deta(current_app.config["DETA_KEY"]).Drive(name)


def add(file, path="", compress=False):
    file_byte = BytesIO()

    is_image = file.content_type.split("/")[0] == "image"
    ext = "jpg" if is_image else file.filename.split(".")[-1]
    name = f"{uuid4().hex}.{ext}"

    if is_image and compress:
        file = Image.open(file).convert('RGBA')
        white = Image.new('RGBA', file.size, (255, 255, 255))
        file = Image.alpha_composite(white, file).convert('RGB')
        file.thumbnail((1024, 1024), Image.Resampling.LANCZOS)

        file.save(file_byte, format="JPEG")

    else:
        file.save(file_byte)

    drive().put(f"/{path}/{name}", file_byte.getvalue())
    return name


def rem(name, path=""):
    return drive().delete(f"/{path}/{name}")


def get(name, path=""):
    return drive().get(f"/{path}/{name}")
