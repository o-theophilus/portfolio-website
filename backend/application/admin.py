from flask import Blueprint, jsonify, request
from uuid import uuid4
import os
import json
from .postgres import db_open, db_close
from werkzeug.security import generate_password_hash
from .log import log
from .tools import token_to_user


bp = Blueprint("admin", __name__)


permissions = {
    "user": [
        ['view', 1],
        ['set_permission', 3]
    ],
    "post": [
        ['add', 2],
        ['edit_photos', 2],
        ['edit_videos', 2],
        ['edit_title', 2],
        ['edit_date', 2],
        ['edit_description', 2],
        ['edit_content', 2],
        ['edit_tags', 2],
        ['edit_status', 2],
        ['edit_highlight', 2]
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
                INSERT INTO "user" ( key, status, name, email,
                    password, permissions)
                VALUES (%s, %s, %s, %s, %s, %s);
            """, (
            key,
            "confirmed",
            "Theophilus",
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


def get_highlight(cur=None):
    cur.execute("SELECT * FROM setting WHERE key = 'highlight';",)
    highlight = cur.fetchone()
    if not highlight:
        cur.execute("""
            INSERT INTO setting (key, misc)
            VALUES ('highlight', %s)
            RETURNING *;
        """, (json.dumps({"highlight": []}),))
        highlight = cur.fetchone()
    keys = highlight["misc"]["highlight"]

    cur.execute("""
        SELECT
            post.*,
            COALESCE(ARRAY_AGG(feedback.rating) FILTER (
                WHERE feedback.rating IS NOT NULL
            ), ARRAY[]::int[]) AS ratings
        FROM post
        LEFT JOIN feedback ON post.key = feedback.post_key
        WHERE
            post.status = 'publish'
            AND post.key = ANY(%s)
        GROUP BY post.key;
    """, (keys,))
    posts = cur.fetchall()
    posts = sorted(posts, key=lambda d: keys.index(d['key']))
    for x in posts:
        x["photos"] = [f"{request.host_url}photo/{y}" for y in x["photos"]]

    return posts


@bp.post("/highlight/<key>")
def set_highlight(key):
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    if "post:edit_highlight" not in user["permissions"]:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error":  "unauthorized access"
        })

    cur.execute('SELECT * FROM post WHERE key = %s OR slug = %s;', (key, key))
    post = cur.fetchone()
    if not post or post["status"] != "publish":
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "not found"
        })

    cur.execute("SELECT * FROM setting WHERE key = 'highlight';",)
    keys = cur.fetchone()["misc"]["highlight"]
    _from = keys

    if post["key"] in keys:
        keys.remove(post["key"])
    else:
        keys.append(post["key"])

    cur.execute("UPDATE setting SET misc = %s WHERE key = 'highlight';",
                (json.dumps({"highlight": keys}),))

    log(
        cur=cur,
        user_key=user["key"],
        action="edited_highlight",
        entity_type="setting",
        misc={
            "from": _from,
            "to": keys
        }
    )

    posts = get_highlight(cur)

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "posts": posts
    })


@bp.put("/highlight")
def edit_highlight():
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    if "post:edit_highlight" not in user["permissions"]:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error":  "unauthorized access"
        })

    if (
        "keys" not in request.json
        or not request.json["keys"]
        or type(request.json["keys"]) is not list
    ):
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    cur.execute("SELECT * FROM setting WHERE key = 'highlight';",)
    keys = cur.fetchone()["misc"]["highlight"]

    if request.json["keys"] == keys:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error":  "no change"
        })

    cur.execute("UPDATE setting SET misc = %s WHERE key = 'highlight';",
                (json.dumps({"highlight": request.json["keys"]}),))

    log(
        cur=cur,
        user_key=user["key"],
        action="edited_highlight",
        entity_type="setting",
        misc={
            "from": keys,
            "to": request.json["keys"]
        }
    )

    posts = get_highlight(cur)

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "posts": posts
    })
