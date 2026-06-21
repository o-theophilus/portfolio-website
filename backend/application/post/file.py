from flask import Blueprint, request

from ..storage import storage
from ..tools import log, rate_limit, session
from .get import post_schema

bp = Blueprint("post_file", __name__)


@bp.post("/posts/<key>/file")
@session(True)
@rate_limit(20, 1)
@log("post")
def add_file(cur, user, key):
    if "post.edit_files" not in user["access"]:
        return {
            "status": 403,
            "error": "unauthorized access"
        }, 403

    cur.execute('SELECT * FROM post WHERE key = %s;', (key,))
    post = cur.fetchone()
    if not post:
        return {
            "status": 404,
            "error": "Invalid request"
        }, 404

    if 'files' not in request.files:
        return {
            "status": 422,
            "error": "Invalid request"
        }, 422

    error = ""
    files = []

    for x in request.files.getlist("files"):
        err = ""
        if x.content_type not in [
                'image/jpeg', 'image/png', 'application/pdf']:
            err = f"{x.filename} => invalid file"
        elif len(post["files"]) + len(
                files) >= post["content"].count("@[file]"):
            err = f"{x.filename} => excess file"

        if err:
            error = f"{error}, {err}" if error else err
        else:
            files.append(x)

    if files == []:
        if not error:
            error = "no file"
        return {
            "status": 422,
            "error": error
        }, 422

    file_names = []
    for x in files:
        filename = storage.save(x, "post")
        file_names.append(filename)

    cur.execute("""
        UPDATE post
        SET files = %s
        WHERE key = %s
        RETURNING *;
    """, (
        post["files"] + file_names,
        post["key"]
    ))
    post = cur.fetchone()

    return {
        "status": 200,
        "post": post_schema(post),
        "error": error,
        "log": {
            "entity_key": post["key"],
            "misc": {
                "added": ", ".join(file_names),
                "error": error
            }
        }
    }, 200


@bp.put("/posts/<key>/file")
@session(True)
@rate_limit(10, 1)
@log("post")
def order_delete_file(cur, user, key):
    if "post.edit_files" not in user["access"]:
        return {
            "status": 403,
            "error": "unauthorized access"
        }, 403

    cur.execute('SELECT * FROM post WHERE key = %s;', (key,))
    post = cur.fetchone()
    if not post:
        return {
            "status": 404,
            "error": "Invalid request"
        }, 404

    files = request.json.get("files")
    if not files or type(files) is not list:
        return {
            "status": 422,
            "error": "Invalid request"
        }, 422

    files = [p.split("/")[-1] for p in files]

    if not all(x in post["files"] for x in files):
        return {
            "status": 422,
            "error": "Invalid request"
        }, 422

    for x in post["files"]:
        if x not in files:
            storage.delete(x, "post")

    cur.execute("""
        UPDATE post
        SET files = %s
        WHERE key = %s
        RETURNING *;
    """, (
        files,
        post["key"]
    ))
    post = cur.fetchone()

    return {
        "status": 200,
        "post": post_schema(post),
        "log": {
            "entity_key": post["key"],
            "misc": {
                "from": post["files"],
                "to": files
            }
        }
    }, 200
