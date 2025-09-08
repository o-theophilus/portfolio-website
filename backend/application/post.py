from flask import Blueprint, jsonify, request
from .tools import reserved_words, get_session
import re
import os
from uuid import uuid4
from .postgres import db_open, db_close
from .storage import storage
from .log import log
from .post_get import get_all, post_schema
from datetime import datetime, timezone
from werkzeug.security import check_password_hash

bp = Blueprint("post", __name__)


@bp.post("/test1")
def test():
    return jsonify({
        "status": 200,
        "message": "post endpoint"
    })


@bp.post("/post")
def add():
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

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
            "error": "This field is required"
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
        datetime.now(timezone.utc)
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

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    cur.execute('SELECT * FROM post WHERE key = %s;', (key,))
    post = cur.fetchone()
    if not post:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    error = {}

    if "title" in request.json:
        if "post:edit_title" not in user["access"]:
            error["title"] = "unauthorized access"
        elif not request.json["title"]:
            error["title"] = "This field is required"
        elif request.json["title"] == post["title"]:
            error["title"] = "No changes were made"
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
                    WHERE key = %s
                    RETURNING *;
                """, (
                request.json["title"],
                slug,
                post["key"]
            ))
            post = cur.fetchone()

    if "date" in request.json:
        if "post:edit_date" not in user["access"]:
            error["date"] = "unauthorized access"
        else:
            try:
                date_obj = datetime.fromisoformat(
                    request.json["date"].replace("Z", "+00:00"))
            except Exception:
                error["date"] = "Invalid request"
            else:
                cur.execute("""
                    UPDATE post
                    SET date = %s
                    WHERE key = %s
                    RETURNING *;
                """, (
                    date_obj,
                    post["key"]
                ))
                post = cur.fetchone()

    if "description" in request.json:
        if "post:edit_description" not in user["access"]:
            error["description"] = "unauthorized access"
        elif request.json["description"] == post["description"]:
            error["description"] = "No changes were made"
        else:
            cur.execute("""
                UPDATE post
                SET description = %s
                WHERE key = %s
                RETURNING *;
            """, (
                request.json["description"],
                post["key"]
            ))
            post = cur.fetchone()

    if "content" in request.json:
        if "post:edit_content" not in user["access"]:
            error["content"] = "unauthorized access"
        elif request.json["content"] == post["content"]:
            error["content"] = "No changes were made"
        else:
            cur.execute("""
                UPDATE post
                SET content = %s
                WHERE key = %s
                RETURNING *;
            """, (
                request.json["content"],
                post["key"]
            ))
            post = cur.fetchone()

    if "tags" in request.json:
        if "post:edit_tags" not in user["access"]:
            error["tags"] = "unauthorized access"
        elif type(request.json["tags"]) is not list:
            error["tags"] = "This field is required"
        elif set(request.json["tags"]) == set(post["tags"]):
            error["tags"] = "No changes were made"
        else:
            cur.execute("""
                    UPDATE post
                    SET tags = %s
                    WHERE key = %s
                    RETURNING *;
                """, (
                request.json["tags"],
                post["key"]
            ))
            post = cur.fetchone()

    if "author_email" in request.json:
        if "post:edit_author" not in user["access"]:
            error["author_email"] = "unauthorized access"
        elif not request.json["author_email"]:
            error["author_email"] = "This field is required"
        elif (
            not re.match(r"^[^\s@]+@[^\s@]+\.[^\s@]+$",
                         request.json["author_email"])
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
                error["author_email"] = "No changes were made"
            else:
                cur.execute("""
                    UPDATE post
                    SET author_key = %s
                    WHERE key = %s
                    RETURNING *;
                """, (
                    author["key"], post["key"]
                ))
                post = cur.fetchone()

    if "status" in request.json:
        if "post:edit_status" not in user["access"]:
            error["status"] = "unauthorized access"
        elif (
            not request.json["status"]
            or request.json["status"] not in ['active', 'draft']
        ):
            error["status"] = "Invalid request"
        elif request.json["status"] == post["status"]:
            error["status"] = "No changes were made"
        elif request.json["status"] == "active" and not post["photo"]:
            error["status"] = "no title photo"
        elif request.json["status"] == "active" and not post["content"]:
            error["status"] = "no content"
        else:
            cur.execute("""
                UPDATE post
                SET status = %s
                WHERE key = %s
                RETURNING *;
            """, (
                request.json["status"],
                post["key"]
            ))
            post = cur.fetchone()

    if error != {}:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            **error
        })

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
        "post": post_schema(post)
    })


@bp.delete("/post/<key>")
def delete(key):
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    error = None
    if "post:edit_status" not in user["access"]:
        error = "unauthorized access"
    elif "password" not in request.json:
        error = "This field is required"
    elif not check_password_hash(user["password"], request.json["password"]):
        error = "incorrect password"

    if error:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": error
        })

    cur.execute('SELECT * FROM post WHERE key = %s;', (key,))
    post = cur.fetchone()
    if not post:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    cur.execute("""
        DELETE FROM comment WHERE post_key = %s;
    """, (post["key"],))

    cur.execute("""
        DELETE FROM post WHERE key = %s;
    """, (post["key"],))

    storage("delete", post["photo"])
    for x in post["files"]:
        storage("delete", x)

    log(
        cur=cur,
        user_key=user["key"],
        action="deleted",
        entity_key=post["key"],
        entity_type="post"
    )

    db_close(con, cur)
    return jsonify({
        "status": 200
    })


@bp.put("/post/photo/<key>")
def add_photo(key):
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    if "post:edit_photo" not in user["access"]:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "unauthorized access"
        })

    cur.execute('SELECT * FROM post WHERE key = %s;', (key,))
    post = cur.fetchone()
    if 'file' not in request.files or not post:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    file = request.files["file"]
    if file.content_type not in ['image/jpeg', 'image/png']:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid file"
        })

    old_photo = None
    if post["photo"]:
        old_photo = post["photo"]
        storage("delete", post["photo"])

    file_name = storage("save", file)

    cur.execute("""
        UPDATE post
        SET photo = %s
        WHERE key = %s
        RETURNING *;
    """, (
        file_name,
        post["key"]
    ))
    post = cur.fetchone()

    log(
        cur=cur,
        user_key=user["key"],
        action="updated_photo",
        entity_type="post",
        entity_key=post["key"],
        misc={
            "from": old_photo,
            "to": file_name
        }
    )

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "post": post_schema(post)
    })


@bp.delete("/post/photo/<key>")
def delete_photo(key):
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    if "post:edit_photo" not in user["access"]:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "unauthorized access"
        })

    cur.execute('SELECT * FROM post WHERE key = %s;', (key,))
    post = cur.fetchone()
    if not post or not post["photo"]:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    storage("delete", post["photo"])

    log(
        cur=cur,
        user_key=user["key"],
        action="deleted_photo",
        entity_type="post",
        entity_key=post["key"],
        misc={"photo": post["photo"]}
    )

    if post["status"] == "active":
        log(
            cur=cur,
            user_key=user["key"],
            action="edited",
            entity_key=post["key"],
            entity_type="post",
            misc={"status": "draft"}
        )

    cur.execute("""
        UPDATE post
        SET photo = NULL, status = %s
        WHERE key = %s
        RETURNING *;
    """, (
        "draft" if post["status"] == "active" else post["status"],
        post["key"]
    ))
    post = cur.fetchone()

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "post": post_schema(post)
    })


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
        "post": post_schema(post),
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
    if (
        not post
        or "files" not in request.json
        or type(request.json["files"]) is not list
    ):
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    files = [p.split("/")[-1] for p in request.json["files"]]

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
        "post": post_schema(post)
    })
