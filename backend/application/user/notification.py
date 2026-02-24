from flask import Blueprint, jsonify

from ..postgres import db_close, db_open
from ..storage import storage
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

    if "admin:manage_files" not in user["access"]:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "unauthorized access"
        })

    cur.execute("""SELECT photo FROM "user";""")
    users_photo = cur.fetchall()
    users_photo = [x["photo"] for x in users_photo if x["photo"]]
    user_store_photo = storage.get_all("user")
    if '.emptyFolderPlaceholder' in user_store_photo:
        user_store_photo.remove('.emptyFolderPlaceholder')
    cur.execute("""
        SELECT COUNT(*) FROM "user"
        WHERE photo IS NOT NULL AND photo <> ALL(%s);
    """, (user_store_photo,))
    users_with_missing_photo = cur.fetchone()["count"]
    unused_user_photo = len(set(user_store_photo) - set(users_photo))

    cur.execute("""SELECT photo, files FROM post;""")
    temp = cur.fetchall()
    posts_photo = []
    for x in temp:
        if x["photo"]:
            posts_photo.append(x["photo"])
        posts_photo += x["files"]
    post_store_photo = storage.get_all("post")
    if '.emptyFolderPlaceholder' in post_store_photo:
        post_store_photo
    cur.execute("""
        SELECT COUNT(*) FROM post
        WHERE NOT %s @> files OR
        photo IS NOT NULL AND photo <> ALL(%s);
    """, (post_store_photo, post_store_photo))
    posts_with_missing_photo = cur.fetchone()["count"]
    unused_post_photo = len(set(post_store_photo) - set(posts_photo))

    nots = []
    if users_with_missing_photo > 0:
        nots.append({
            "type": 'missing user photo',
            "count": users_with_missing_photo,
            "slug": "/admin/file_error"
        })

    if unused_user_photo > 0:
        nots.append({
            "type": 'unused user photo',
            "count": unused_user_photo,
            "slug": "/admin/file_error"
        })

    if posts_with_missing_photo > 0:
        nots.append({
            "type": 'missing post photo',
            "count": posts_with_missing_photo,
            "slug": "/admin/file_error"
        })

    if unused_post_photo > 0:
        nots.append({
            "type": 'unused post photo',
            "count": unused_post_photo,
            "slug": "/admin/file_error"
        })

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "nots": nots
    })
