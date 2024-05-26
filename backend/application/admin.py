from flask import Blueprint, jsonify, request
from .tools import token_to_user
from . import db
from .schema import now, post_schema
from uuid import uuid4
import os
from .postgres import db_open, db_close
from werkzeug.security import generate_password_hash
from .log import log


bp = Blueprint("admin", __name__)


permissions = {
    "user": [
        ['view', 1],
        ['set_permission', 3]
    ],
    "post": [
        ['add', 2],
        ['edit_photo', 2],
        ['edit_status', 2],
        ['edit_title', 2],
        ['edit_content', 2],
        ['edit_description', 2],
        ['edit_photos', 2],
        ['edit_videos', 2],
        ['tags', 2]
    ],
    "log": [
        ['view', 1]
    ]
}


@bp.get("/admin/init")
def default_admin():
    con, cur = db_open()
    email = os.environ["MAIL_USERNAME"]

    cur.execute('SELECT * FROM "user" WHERE email = %s;', (email,))
    if not cur.fetchone():
        key = uuid4().hex
        cur.execute("""
                INSERT INTO "user" ( key, version, status, name, email,
                    password, permissions)
                VALUES (%s, %s, %s, %s, %s, %s, %s);
            """, (
            key,
            uuid4().hex,
            "confirmed",
            "App Admin",
            email,
            generate_password_hash(
                os.environ["MAIL_PASSWORD"], method="scrypt"),
            [f"{x}:{y[0]}" for x in permissions for y in permissions[x]]
        ))

        log(
            cur=cur,
            user_key=key,
            action="created",
            entity_type="auth"
        )
        log(
            cur=cur,
            user_key=key,
            action="signed_up",
            entity_type="auth"
        )
        log(
            cur=cur,
            user_key=key,
            action="confirmed",
            entity_type="auth"
        )

    db_close(con, cur)
    return jsonify({
        "status": 200
    })


def get_setting(data):
    for row in data:
        if row["type"] == "setting":
            return row
    return None


def admin():
    data = db.data()

    setting = get_setting(data)
    if not setting:
        setting = db.add({
            "type": "setting",
            "key": uuid4().hex,
            "version": uuid4().hex,
            "created_at": now(),
            "updated_at": now(),
            "featured_posts": []
        })

    return jsonify({
        "status": 200,
        "posts": []
    })


@bp.get("/featured_post")
def get():
    # data = db.data()

    # setting = get_setting(data)

    # posts = []
    # if setting:
    #     for slug in setting["featured_posts"]:
    #         for row in data:
    #             if (
    #                 row["type"] == "post"
    #                 and row["slug"] == slug
    #                 and row["status"] == "publish"
    #             ):
    #                 posts.append(row)

    return jsonify({
        "status": 200,
        # "posts": [post_schema(a) for a in posts]
        "posts": []
    })


@bp.post("/featured_post")
def featured_post():
    if (
        "featured_posts" not in request.json
        or type(request.json["featured_posts"]) is not list
    ):
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    data = db.data()

    user = token_to_user(data)
    if not user or "admin" not in user["roles"]:
        return jsonify({
            "status": 400,
            "error": "unauthorised access"
        })

    setting = get_setting(data)

    slugs = []
    for slug in request.json["featured_posts"][:10]:
        for row in data:
            if (
                row["type"] == "post"
                and row["slug"] == slug
                and row["status"] == "publish"
                and slug not in slugs
            ):
                slugs.append(row["slug"])

    setting["featured_posts"] = slugs
    db.add(setting)

    return jsonify({
        "status": 200,
        "setting": setting
    })


@bp.get("/slug")
def slug():
    data = db.data()

    slugs = []
    for row in data:
        if row["type"] == "post" and row["status"] == "publish":
            slugs.append(row["slug"])

    return jsonify({
        "status": 200,
        "slugs": slugs
    })
