from flask import Blueprint, jsonify, request
from .tools import reserved_words, token_to_user
import re
import os
from uuid import uuid4
from .postgres import db_open, db_close
from .storage import storage
from .log import log
from .post_get import get_post
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

    if "post:add" not in user["permissions"]:
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
        author["key"],
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

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "post": post
    })


@ bp.put("/post/<key>")
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
        if "post:edit_title" not in user["permissions"]:
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
        if "post:edit_date" not in user["permissions"]:
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
        if "post:edit_description" not in user["permissions"]:
            error["description"] = "unauthorized access"
        elif request.json["description"] == post["description"]:
            error["description"] = "no change"
        else:
            cur.execute("UPDATE post SET description = %s WHERE key = %s;", (
                request.json["description"], post["key"]))

    if "content" in request.json:
        if "post:edit_content" not in user["permissions"]:
            error["content"] = "unauthorized access"
        elif request.json["content"] == post["content"]:
            error["content"] = "no change"
        else:
            cur.execute("UPDATE post SET content = %s WHERE key = %s;", (
                request.json["content"], post["key"]))

    if "tags" in request.json:
        if "post:edit_tags" not in user["permissions"]:
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
        if "post:edit_author" not in user["permissions"]:
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
        if "post:edit_status" not in user["permissions"]:
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


@ bp.post("/post/like/<key>")
def like(key):
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    cur.execute("""
        SELECT * FROM post WHERE post.key = %s;
    """, (key,))
    post = cur.fetchone()

    if (
        not post
        or "like" not in request.json
        or type(request.json["like"]) is not bool
    ):
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    post["photos"] = [f"{request.host_url}photo/{x}" for x in post["photos"]]

    if request.json["like"]:
        if user["key"] in post["dislike"]:
            post["dislike"].remove(user["key"])
        if user["key"] in post["like"]:
            post["like"].remove(user["key"])
        else:
            post["like"].append(user["key"])
    else:
        if user["key"] in post["like"]:
            post["like"].remove(user["key"])
        if user["key"] in post["dislike"]:
            post["dislike"].remove(user["key"])
        else:
            post["dislike"].append(user["key"])

    cur.execute("""
        UPDATE post
        SET
            "like" = %s,
            dislike = %s
        WHERE key = %s;
    """, (
        post["like"],
        post["dislike"],
        post["key"]
    ))

    log(
        cur=cur,
        user_key=user["key"],
        action='liked' if request.json['like'] else 'disliked',
        entity_key=post["key"],
        entity_type="post"
    )

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "post": post
    })


@ bp.post("/post/photo/<key>")
def add_photos(key):
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    if "post:edit_photos" not in user["permissions"]:
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
    for x in request.files.getlist("files"):
        media, format = x.content_type.split("/")

        err = ""
        if media != "image" or format in ['svg+xml', 'x-icon']:
            err = f"{x.filename} => invalid file"
        elif len(files) + len(post["photos"]) >= 10:
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
        filename = storage(x)
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


@ bp.put("/post/photo/<key>")
def order_photo(key):
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    if "post:edit_photos" not in user["permissions"]:
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
        or set(post["photos"]) != set(
            [p.split("/")[-1] for p in request.json["photos"]])
    ):
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    in_photos = [p.split("/")[-1] for p in request.json["photos"]]

    log(
        cur=cur,
        user_key=user["key"],
        action="arranged_photo",
        entity_key=post["key"],
        entity_type="post",
        misc={
            "from": post["photos"],
            "to": in_photos
        }
    )

    cur.execute("""
            UPDATE post
            SET photos = %s
            WHERE key = %s;
        """, (
        in_photos,
        post["key"]
    ))

    post = get_post(key, cur).json["post"]

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "post": post
    })


@ bp.delete("/post/photo/<key>")
def delete_photo(key):
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    if "post:edit_photos" not in user["permissions"]:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "unauthorized access"
        })

    cur.execute('SELECT * FROM post WHERE key = %s;', (key,))
    post = cur.fetchone()
    if (
        not post
        or "active_photo" not in request.json
        or not request.json["active_photo"]
        or request.json["active_photo"].split("/")[-1] not in post["photos"]
    ):
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    file_name = request.json["active_photo"].split("/")[-1]

    storage(file_name, delete=True)

    post["photos"].remove(file_name)
    cur.execute("""
            UPDATE post
            SET photos = %s
            WHERE key = %s;
        """, (
        post["photos"],
        post["key"]
    ))

    if len(post["photos"]) == 0 and post["status"] == "live":
        cur.execute("""
                UPDATE post
                SET status = %s
                WHERE key = %s;
            """, (
            "draft",
            post["key"]
        ))

    post = get_post(key, cur).json["post"]

    log(
        cur=cur,
        user_key=user["key"],
        action="deleted_photo",
        entity_key=post["key"],
        entity_type="post",
        misc={"photo": file_name}
    )

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "post": post
    })
