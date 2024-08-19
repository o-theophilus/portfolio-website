from flask import Blueprint, jsonify, request
from uuid import uuid4
import os
import json
from .postgres import db_open, db_close
from werkzeug.security import generate_password_hash, check_password_hash
from .log import log
from .tools import token_to_user, user_schema
from .storage import drive, storage


bp = Blueprint("admin", __name__)


access = {
    "user": [
        ['view', 1],
        ['set_access', 3]
    ],
    "admin": [
        ['manage_photo', 3]
    ],
    "post": [
        ['add', 2],
        ['edit_photos', 2],
        ['edit_title', 2],
        ['edit_date', 2],
        ['edit_description', 2],
        ['edit_content', 2],
        ['edit_tags', 2],
        ['edit_status', 2],
        ['edit_author', 2],
        ['edit_highlight', 2]
    ],
    "report": [
        ['view', 1],
        ['edit_status', 3]
    ],
    "comment": [
        ['view_deleted', 1]
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
                    password, access)
                VALUES (%s, %s, %s, %s, %s, %s);
            """, (
            key,
            "confirmed",
            "Theophilus",
            email,
            generate_password_hash(
                os.environ["MAIL_PASSWORD"], method="scrypt"),
            [f"{x}:{y[0]}" for x in access for y in access[x]]
        ))

        log(
            cur=cur,
            user_key=key,
            action="created",
            entity_type="account"
        )
        log(
            cur=cur,
            user_key=key,
            action="signedup",
            entity_type="account"
        )
        log(
            cur=cur,
            user_key=key,
            action="confirmed",
            entity_type="account"
        )

    db_close(con, cur)
    return jsonify({
        "status": 200
    })


@bp.get("/admin/access")
@bp.get("/admin/access/<search>")
def get_access(search=None):
    _all = [f"{x}:{y[0]}" for x in access for y in access[x]]
    if search:
        _all = [x for x in _all if x.find(search) != -1]

    return jsonify({
        "status": 200,
        "access": _all
    })


@bp.put("/admin/access/<key>")
def set_access(key):
    con, cur = db_open()

    me = token_to_user(cur)
    cur.execute('SELECT * FROM "user" WHERE key = %s;', (key,))
    user = cur.fetchone()

    error = None
    if not me or "user:set_access" not in me["access"]:
        error = "unauthorized access"
    elif "password" not in request.json:
        error = "cannot be empty"
    elif not check_password_hash(me["password"], request.json["password"]):
        error = "incorrect password"
    elif (
        not user
        or me["key"] == user["key"]
        or "access" not in request.json
        or type(request.json["access"]) is not list
        or user["email"] == os.environ["MAIL_USERNAME"]
        or user["status"] != "confirmed"
    ):
        error = "invalid request"

    if error:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": error
        })

    cur.execute("""
        UPDATE "user"
        SET access = %s
        WHERE key = %s;
    """, (
        request.json["access"],
        user["key"]
    ))

    log(
        cur=cur,
        user_key=me["key"],
        action="changed_access",
        entity_key=user["key"],
        entity_type="admin",
        misc={
            "from": user["access"],
            "to": request.json["access"]
        }
    )

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "user": user_schema(user)
    })


@bp.get("/photo/error")
def photo_error():
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    if "admin:manage_photo" not in user["access"]:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "unauthorized access"
        })

    cur.execute("""
        SELECT photo
        FROM "user";
    """)
    users_photo = cur.fetchall()
    users_photo = [x["photo"] for x in users_photo if x["photo"]]

    cur.execute("""
        SELECT photos
        FROM post;
    """)
    temp = cur.fetchall()
    posts_photos = []
    for x in temp:
        if x["photos"] != []:
            posts_photos += x["photos"]

    all_used_photos = users_photo + posts_photos
    paths = drive().list()["names"]
    all_stored_photos = [x.split('/')[1] for x in paths]

    cur.execute("""
        SELECT "user".key, "user".name
        FROM "user"
        WHERE
            photo IS NOT NULL
            AND NOT photo = ANY(%s);
    """, (all_stored_photos,))
    _users = cur.fetchall()

    cur.execute("""
        SELECT post.key, post.title
        FROM post
        WHERE NOT ARRAY[%s] @> photos;
    """, (all_stored_photos,))
    _posts = cur.fetchall()

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "unused": [f"{request.host_url}photo/{x}"
                   for x in all_stored_photos if x not in all_used_photos],
        "users": _users,
        "posts": _posts
    })


@bp.delete("/photo/error")
def delete_photo():
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    if "admin:manage_photo" not in user["access"]:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "unauthorized access"
        })

    if (
        "photos" not in request.json
        or type(request.json["photos"]) is not list
    ):
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    for x in request.json["photos"]:
        pass
        storage(x.split("/")[-1], delete=True)

    log(
        cur=cur,
        user_key=user["key"],
        action="deleted",
        entity_type="photo",
        misc={
            "photo(s)": request.json["photos"]
        }
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
            COALESCE(ARRAY_AGG(rating.rating) FILTER (
                WHERE rating.rating IS NOT NULL
            ), ARRAY[]::int[]) AS ratings
        FROM post
        LEFT JOIN rating ON post.key = rating.post_key
        WHERE
            post.status = 'active'
            AND post.key = ANY(%s)
        GROUP BY post.key;
    """, (keys,))
    posts = cur.fetchall()
    posts = sorted(posts, key=lambda d: keys.index(d['key']))
    for x in posts:
        x["photos"] = [f"{request.host_url}photo/{y}" for y in x["photos"]]

    return posts


@bp.post("/highlight")
def set_highlight():
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    if "post:edit_highlight" not in user["access"]:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error":  "unauthorized access"
        })

    if "key" not in request.json or not request.json["key"]:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "cannot be empty"
        })

    cur.execute("""SELECT * FROM post WHERE key = %s OR slug = %s;""",
                (request.json["key"], request.json["key"]))
    post = cur.fetchone()
    if not post or post["status"] != "active":
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

    if "post:edit_highlight" not in user["access"]:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error":  "unauthorized access"
        })

    if (
        "keys" not in request.json
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
