from flask import Blueprint, jsonify, request

from ..log import log
from ..storage import storage
from ..tools import rate_limit, session
from .get import post_schema

bp = Blueprint("post_file", __name__)


@bp.post("/posts/<key>/file")
@session(True)
@rate_limit(20, 1)
def add_file(cur, user, key):
    if "post.edit_files" not in user["access"]:
        return jsonify({
            "status": 403,
            "error": "unauthorized access"
        })

    cur.execute('SELECT * FROM post WHERE key = %s;', (key,))
    post = cur.fetchone()
    if 'files' not in request.files or not post:
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

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
        return jsonify({
            "status": 400,
            "error": error
        })

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

    log(
        cur=cur,
        user_key=user["key"],
        action="added file to post",
        entity_type="post",
        entity_key=post["key"],
        misc={
            "added": ", ".join(file_names),
            "error": error
        }
    )

    return jsonify({
        "status": 200,
        "post": post_schema(post),
        "error": error
    })


@bp.put("/posts/<key>/file")
@session(True)
@rate_limit(10, 1)
def order_delete_file(cur, user, key):
    if "post.edit_files" not in user["access"]:
        return jsonify({
            "status": 403,
            "error": "unauthorized access"
        })

    cur.execute('SELECT * FROM post WHERE key = %s;', (key,))
    post = cur.fetchone()

    files = request.json.get("files")

    if not post or not files or type(files) is not list:
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    files = [p.split("/")[-1] for p in files]

    if not all(x in post["files"] for x in files):
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    for x in post["files"]:
        if x not in files:
            storage.delete(x, "post")

    log(
        cur=cur,
        user_key=user["key"],
        action="edited post files",
        entity_type="post",
        entity_key=post["key"],
        misc={
            "from": post["files"],
            "to": files
        }
    )

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

    return jsonify({
        "status": 200,
        "post": post_schema(post)
    })
