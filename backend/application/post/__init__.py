from flask import Blueprint, jsonify, request
import re
import os
from uuid import uuid4
from werkzeug.security import check_password_hash
from ..tools import reserved_words, get_session
from ..postgres import db_open, db_close
from ..storage import storage
from ..log import log
from .get import get_many, post_schema

bp = Blueprint("post", __name__)


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

    title = request.json.get("title")

    error = {}
    if not title:
        error["title"] = "This field is required"
    elif len(title) > 100:
        error["title"] = "This field cannot exceed 100 characters"
    if error != {}:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            **error
        })

    slug = re.sub('-+', '-', re.sub('[^a-zA-Z0-9]', '-', title.lower()))
    slug = slug[:100]
    cur.execute('SELECT * FROM post WHERE slug = %s;', (slug,))
    post = cur.fetchone()
    if post or slug in reserved_words:
        slug = f"{slug[:89]}-{str(uuid4().hex)[:10]}"

    cur.execute("""
        SELECT key FROM "user" WHERE email = %s;
    """, (os.environ["MAIL_USERNAME"],))
    author = cur.fetchone()

    cur.execute("""
        INSERT INTO post (title, slug, author_key)
        VALUES (%s, %s, %s) RETURNING *;
    """, (
        title,
        slug,
        author["key"] if author else None,
    ))
    item = cur.fetchone()

    log(
        cur=cur,
        user_key=user["key"],
        action="created",
        entity_key=item["key"],
        entity_type="post"
    )

    items = get_many(cur)

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "item": post_schema(item),
        "items": items.json["items"],
        "total_page": items.json["total_page"]
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

    title = post["title"]
    date_created = post["date_created"]
    description = post["description"]
    content = post["content"]
    tags = post["tags"]
    author_key = post["author_key"]
    status = post["status"]

    if "title" in request.json:
        title = request.json.get("title")
        if "post:edit_title" not in user["access"]:
            error["title"] = "unauthorized access"
        elif not title:
            error["title"] = "This field is required"
        elif title == post["title"]:
            error["title"] = "No changes were made"
        elif len(title) > 100:
            error["name"] = "This field cannot exceed 100 characters"

    if "date_created" in request.json:
        date_created = request.json.get("date_created")
        if "post:edit_date" not in user["access"]:
            error["date_created"] = "unauthorized access"
        elif not date_created:
            error["date_created"] = "This field is required"
        elif date_created == post["date_created"]:
            error["date_created"] = "No changes were made"

    if "description" in request.json:
        description = request.json.get("description")
        if "post:edit_description" not in user["access"]:
            error["description"] = "unauthorized access"
        elif description == post["description"]:
            error["description"] = "No changes were made"
        elif len(description) > 500:
            error["description"] = "This field cannot exceed 500 characters"

    if "content" in request.json:
        content = request.json.get("content")
        if "post:edit_content" not in user["access"]:
            error["content"] = "unauthorized access"
        elif content == post["content"]:
            error["content"] = "No changes were made"

    if "tags" in request.json:
        tags = request.json.get("tags")
        if "post:edit_tags" not in user["access"]:
            error["tags"] = "unauthorized access"
        elif type(tags) is not list:
            error["tags"] = "This field is required"
        elif set(tags) == set(post["tags"]):
            error["tags"] = "No changes were made"

    if "author_key" in request.json:
        author_key = request.json.get("author_key")
        if "post:edit_author" not in user["access"]:
            error["author_key"] = "unauthorized access"
        elif not author_key:
            error["author_key"] = "This field is required"
        else:
            if author_key == "default":
                author_key = os.environ["MAIL_USERNAME"]

            cur.execute("""
                SELECT key FROM "user"
                WHERE key = %s OR email = %s OR username = %s;
            """, (author_key, author_key, author_key))
            author = cur.fetchone()

            if not author:
                error["author_key"] = "no user found"
            elif author["key"] == post["author_key"]:
                error["author_key"] = "No changes were made"
            else:
                author_key = author["key"]

    if "status" in request.json:
        status = request.json.get("status")
        if "post:edit_status" not in user["access"]:
            error["status"] = "unauthorized access"
        elif not status or status not in ['active', 'draft']:
            error["status"] = "Invalid request"
        elif status == post["status"]:
            error["status"] = "No changes were made"
        elif status == "active" and not post["photo"]:
            error["status"] = "no title photo"
        elif status == "active" and not post["content"]:
            error["status"] = "no content"

    if error != {}:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            **error
        })

    slug = re.sub('-+', '-', re.sub('[^a-zA-Z0-9]', '-', title.lower()))
    slug = slug[:100]
    cur.execute('SELECT * FROM post WHERE key != %s AND slug = %s;',
                (post["key"], slug))
    slug_in_use = cur.fetchone()
    if (slug_in_use or slug in reserved_words):
        slug = f"{slug[:89]}-{str(uuid4().hex)[:10]}"

    cur.execute("""
        UPDATE post
        SET title = %s, slug = %s, date_created= %s, description= %s,
        content= %s, tags= %s, author_key= %s, status= %s
        WHERE key = %s RETURNING *;
    """, (
        title, slug, date_created, description, content, tags,
        author_key, status, post["key"]
    ))
    item = cur.fetchone()

    log(
        cur=cur,
        user_key=user["key"],
        action="edited",
        entity_key=item["key"],
        entity_type="post",
        misc=request.json
    )

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "item": post_schema(item)
    })


@bp.delete("/post/<key>")
def delete(key):
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    password = request.json.GET("password")

    error = None
    if "post:edit_status" not in user["access"]:
        error = "unauthorized access"
    elif not password:
        error = "This field is required"
    elif not check_password_hash(user["password"], password):
        error = "Incorrect password"
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
        DELETE FROM "like"
        WHERE entity_type = 'post' entity_key = %s;
    """, (post["key"],))

    cur.execute("""
        WITH RECURSIVE to_delete AS (
            SELECT key
            FROM comment
            WHERE post_key = %s

            UNION ALL

            SELECT c.key
            FROM comment c
            INNER JOIN to_delete td ON c.parent_key = td.key
        )
        DELETE FROM comment
        WHERE key IN (SELECT key FROM to_delete);
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
