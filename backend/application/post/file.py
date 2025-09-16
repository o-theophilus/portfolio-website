from flask import Blueprint, jsonify, request
from ..tools import get_session
from ..postgres import db_open, db_close
from ..storage import storage
from ..log import log
from .get import post_schema

bp = Blueprint("post_file", __name__)


@bp.post("/post/file/<key>")
def add_file(key):
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    if "post:edit_files" not in user["access"]:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "unauthorized access"
        })

    cur.execute('SELECT * FROM post WHERE key = %s;', (key,))
    post = cur.fetchone()
    if 'files' not in request.files or not post:
        db_close(con, cur)
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
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": error
        })

    file_names = []
    for x in files:
        filename = storage("save", x)
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
        action="added_file",
        entity_key=post["key"],
        entity_type="post",
        misc={
            "added": ", ".join(file_names),
            "error": error
        }
    )

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "item": post_schema(post),
        "error": error
    })


@bp.put("/post/file/<key>")
def order_delete_file(key):
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    if "post:edit_files" not in user["access"]:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "unauthorized access"
        })

    cur.execute('SELECT * FROM post WHERE key = %s;', (key,))
    post = cur.fetchone()

    files = request.json.get("files")

    if not post or not files or type(files) is not list:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    files = [p.split("/")[-1] for p in files]

    if not all(x in post["files"] for x in files):
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    for x in post["files"]:
        if x not in files:
            storage("delete", x)

    log(
        cur=cur,
        user_key=user["key"],
        action="edited_files",
        entity_key=post["key"],
        entity_type="post",
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

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "item": post_schema(post)
    })
