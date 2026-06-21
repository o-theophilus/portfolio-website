import os
import re
from uuid import uuid4

from flask import Blueprint, request
from werkzeug.security import check_password_hash

from ..storage import storage
from ..tools import log, rate_limit, reserved_words, session
from .get import post_schema

bp = Blueprint("post", __name__)


@bp.post("/posts")
@session(True)
@rate_limit(10, 1)
@log("post")
def create(cur, user):
    if "post.add" not in user["access"]:
        return {
            "status": 403,
            "error": "unauthorized access"
        }, 403

    title = request.json.get("title")

    error = {}
    if not title:
        error["title"] = "This field is required"
    elif len(title) > 100:
        error["title"] = "This field cannot exceed 100 characters"
    if error:
        return {
            "status": 422,
            **error
        }, 422

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

    return {
        "status": 200,
        "post": post_schema(post),
        "log": {
            "entity_key": post["key"],
        }
    }, 200


@bp.put("/posts/<key>")
@session(True)
@rate_limit(10, 1)
@log("post")
def edit(cur, user, key):
    cur.execute('SELECT * FROM post WHERE key = %s;', (key,))
    post = cur.fetchone()
    if not post:
        return {
            "status": 404,
            "error": "Invalid request"
        }, 404

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
        title = request.json.get("title", "").strip()
        if "post.edit_title" not in user["access"]:
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
        if "post.edit_date" not in user["access"]:
            error["date_created"] = "unauthorized access"
        elif not date_created:
            error["date_created"] = "This field is required"
        elif date_created == post["date_created"]:
            error["date_created"] = "No changes were made"

    if "description" in request.json:
        description = request.json.get("description", "").strip()
        if "post.edit_description" not in user["access"]:
            error["description"] = "unauthorized access"
        elif description == post["description"]:
            error["description"] = "No changes were made"
        elif len(description) > 500:
            error["description"] = "This field cannot exceed 500 characters"

    if "content" in request.json:
        content = request.json.get("content", "").strip()
        if "post.edit_content" not in user["access"]:
            error["content"] = "unauthorized access"
        elif content == post["content"]:
            error["content"] = "No changes were made"
        elif len(content) > 5000:
            error["content"] = "This field cannot exceed 5000 characters"

    if "tags" in request.json:
        tags = request.json.get("tags")
        if "post.edit_tags" not in user["access"]:
            error["tags"] = "unauthorized access"
        elif type(tags) is not list:
            error["tags"] = "This field is required"
        elif set(tags) == set(post["tags"]):
            error["tags"] = "No changes were made"

    if "author_key" in request.json:
        author_key = request.json.get("author_key")
        if "post.edit_author" not in user["access"]:
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

            if not author:
                error["author_key"] = "no user found"
            elif author["key"] == post["author_key"]:
                error["author_key"] = "No changes were made"
            else:
                author_key = author["key"]

    if "status" in request.json:
        status = request.json.get("status")
        if "post.edit_status" not in user["access"]:
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
        return {
            "status": 400,
            **error
        }, 400

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

    return {
        "status": 200,
        "post": post_schema(post),
        "log": {
            "entity_key": post["key"],
            "misc": request.json
        }
    }, 200


@bp.post("/posts/<key>/feature")
@session(True)
@rate_limit(10, 1)
@log("post")
def feature(cur, user, key):
    if "post.edit_featured" not in user["access"]:
        return {
            "status": 403,
            "error":  "unauthorized access"
        }, 403

    cur.execute("""
        SELECT * FROM post WHERE key = %s AND status = 'active';
    """, (key,))
    post = cur.fetchone()
    if not post:
        return {
            "status": 404,
            "error": "Invalid request"
        }, 404

    action = "add"
    if post["featured"] > 0:
        action = "remove"

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

    return {
        "status": 200,
        "post": post_schema(post),
        "log": {
            "entity_key": post["key"],
            "misc": {
                "action": action
            }
        }
    }, 200


@bp.delete("/posts/<key>")
@session(True)
@rate_limit(10, 1)
@log("post")
def delete(cur, user, key):
    if "post.edit_status" not in user["access"]:
        return {
            "status": 403,
            "error":  "unauthorized access"
        }, 403

    cur.execute('SELECT * FROM post WHERE key = %s;', (key,))
    post = cur.fetchone()
    if not post:
        return {
            "status": 404,
            "error": "Invalid request"
        }, 404

    password = request.json.GET("password")
    error = None
    if not password:
        error = "This field is required"
    elif not check_password_hash(user["password"], password):
        error = "Incorrect password"
    if error:
        return {
            "status": 422,
            "error": error
        }, 422

    cur.execute("""
        DELETE FROM post WHERE key = %s;
    """, (post["key"],))

    storage.delete(post["photo"], "post")
    for x in post["files"]:
        storage.delete(x, "post")

    return {
        "status": 200,
        "log": {
            "entity_key": post["key"]
        }
    }, 200


@bp.post("/posts/<key>/like")
@session(True)
@rate_limit(10, 1)
@log("post")
def like(cur, user, key):
    cur.execute("""SELECT * FROM post WHERE key = %s;""", (key,))
    if not cur.fetchone():
        return {
            "status": 404,
            "error": "Invalid request"
        }, 404

    reaction = request.json.get("reaction")
    if reaction not in ["like", "dislike"]:
        return {
            "status": 422,
            "error": "Invalid request"
        }, 422

    cur.execute("""
        SELECT * FROM "like"
        WHERE user_key = %s AND post_key = %s;
    """, (user["key"], key))
    user_reaction = cur.fetchone()

    un = ""
    if not user_reaction:
        cur.execute("""
            INSERT INTO "like" (user_key, reaction, post_key)
            VALUES (%s, %s, %s);
        """, (user["key"], reaction, key))
    elif user_reaction["reaction"] == reaction:
        un = "un"
        cur.execute("""DELETE FROM "like" WHERE key = %s;""",
                    (user_reaction["key"],))
    else:
        cur.execute("""
            UPDATE "like"
            SET date_created = now(), reaction = %s WHERE key = %s;
        """, (reaction, user_reaction["key"]))

    cur.execute("""
        SELECT
            COUNT(CASE WHEN user_key != %s
                AND reaction = 'like' THEN 1 END) AS others_like,
            COUNT(CASE WHEN user_key != %s
                AND reaction = 'dislike' THEN 1 END) AS others_dislike,
            MAX(CASE WHEN user_key = %s THEN reaction END) AS user_reaction
        FROM "like"
        WHERE post_key = %s;
    """, (user["key"], user["key"], user["key"], key))
    reactions = cur.fetchone()

    return {
        "status": 200,
        **reactions,
        "log": {
            "entity_key": key,
            "misc": {
                "action": f"{un}{reaction}"
            }
        }
    }, 200


@bp.post("/posts/<key>/comments")
@session(True)
@rate_limit(10, 1)
@log("comment")
def create_comment(cur, user, key):
    cur.execute("""
        SELECT * FROM post WHERE slug = %s OR key = %s;
    """, (key, key))
    post = cur.fetchone()
    if not post:
        return {
            "status": 404,
            "error": "Invalid request"
        }, 404

    parent_key = request.json.get("parent_key")
    comment = request.json.get("comment", "").strip()

    if parent_key:
        cur.execute("SELECT * FROM comment WHERE key = %s;", (parent_key,))
        parent = cur.fetchone()
        if not parent or parent["parent_key"] is not None:
            return {
                "status": 404,
                "error": "Invalid request"
            }, 404

    error = {}
    if not comment:
        error["comment"] = "This field is required"
    elif len(comment) > 500:
        error["comment"] = "This field cannot exceed 500 characters"
    if error:
        return {
            "status": 422,
            **error
        }, 422

    cur.execute("""
        INSERT INTO comment (user_key, post_key, comment, parent_key)
        VALUES (%s, %s, %s, %s) RETURNING *;
    """, (user["key"], post["key"], comment, parent_key))
    comment = cur.fetchone()

    return {
        "status": 200,
        "log": {
            "entity_key": comment["key"],
            "action": "comment.create",
            "misc": {
                "post_key": post["key"]
            }
        }

    }, 200


@bp.put("/posts/feature")
@session(True)
@rate_limit(10, 1)
@log("app")
def edit_home_feature(cur, user):
    if "post.edit_featured" not in user["access"]:
        return {
            "status": 403,
            "error":  "unauthorized access"
        }, 403

    keys = request.json.get("keys")

    if not keys or type(keys) is not list:
        return {
            "status": 422,
            "error": "Invalid request"
        }, 422

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

    return {
        "status": 200,
    }, 200
