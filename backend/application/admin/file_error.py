from flask import Blueprint, jsonify, request
from ..postgres import db_open, db_close
from ..log import log
from ..tools import get_session
from ..storage import storage


bp = Blueprint("file_error", __name__)


@bp.get("/file_error")
def get_file_error():
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    if "admin:manage_files" not in user["access"]:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "unauthorized access"
        })

    cur.execute("""SELECT photo FROM "user";""")
    users_photo = cur.fetchall()
    users_photo = [x["photo"] for x in users_photo if x["photo"]]

    cur.execute("""SELECT photo, files FROM post;""")
    temp = cur.fetchall()
    posts_files = []
    for x in temp:
        posts_files.append(x["photo"])
        if x["files"] != []:
            posts_files += x["files"]

    all_used_files = users_photo + posts_files
    all_stored_files = storage("get_all")

    cur.execute("""
        SELECT username, name
        FROM "user"
        WHERE
            photo IS NOT NULL
            AND NOT photo = ANY(%s);
    """, (all_stored_files,))
    _users = cur.fetchall()

    cur.execute("""
        SELECT slug, title
        FROM post
        WHERE
            photo IS NOT NULL
            AND NOT photo = ANY(%s)
            OR NOT ARRAY[%s] @> files;
    """, (all_stored_files, all_stored_files))
    _posts = cur.fetchall()

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "unused": [f"{request.host_url}file/{x}"
                   for x in all_stored_files if x not in all_used_files],
        "users": _users,
        "posts": _posts
    })


@bp.delete("/file_error")
def delete_file():
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    if "admin:manage_files" not in user["access"]:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "unauthorized access"
        })

    files = request.json.get("files")

    if not files or type(files) is not list:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    for x in files:
        storage("delete", x.split("/")[-1])

    log(
        cur=cur,
        user_key=user["key"],
        action="deleted",
        entity_key="app",
        entity_type="file",
        misc={
            "file(s)": files
        }
    )

    db_close(con, cur)
    return jsonify({
        "status": 200
    })
