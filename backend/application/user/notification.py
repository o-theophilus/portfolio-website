from flask import Blueprint, jsonify
from ..tools import get_session
from ..postgres import db_open, db_close
from ..storage import storage


bp = Blueprint("notification", __name__)


@bp.get("/notification")
def notification():
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

    unused_photos = [x for x in all_stored_files if x not in all_used_files]

    nots = []
    if unused_photos != []:
        nots.append({
            "type": 'unused_files',
            "count": len(unused_photos),
            "slug": "/admin/file_error"
        })

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "nots": nots
    })
