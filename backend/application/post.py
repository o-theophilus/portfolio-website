from flask import Blueprint, jsonify, request
from .tools import reserved_words, token_to_user
import re
import os
from uuid import uuid4
from .postgres import db_open, db_close
from .storage import storage
from .log import log
from .post_get import get_post, get_all
from datetime import datetime

bp = Blueprint("post", __name__)


@bp.post("/post")
def add():
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    if "post:add" not in user["access"]:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "unauthorized access"
        })

    if "title" not in request.json or not request.json["title"]:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "cannot be empty"
        })

    slug = re.sub('-+', '-', re.sub(
        '[^a-zA-Z0-9]', '-', request.json["title"].lower()))
    cur.execute('SELECT * FROM post WHERE slug = %s;', (slug,))
    post = cur.fetchone()
    if post or slug in reserved_words:
        slug = f"{slug}-{str(uuid4().hex)[:10]}"

    cur.execute("""
        SELECT key FROM "user" WHERE email = %s;
    """, (os.environ["MAIL_USERNAME"],))
    author = cur.fetchone()

    cur.execute("""
            INSERT INTO post (key, author_key, title, slug, date)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING *;
        """, (
        uuid4().hex,
        author["key"] if author else None,
        request.json["title"],
        slug,
        datetime.now()
    ))
    post = cur.fetchone()
    post["ratings"] = []

    log(
        cur=cur,
        user_key=user["key"],
        action="created",
        entity_key=post["key"],
        entity_type="post"
    )

    posts = get_all(cur=cur)

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "post": post,
        "posts": posts.json["posts"],
        "total_page": posts.json["total_page"]
    })


@bp.put("/post/<key>")
def edit(key):
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    cur.execute('SELECT * FROM post WHERE key = %s;', (key,))
    post = cur.fetchone()
    if not post:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    error = {}

    if "title" in request.json:
        if "post:edit_title" not in user["access"]:
            error["title"] = "unauthorized access"
        elif not request.json["title"]:
            error["title"] = "cannot be empty"
        elif request.json["title"] == post["title"]:
            error["title"] = "no change"
        else:
            slug = re.sub('-+', '-', re.sub(
                '[^a-zA-Z0-9]', '-', request.json["title"].lower()))
            cur.execute('SELECT * FROM post WHERE key != %s AND slug = %s;',
                        (post["key"], slug))
            slug_in_use = cur.fetchone()
            if (slug_in_use or slug in reserved_words):
                slug = f"{slug}-{str(uuid4().hex)[:10]}"

            cur.execute("""
                    UPDATE post
                    SET title = %s, slug = %s
                    WHERE key = %s;
                """, (
                request.json["title"],
                slug,
                post["key"]
            ))

    if "date" in request.json:
        if "post:edit_date" not in user["access"]:
            error["date"] = "unauthorized access"
        else:
            try:
                datetime.strptime(
                    f"{request.json['date']}",
                    "%Y-%m-%dT%H:%M:%S"
                )
            except Exception:
                error["date"] = "invalid request"

            cur.execute("""
                UPDATE post
                SET date = %s
                WHERE key = %s;
            """, (
                request.json['date'],
                post["key"]
            ))

    if "description" in request.json:
        if "post:edit_description" not in user["access"]:
            error["description"] = "unauthorized access"
        elif request.json["description"] == post["description"]:
            error["description"] = "no change"
        else:
            cur.execute("UPDATE post SET description = %s WHERE key = %s;", (
                request.json["description"], post["key"]))

    if "content" in request.json:
        if "post:edit_content" not in user["access"]:
            error["content"] = "unauthorized access"
        elif request.json["content"] == post["content"]:
            error["content"] = "no change"
        else:
            cur.execute("UPDATE post SET content = %s WHERE key = %s;", (
                request.json["content"], post["key"]))

    if "tags" in request.json:
        if "post:edit_tags" not in user["access"]:
            error["tags"] = "unauthorized access"
        elif type(request.json["tags"]) is not list:
            error["tags"] = "cannot be empty"
        elif set(request.json["tags"]) == set(post["tags"]):
            error["tags"] = "no change"
        else:
            cur.execute("""
                    UPDATE post
                    SET tags = %s
                    WHERE key = %s;
                """, (
                request.json["tags"],
                post["key"]
            ))

    if "author_email" in request.json:
        if "post:edit_author" not in user["access"]:
            error["author_email"] = "unauthorized access"
        elif not request.json["author_email"]:
            error["author_email"] = "cannot be empty"
        elif (
            not re.match(r"\S+@\S+\.\S+", request.json["author_email"])
            and request.json["author_email"] != "default"
        ):
            error["author_email"] = "Please enter a valid email"
        else:
            cur.execute("""
                SELECT key FROM "user" WHERE email = %s;
            """, (os.environ["MAIL_USERNAME"]
                  if request.json["author_email"] == "default" else
                  request.json["author_email"],))
            author = cur.fetchone()

            if not author:
                error["author_email"] = "no user found"
            elif author["key"] == post["author_key"]:
                error["author_email"] = "no change"
            else:
                cur.execute("""
                    UPDATE post SET author_key = %s WHERE key = %s
                ;""", (
                    author["key"], post["key"]
                ))

    if "status" in request.json:
        if "post:edit_status" not in user["access"]:
            error["status"] = "unauthorized access"
        elif (
            not request.json["status"]
            or request.json["status"] not in ['active', 'draft', 'delete']
        ):
            error["status"] = "invalid request"
        elif request.json["status"] == post["status"]:
            error["status"] = "no change"
        elif request.json["status"] == "active" and len(post["photos"]) == 0:
            error["status"] = "add photo"
        elif request.json["status"] == "active" and not post["content"]:
            error["status"] = "no content"
        else:
            cur.execute("""
                    UPDATE post
                    SET status = %s
                    WHERE key = %s;
                """, (
                request.json["status"],
                post["key"]
            ))

    if error != {}:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            **error
        })

    post = get_post(key, cur).json["post"]

    log(
        cur=cur,
        user_key=user["key"],
        action="edited",
        entity_key=post["key"],
        entity_type="post",
        misc=request.json
    )

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "post": post
    })


@bp.post("/post/photo/<key>")
def add_photos(key):
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    if "post:edit_photos" not in user["access"]:
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
            "error": "invalid request"
        })

    error = ""
    files = []
    _req = post["content"].count("{#photo}") + 1 - len(post["photos"])

    for x in request.files.getlist("files"):
        media, format = x.content_type.split("/")

        err = ""
        if media != "image" or format in ['svg+xml', 'x-icon']:
            err = f"{x.filename} => invalid file"
        elif _req - len(files) < 1:
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
            SET photos = %s
            WHERE key = %s;
        """, (
        post["photos"] + file_names,
        post["key"]
    ))

    post = get_post(key, cur).json["post"]

    log(
        cur=cur,
        user_key=user["key"],
        action="added_photo",
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
        "post": post,
        "error": error
    })


@bp.post("/post/file/<key>")
def add_file(key):
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

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
            "error": "invalid request"
        })

    error = ""
    files = []
    _req = post["content"].count("{#file}") + 1 - len(post["files"])

    for x in request.files.getlist("files"):
        media, format = x.content_type.split("/")

        err = ""
        # <=========== come back ===============
        # <=========== come back ===============
        # <=========== come back ===============
        # <=========== come back ===============
        if media not in ["image"] or format in ['svg+xml', 'x-icon']:
            err = f"{x.filename} => invalid file"
        elif _req - len(files) < 1:
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
            UPDATE post SET files = %s WHERE key = %s;
        """, (
        post["files"] + file_names,
        post["key"]
    ))

    post = get_post(key, cur).json["post"]

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
        "post": post,
        "error": error
    })


@ bp.put("/post/photo/<key>")
def order_delete_photo(key):
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    if "post:edit_photos" not in user["access"]:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "unauthorized access"
        })

    cur.execute('SELECT * FROM post WHERE key = %s;', (key,))
    post = cur.fetchone()
    if (
        not post
        or "photos" not in request.json
        or type(request.json["photos"]) is not list
    ):
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    photos = [p.split("/")[-1] for p in request.json["photos"]]

    if not all(x in post["photos"] for x in photos):
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    for x in post["photos"]:
        if x not in photos:
            storage("delete", x)

    draft = False
    if post["status"] == "live" and photos == []:
        draft = True

    log(
        cur=cur,
        user_key=user["key"],
        action="edited_photo",
        entity_key=post["key"],
        entity_type="post",
        misc={
            "from": post["photos"],
            "to": photos
        }
    )

    if draft:
        log(
            cur=cur,
            user_key=user["key"],
            action="edited",
            entity_key=post["key"],
            entity_type="post",
            misc={"status": "draft"}
        )

    cur.execute("""
            UPDATE post SET photos = %s, status = %s WHERE key = %s;
        """, (
        photos,
        "draft" if draft else post["status"],
        post["key"]
    ))

    post = get_post(key, cur).json["post"]

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "post": post
    })
