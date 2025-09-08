from flask import Blueprint, jsonify, request
from .postgres import db_open, db_close
from .tools import (
    get_session, user_schema, send_mail,
    generate_code, check_code, reserved_words)
from .log import log
import re
import os
from werkzeug.security import generate_password_hash, check_password_hash
from .storage import storage


bp = Blueprint("user", __name__)


@bp.post("/user/theme")
def theme():
    con, cur = db_open()

    session = get_session(cur)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    theme = "light"
    if user["theme"] == "light":
        theme = "dark"

    log(
        cur=cur,
        user_key=user["key"],
        action="changed_theme",
        entity_type="user",
        entity_key=user["key"],
        misc={
            "from": user["theme"],
            "to": theme
        }
    )

    cur.execute("""
        UPDATE "user"
        SET theme = %s
        WHERE key = %s
        RETURNING *
    ;""", (
        theme,
        user["key"]
    ))
    user = cur.fetchone()

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "user": user_schema(user)
    })


@bp.put("/user")
def edit_user():
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    error = {}

    name = user["name"]
    username = user["username"]
    phone = user["phone"]

    if "name" in request.json:
        name = ' '.join(request.json.get("name", "").strip().split())
        if not name:
            error['name'] = "This field is required"
        elif name == user["name"]:
            error['name'] = "No changes were made"
        elif len(name) > 100:
            error["name"] = "This field cannot exceed 100 characters"

    if "username" in request.json:
        username = request.json.get("username", "").strip()
        if not username:
            error["username"] = "This field is required"
        elif (
                not re.match(r"^[A-Za-z][A-Za-z0-9_]*$", username)
                or len(username) > 20
        ):
            error["name"] = """'Username can only contain letters,
            numbers, or underscores, must start with a letter,
            and be at most 20 characters"""
        elif username == user["username"]:
            error['username'] = "No changes were made"
        elif username in reserved_words:
            error["username"] = "Username is not allowed"
        else:
            cur.execute(
                'SELECT * FROM "user" WHERE username = %s AND key != %s;',
                (username, user["key"]))
            if cur.fetchone():
                error["username"] = "Username already in use"

    if "phone" in request.json:
        phone = request.json.get("phone", "").replace(" ", "")
        if phone == user["phone"]:
            error['phone'] = "No changes were made"
        elif len(phone) > 20:
            error["phone"] = "This field cannot exceed 20 characters"

    if error != {}:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            **error
        })

    cur.execute("""
        UPDATE "user"
        SET name = %s, username = %s, phone = %s WHERE key = %s
        RETURNING *;
    """, (name, username, phone, user["key"]))
    user = cur.fetchone()

    log(
        cur=cur,
        user_key=user["key"],
        action="edited",
        entity_type="user",
        entity_key=user["key"],
        misc=request.json
    )

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "user": user_schema(user)
    })


@bp.post("/user/email/1")
def email_1_old_email():
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    if (
        "email_template" not in request.json
        or not request.json["email_template"]
    ):
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    send_mail(
        user["email"],
        "Email Change Confirmation - Code",
        request.json['email_template'].format(
            name=user["name"],
            code=generate_code(cur, user["key"], user["email"], "change email")
        )
    )

    db_close(con, cur)
    return jsonify({
        "status": 200
    })


@bp.post("/user/email/2")
def email_2_old_code():
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    error = check_code(cur, user["key"], user["email"], "code_1")
    if error:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "code_1": error
        })

    db_close(con, cur)
    return jsonify({
        "status": 200
    })


@bp.post("/user/email/3")
def email_3_new_email():
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    error = check_code(cur, user["key"], user["email"], "code_1")
    if error:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    if (
        "email_template" not in request.json
        or not request.json["email_template"]
    ):
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    error = None
    if "email" not in request.json or not request.json["email"]:
        error = "This field is required"
    elif not re.match(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", request.json["email"]):
        error = "Invalid email address"
    if error:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "email": error
        })

    if user["email"] == request.json["email"]:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "email": "please use a different email form your current email"
        })

    cur.execute('SELECT * FROM "user" WHERE email = %s;',
                (request.json["email"],))
    exist = cur.fetchone()
    if exist:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "email": "email is already in use"
        })

    send_mail(
        request.json["email"],
        "Email Change Confirmation - Code",
        request.json['email_template'].format(
            name=user["name"],
            code=generate_code(
                cur, user["key"], request.json["email"], "change email", False)
        )
    )

    db_close(con, cur)
    return jsonify({
        "status": 200
    })


@bp.post("/user/email/4")
def email_4_new_code():
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    error = check_code(cur, user["key"], user["email"], "code_1")
    if error:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    if (
        "email" not in request.json or not request.json["email"]
        or not re.match(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", request.json["email"])
    ):
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    if user["email"] == request.json["email"]:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    cur.execute('SELECT * FROM "user" WHERE email = %s;',
                (request.json["email"],))
    exist = cur.fetchone()
    if exist:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    error = check_code(cur, user["key"], request.json["email"], "code_2")
    if error:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    if user["email"] == os.environ["MAIL_USERNAME"]:
        cur.execute("DELETE FROM code WHERE user_key = %s;", (user["key"],))
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "LoL"
        })

    log(
        cur=cur,
        user_key=user["key"],
        action="changed_email",
        entity_type="user",
        entity_key=user["key"],
        misc={
            "from": user['email'],
            "to": request.json['email']
        }
    )

    cur.execute("""
        UPDATE "user" SET email = %s WHERE key = %s RETURNING *;
    """, (
        request.json["email"], user["key"]))
    user = cur.fetchone()

    cur.execute("DELETE FROM code WHERE user_key = %s;", (user["key"],))

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "user": user_schema(user)
    })


@bp.post("/user/password/1")
def password_1_email():
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    if (
        "email_template" not in request.json
        or not request.json["email_template"]
    ):
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    send_mail(
        user["email"],
        "Password Change Confirmation - Code",
        request.json['email_template'].format(
            name=user["name"],
            code=generate_code(
                cur, user["key"], user["email"], "change password")
        )
    )

    db_close(con, cur)
    return jsonify({
        "status": 200
    })


@bp.post("/user/password/2")
def password_2_code():
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    error = check_code(cur, user["key"], user["email"])
    if error:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "code": error
        })

    db_close(con, cur)
    return jsonify({
        "status": 200
    })


@bp.post("/user/password/3")
def password_3_password():
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    error = check_code(cur, user["key"], user["email"])
    if error:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    error = {}
    if "password" not in request.json or not request.json["password"]:
        error["password"] = "This field is required"
    elif (
        not re.search("[a-z]", request.json["password"])
        or not re.search("[A-Z]", request.json["password"])
        or not re.search("[0-9]", request.json["password"])
        or len(request.json["password"]) not in range(8, 19)
    ):
        error["password"] = """Password must include at least 1 lowercase
        letter, 1 uppercase letter, 1 number and must contain 8 - 18
        characters"""
    elif check_password_hash(user["password"], request.json["password"]):
        error["password"
              ] = "New password should be different from old password"

    if (
        "confirm_password" not in request.json
        or not request.json["confirm_password"]
    ):
        error["confirm_password"] = "This field is required"
    elif (
            request.json["password"]
            and request.json["confirm_password"] != request.json["password"]
    ):
        error["confirm_password"] = """Password and confirm_password password
         does not match"""
    if error != {}:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            **error
        })

    cur.execute("""
        UPDATE "user" SET password = %s WHERE key = %s;
    """, (
        generate_password_hash(request.json["password"], method="scrypt"),
        user["key"]
    ))
    log(
        cur=cur,
        user_key=user["key"],
        action="changed_password",
        entity_type="user",
        entity_key=user["key"]
    )

    cur.execute("DELETE FROM code WHERE user_key = %s;", (user["key"],))

    db_close(con, cur)
    return jsonify({
        "status": 200
    })


@bp.put("/user/photo")
def add_photo():
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    if 'file' not in request.files:
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
    if user["photo"]:
        old_photo = user["photo"]
        storage("delete", user["photo"])

    file_name = storage("save", file)

    cur.execute("""
        UPDATE "user"
        SET photo = %s
        WHERE key = %s
        RETURNING *;
    """, (
        file_name,
        user["key"]
    ))
    user = cur.fetchone()

    log(
        cur=cur,
        user_key=user["key"],
        action="updated_photo",
        entity_type="user",
        entity_key=user["key"],
        misc={
            "from": old_photo,
            "to": file_name
        }
    )

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "user": user_schema(user)
    })


@bp.delete("/user/photo")
def delete_photo():
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    if not user["photo"]:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    storage("delete", user["photo"])

    cur.execute("""
        UPDATE "user"
        SET photo = NULL
        WHERE key = %s
        RETURNING *;
    """, (user["key"],))
    user = cur.fetchone()

    log(
        cur=cur,
        user_key=user["key"],
        action="deleted_photo",
        entity_type="user",
        entity_key=user["key"],
        misc={"photo": user["photo"]}
    )

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "user": user_schema(user)
    })
