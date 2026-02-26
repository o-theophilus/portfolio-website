import os
import re
from datetime import datetime, timezone
from uuid import uuid4

from flask import Blueprint, jsonify, request
from werkzeug.security import check_password_hash

from ..log import log
from ..postgres import db_close, db_open
from ..storage import storage
from ..tools import get_session, reserved_words
from .get import get_feature, get_many, post_schema

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
    if error:
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
        INSERT INTO post (title, slug, author_key)
        VALUES (%s, %s, %s) RETURNING *;
    """, (title, slug, user["key"],))
    post = cur.fetchone()

    log(
        cur=cur,
        user_key=user["key"],
        action="created",
        entity_key=post["key"],
        entity_type="post"
    )

    posts = get_many(cur)

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "post": post_schema(post),
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

    title = post["title"]
    slug = post["slug"]
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
        else:
            slug = re.sub(
                '-+', '-', re.sub('[^a-zA-Z0-9]', '-', title.lower()))
            slug = slug[:100]
            cur.execute('SELECT * FROM post WHERE key != %s AND slug = %s;',
                        (post["key"], slug))
            slug_in_use = cur.fetchone()
            if (slug_in_use or slug in reserved_words):
                slug = f"{slug[:89]}-{str(uuid4().hex)[:10]}"

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
                WHERE key::TEXT = %s OR email = %s OR username = %s;
            """, (author_key, author_key, author_key))
            author = cur.fetchone()
            print(author)

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

    if error:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            **error
        })

    cur.execute("""
        UPDATE post
        SET title = %s, slug = %s, date_created= %s, description= %s,
        content= %s, tags= %s, author_key= %s, status= %s, featured= %s
        WHERE key = %s RETURNING *;
    """, (
        title, slug, date_created, description, content, tags,
        author_key, status,
        post["featured"] if status == "active" else 0,
        post["key"]
    ))
    post = cur.fetchone()

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
        DELETE FROM post WHERE key = %s;
    """, (post["key"],))

    storage.delete(post["photo"], "post")
    for x in post["files"]:
        storage.delete(x, "post")

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


@bp.post("/post/like/<key>")
def like(key):
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    reaction = request.json.get("reaction")

    if reaction not in ["like", "dislike"]:
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    cur.execute("""SELECT * FROM post WHERE key = %s;""", (key,))
    if not cur.fetchone():
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    cur.execute("""
        SELECT * FROM "like" WHERE user_key = %s AND post_key = %s;
    """, (user["key"], key))
    user_reaction = cur.fetchone()

    un = ""
    if not user_reaction:
        cur.execute("""
            INSERT INTO "like" (user_key, post_key, reaction)
            VALUES (%s, %s, %s);
        """, (user["key"], key, reaction))
    elif user_reaction["reaction"] == reaction:
        un = "un"
        cur.execute("""DELETE FROM "like" WHERE key = %s;""",
                    (user_reaction["key"],))
    else:
        cur.execute("""
            UPDATE "like"
            SET date_created = %s, reaction = %s WHERE key = %s;
        """, (datetime.now(timezone.utc), reaction, user_reaction["key"]))

    log(
        cur=cur,
        user_key=user["key"],
        action=f"{un}{reaction}",
        entity_key=key,
        entity_type="post"
    )

    cur.execute("""
        SELECT
            COUNT(CASE WHEN user_key != %s
                AND reaction = 'like' THEN 1 END) AS others_like,
            COUNT(CASE WHEN user_key != %s
                AND reaction = 'dislike' THEN 1 END) AS others_dislike,
            MAX(CASE WHEN user_key = %s THEN reaction END) AS user_reaction
        FROM "like"
        WHERE post_key = %s
    """, (user["key"], user["key"], user["key"], key))
    reactions = cur.fetchone()

    db_close(con, cur)
    return jsonify({
        "status": 200,
        **reactions
    })


@bp.post("/post/feature/<key>")
def feature(key):
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    if "post:edit_featured" not in user["access"]:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error":  "unauthorized access"
        })

    cur.execute('SELECT * FROM post WHERE key = %s;', (key,))
    post = cur.fetchone()
    if not post or post["status"] != "active":
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    action = "added post to featured"
    if post["featured"] > 0:
        action = "removed post from featured"

    cur.execute("""
        UPDATE post SET featured = %s WHERE key = %s RETURNING *;
    """, (0 if post["featured"] > 0 else 1, post["key"],))
    post = cur.fetchone()

    cur.execute("""
        WITH ordered AS (
            SELECT key,
                ROW_NUMBER() OVER (ORDER BY featured ASC, date_created ASC)
                AS new_order
            FROM post
            WHERE featured > 0
        )
        UPDATE post p
        SET featured = o.new_order
        FROM ordered o
        WHERE p.key = o.key;
    """)

    log(
        cur=cur,
        user_key=user["key"],
        action=action,
        entity_key=post["key"],
        entity_type="post"
    )

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "post": post_schema(post)
    })


@bp.put("/post/feature")
def edit_feature():
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    if "post:edit_featured" not in user["access"]:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error":  "unauthorized access"
        })

    keys = request.json.get("keys")

    if not keys or type(keys) is not list:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    cur.execute("UPDATE post SET featured = 0;")

    cur.execute("""
        UPDATE post
        SET featured = x.position
        FROM (
            SELECT key, position
            FROM unnest(%s::uuid[]) WITH ORDINALITY AS t(key, position)
        ) AS x
        WHERE post.key = x.key;
    """, (keys,))

    log(
        cur=cur,
        user_key=user["key"],
        action="re-ordered featured post",
        entity_key="app",
        entity_type="app",

    )

    posts = get_feature(cur).json["posts"]

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "posts": posts
    })
