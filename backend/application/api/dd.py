from flask import current_app
from deta import Deta
from PIL import Image
from io import BytesIO
from uuid import uuid4


def drive():
    name = "live"
    # if current_app.config["DEBUG"]:
    #     name = "test"
    return Deta(current_app.config["DETA_KEY"]).Drive(name)


def add(photo, path, compress=False):
    file = BytesIO()

    if compress:
        photo = Image.open(photo).convert('RGBA')
        white = Image.new('RGBA', photo.size, (255, 255, 255))
        photo = Image.alpha_composite(white, photo).convert('RGB')
        # photo = ImageOps.fit(photo, (width, height), Image.ANTIALIAS)
        photo.thumbnail((500, 500), Image.Resampling.LANCZOS)

        photo.save(file, format="JPEG")
    else:
        photo.save(file)

    name = f"{uuid4().hex}.jpg"
    drive().put(f"/{path}/{name}", file.getvalue())

    return name


def rem(name, path=""):
    return drive().delete(f"/{path}/{name}")


def get(name, path):
    return drive().get(f"/{path}/{name}")
