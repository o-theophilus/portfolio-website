from flask import Blueprint, jsonify

from ..api.file_error import get_file_error
from ..postgres import db_close, db_open
from ..tools import get_session

bp = Blueprint("notification", __name__)


@bp.get("/notification")
def notification():
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    nots = []
    if "admin.manage_files" in user["access"]:
        file_error = get_file_error(cur).json

        if "unused_post_photo" in file_error and file_error[
                "unused_post_photo"]:
            nots.append({
                "type": 'unused post photo',
                "count": len(file_error["unused_post_photo"]),
                "slug": "/admin/file_error"
            })

        if "unused_user_photo" in file_error and file_error[
                "unused_user_photo"]:
            nots.append({
                "type": 'unused user photo',
                "count": len(file_error["unused_user_photo"]),
                "slug": "/admin/file_error"
            })

        if "posts" in file_error and file_error["posts"]:
            nots.append({
                "type": 'missing post photo',
                "count": len(file_error["posts"]),
                "slug": "/admin/file_error"
            })

        if "users" in file_error and file_error["users"]:
            nots.append({
                "type": 'missing user photo',
                "count": len(file_error["users"]),
                "slug": "/admin/file_error"
            })

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "nots": nots
    })
