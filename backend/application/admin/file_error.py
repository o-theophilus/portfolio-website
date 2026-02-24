from flask import Blueprint, jsonify, request

from ..log import log
from ..postgres import db_close, db_open
from ..storage import storage
from ..tools import get_session

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
    user_store_photo = storage.get_all("user")
    if '.emptyFolderPlaceholder' in user_store_photo:
        user_store_photo.remove('.emptyFolderPlaceholder')
    cur.execute("""
        SELECT username, name FROM "user"
        WHERE photo IS NOT NULL AND photo <> ALL(%s);
    """, (user_store_photo,))
    users_with_missing_photo = cur.fetchall()

    cur.execute("""SELECT photo, files FROM post;""")
    temp = cur.fetchall()
    posts_photo = []
    for x in temp:
        if x["photo"]:
            posts_photo.append(x["photo"])
        posts_photo += x["files"]
    post_store_photo = storage.get_all("post")
    if '.emptyFolderPlaceholder' in post_store_photo:
        post_store_photo.remove('.emptyFolderPlaceholder')
    cur.execute("""
        SELECT slug, title FROM post
        WHERE NOT ARRAY[%s] @> files OR
        photo IS NOT NULL AND photo <> ANY(%s);
    """, (post_store_photo, post_store_photo))
    posts_with_missing_photo = cur.fetchall()

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "unused_post_photo": [f"{request.host_url}photo/post/{x}"
                   for x in post_store_photo if x not in posts_photo],
        "unused_user_photo": [f"{request.host_url}photo/user/{x}"
                   for x in user_store_photo if x not in users_photo],
        "users": users_with_missing_photo,
        "posts": posts_with_missing_photo
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

    photos = request.json.get("photos")
    entity = request.json.get("entity")

    if (
        not photos or type(photos) is not list
        or not entity or entity not in ["user", "post"]
    ):
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    for x in photos:
        storage.delete(x.split("/")[-1], entity)

    log(
        cur=cur,
        user_key=user["key"],
        action="deleted unuded photo(s)",
        entity_key="app",
        entity_type="photo",
        misc={
            "photo(s)": photos,
            "from": entity
        }
    )

    db_close(con, cur)
    return jsonify({
        "status": 200
    })
