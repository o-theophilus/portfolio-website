from flask import Blueprint, jsonify, request
from uuid import uuid4
import os
from psycopg2.extras import Json
from .postgres import db_open, db_close
from werkzeug.security import generate_password_hash, check_password_hash
from .log import log
from .tools import get_session, user_schema
from .storage import storage
from .post import post_schema


bp = Blueprint("admin", __name__)


access = {
    "user": [
        ['view', 1],
        ['reset_name', 2],
        ['reset_username', 2],
        ['reset_photo', 2],
        ['block', 2],
        ['set_access', 3]
    ],
    "admin": [
        ['manage_files', 3]
    ],
    "post": [
        ['add', 2],
        ['edit_photo', 2],
        ['edit_title', 2],
        ['edit_date', 2],
        ['edit_description', 2],
        ['edit_content', 2],
        ['edit_files', 2],
        ['edit_tags', 2],
        ['edit_status', 2],
        ['edit_author', 2],
        ['edit_highlight', 2]
    ],
    "report": [
        ['view', 1],
        ['edit_status', 3]
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
        cur.execute("""
                INSERT INTO "user"
                (status, name, username, email, password, access)
                VALUES (%s, %s, %s, %s, %s, %s) RETURNING *;
            """, (
            "confirmed",
            "Theophilus",
            "omni",
            email,
            generate_password_hash(
                os.environ["MAIL_PASSWORD"], method="scrypt"),
            [f"{x}:{y[0]}" for x in access for y in access[x]]
        ))
        user = cur.fetchone()

        log(
            cur=cur,
            user_key=user["key"],
            action="created",
            entity_type="account"
        )
        log(
            cur=cur,
            user_key=user["key"],
            action="signedup",
            entity_type="account"
        )
        log(
            cur=cur,
            user_key=user["key"],
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


@bp.put("/admin/user/access/<key>")
def user_access(key):
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    me = session["user"]

    cur.execute('SELECT * FROM "user" WHERE key = %s;', (key,))
    user = cur.fetchone()

    error = None
    if not me or "user:set_access" not in me["access"]:
        error = "unauthorized access"
    elif "password" not in request.json:
        error = "This field is required"
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
        error = "Invalid request"

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


@bp.put("/admin/user/actions/<key>")
def user_actions(key):
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    cur.execute("""SELECT * FROM "user" WHERE key = %s;""", (key,))
    e_user = cur.fetchone()
    if (
        not e_user or user["key"] == e_user["key"]
        or e_user["email"] == os.environ["MAIL_USERNAME"]
    ):
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    error = {}
    if (
        "actions" not in request.json
        or type(request.json["actions"]) is not list
        or request.json["actions"] == []
    ):
        error["actions"] = "select action"
    if "note" not in request.json or not request.json["note"]:
        error["note"] = "This field is required"
    if error != {}:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            **error
        })

    actions = []
    error = None
    if "reset_name" in request.json["actions"]:
        if "user:reset_name" in user["access"]:
            actions.append("name")
        else:
            error = "unauthorized access"
    if "reset_username" in request.json["actions"]:
        if "user:reset_username" in user["access"]:
            actions.append("name")
        else:
            error = "unauthorized access"
    if "reset_photo" in request.json["actions"]:
        if "user:reset_photo" in user["access"]:
            actions.append("photo")
        else:
            error = "unauthorized access"

    if actions == []:
        error = "Invalid request"
    if error:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": error
        })

    _key = uuid4().hex
    cur.execute("""
        UPDATE "user" SET name = %s, username = %s, photo = %s
        WHERE key = %s RETURNING *;
    """, (
        f"user {_key[-8:]}" if "name" in actions else e_user["name"],
        f"user_{_key[:8]}" if "username" in actions else e_user["username"],
        None if "photo" in actions else e_user["photo"],
        e_user["key"]
    ))
    e_user = cur.fetchone()

    log(
        cur=cur,
        user_key=user["key"],
        action="reset",
        entity_type="user",
        entity_key=e_user["key"],
        misc={
            "field(s)": ", ".join(actions),
            "note": request.json["note"]
        }
    )

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "user": user_schema(e_user)
    })


@bp.put("/admin/user/block/<key>")
def user_block(key):
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    cur.execute("""SELECT * FROM "user" WHERE key = %s;""", (key,))
    e_user = cur.fetchone()
    if (
        not e_user or user["key"] == e_user["key"]
        or e_user["email"] == os.environ["MAIL_USERNAME"]
    ):
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    if "note" not in request.json or not request.json["note"]:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "note": "This field is required"
        })

    log(
        cur=cur,
        user_key=user["key"],
        action="unblocked" if e_user["status"] == "blocked" else "blocked",
        entity_type="user",
        entity_key=e_user["key"],
        misc={"note": request.json["note"]}
    )

    cur.execute("""
        DELETE FROM session WHERE user_key = %s;
    """, (e_user["key"],))

    cur.execute("""
        UPDATE "user" SET status = %s
        WHERE key = %s RETURNING *;
    """, (
        "signedup" if e_user["status"] == "blocked" else "blocked",
        e_user["key"]
    ))
    e_user = cur.fetchone()

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "user": user_schema(e_user)
    })


@bp.get("/file/error")
def file_error():
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

    cur.execute("""SELECT photo, files FROM post;""")
    temp = cur.fetchall()
    posts_files = []
    for x in temp:
        posts_files.append(x["photo"])
        if x["files"] != []:
            posts_files += x["files"]

    all_used_files = users_photo + posts_files
    all_stored_files = storage("get_all")

    cur.execute("""
        SELECT key, name
        FROM "user"
        WHERE
            photo IS NOT NULL
            AND NOT photo = ANY(%s);
    """, (all_stored_files,))
    _users = cur.fetchall()

    cur.execute("""
        SELECT key, title
        FROM post
        WHERE
            photo IS NOT NULL
            AND NOT photo = ANY(%s)
            OR NOT ARRAY[%s] @> files;
    """, (all_stored_files, all_stored_files))
    _posts = cur.fetchall()

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "unused": [f"{request.host_url}file/{x}"
                   for x in all_stored_files if x not in all_used_files],
        "users": _users,
        "posts": _posts
    })


@bp.delete("/file/error")
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

    if (
        "files" not in request.json
        or type(request.json["files"]) is not list
    ):
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    for x in request.json["files"]:
        storage("delete", x.split("/")[-1])

    log(
        cur=cur,
        user_key=user["key"],
        action="deleted",
        entity_type="file",
        misc={
            "file(s)": request.json["files"]
        }
    )

    db_close(con, cur)
    return jsonify({
        "status": 200
    })


@bp.get("/highlight")
def get_highlight(cur=None):
    close_conn = not cur
    if not cur:
        con, cur = db_open()

    cur.execute("SELECT * FROM setting WHERE alias = 'highlight';",)
    highlight = cur.fetchone()
    if not highlight:
        cur.execute("""
            INSERT INTO setting (alias, value)
            VALUES ('highlight', %s)
            RETURNING *;
        """, (Json({"post_keys": []}),))
        highlight = cur.fetchone()
    keys = highlight["value"]["post_keys"]

    cur.execute("""
        SELECT * FROM post WHERE status = 'active' AND key = ANY(%s);
    """, (keys,))
    posts = cur.fetchall()
    posts = sorted(posts, key=lambda d: keys.index(d['key']))

    if close_conn:
        db_close(con, cur)
    return jsonify({
        "status": 200,
        "posts": [post_schema(x) for x in posts]
    })


@bp.post("/highlight")
def set_highlight():
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

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
            "error": "This field is required"
        })

    cur.execute("""
        SELECT * FROM post WHERE key = %s OR slug = %s;
    """, (request.json["key"], request.json["key"]))
    post = cur.fetchone()
    if not post:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "not found"
        })

    if post["status"] != "active":
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "not active"
        })

    cur.execute("SELECT * FROM setting WHERE alias = 'highlight';",)
    keys = cur.fetchone()["value"]["post_keys"]
    _from = [*keys]

    if post["key"] in keys:
        keys.remove(post["key"])
    else:
        keys.append(post["key"])

    cur.execute("UPDATE setting SET value = %s WHERE alias = 'highlight';",
                (Json({"post_keys": keys}),))

    log(
        cur=cur,
        user_key=user["key"],
        action="edited_highlight",
        entity_type="setting",
        misc={
            "from": ", ".join(_from),
            "to": ", ".join(keys)
        }
    )

    posts = get_highlight(cur).json["posts"]

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "posts": posts
    })


@bp.put("/highlight")
def edit_highlight():
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

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
            "error": "Invalid request"
        })

    cur.execute("SELECT * FROM setting WHERE alias = 'highlight';",)
    keys = cur.fetchone()["value"]["post_keys"]

    if request.json["keys"] == keys:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error":  "No changes were made"
        })

    cur.execute("UPDATE setting SET value = %s WHERE alias = 'highlight';",
                (Json({"post_keys": request.json["keys"]}),))

    log(
        cur=cur,
        user_key=user["key"],
        action="edited_highlight",
        entity_type="setting",
        misc={
            "from": ", ".join(keys),
            "to": ", ".join(request.json["keys"])
        }
    )

    posts = get_highlight(cur).json["posts"]

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "posts": posts
    })
