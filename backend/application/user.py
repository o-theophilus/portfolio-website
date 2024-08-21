from flask import Blueprint, jsonify, request
from .postgres import db_open, db_close
from .tools import (
    token_to_user, user_schema, send_mail, token_tool,
    generate_code, check_code)
from .log import log
import re
import os
from werkzeug.security import generate_password_hash, check_password_hash
from .storage import storage
from .account import anon


bp = Blueprint("user", __name__)


@bp.post("/user/theme")
def theme():
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    theme = "light"
    if user["setting_theme"] == "light":
        theme = "dark"

    cur.execute("""
        UPDATE "user"
        SET setting_theme = %s
        WHERE key = %s;
    """, (
        theme,
        user["key"]
    ))

    log(
        cur=cur,
        user_key=user["key"],
        action="changed_theme",
        entity_type="user",
        misc={
            "from": user["setting_theme"],
            "to": theme
        }
    )

    user["setting_theme"] = theme

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "user": user
    })


# TODO: admin can edit name and photo
# TODO: SUPER USER CANNOT BE EDITED
@bp.put("/user/<key>")
def edit_user(key):
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    # if user["key"] != key:
    #     if "user:edit_name" not in user["access"]:
    #         db_close(con, cur)
    #         return jsonify({
    #             "status": 400,
    #             "error": "unauthorized access"
    #         })
    #     else:
    #         cur.execute("""SELECT * FROM "user" WHERE key = %s;""", (key,))
    #         user = cur.fetchone()

    #         if not user:
    #             db_close(con, cur)
    #             return jsonify({
    #                 "status": 400,
    #                 "error": "invalid request"
    #             })

    error = {}

    if "name" in request.json:
        if not request.json["name"]:
            error['name'] = "cannot be empty"
        elif request.json["name"] == user["name"]:
            error['name'] = "no change"
        else:
            cur.execute("""
                UPDATE "user"
                SET name = %s
                WHERE key = %s;
            """, (
                request.json["name"],
                user["key"]
            ))

    if "phone" in request.json:
        if not request.json["phone"]:
            error['phone'] = "cannot be empty"
        elif request.json["phone"] == user["phone"]:
            error['phone'] = "no change"
        else:
            cur.execute("""
                UPDATE "user"
                SET phone = %s
                WHERE key = %s;
            """, (
                request.json["phone"],
                user["key"]
            ))

    if error != {}:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            **error
        })

    cur.execute("""
        SELECT * FROM "user" WHERE key = %s;
    """, (user["key"],))
    user = cur.fetchone()

    log(
        cur=cur,
        user_key=user["key"],
        action="edited",
        entity_type="user",
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

    user = token_to_user(cur)
    if not user:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    if (
        "email_template" not in request.json
        or not request.json["email_template"]
    ):
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
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

    user = token_to_user(cur)
    if not user:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

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

    user = token_to_user(cur)
    if not user:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    error = check_code(cur, user["key"], user["email"], "code_1")
    if error:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    if (
        "email_template" not in request.json
        or not request.json["email_template"]
    ):
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    error = None
    if "email" not in request.json or not request.json["email"]:
        error = "cannot be empty"
    elif not re.match(r"\S+@\S+\.\S+", request.json["email"]):
        error = "invalid email"
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

    user = token_to_user(cur)
    if not user:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    error = check_code(cur, user["key"], user["email"], "code_1")
    if error:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    if (
        "email" not in request.json or not request.json["email"]
        or not re.match(r"\S+@\S+\.\S+", request.json["email"])
    ):
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    if user["email"] == request.json["email"]:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    cur.execute('SELECT * FROM "user" WHERE email = %s;',
                (request.json["email"],))
    exist = cur.fetchone()
    if exist:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    error = check_code(cur, user["key"], request.json["email"], "code_2")
    if error:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
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

    user = token_to_user(cur)
    if not user:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    if (
        "email_template" not in request.json
        or not request.json["email_template"]
    ):
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
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

    user = token_to_user(cur)
    if not user:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

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

    user = token_to_user(cur)
    if not user:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    error = check_code(cur, user["key"], user["email"])
    if error:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    error = {}
    if "password" not in request.json or not request.json["password"]:
        error["password"] = "cannot be empty"
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
        error["confirm_password"] = "cannot be empty"
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
        entity_type="user"
    )

    cur.execute("DELETE FROM code WHERE user_key = %s;", (user["key"],))

    db_close(con, cur)
    return jsonify({
        "status": 200
    })


@ bp.delete("/user")
def delete():
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    error = {}

    if "note" not in request.json or not request.json["note"]:
        error["note"] = "cannot be empty"
    if "password" not in request.json or not request.json["password"]:
        error["password"] = "cannot be empty"

    if error != {}:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            **error
        })

    if not check_password_hash(user["password"], request.json["password"]):
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "incorrect password"
        })

    cur.execute("""
        UPDATE "user"
        SET status = 'deleted', login = %s, access = %s
        WHERE key = %s;
    """, (
        False,
        [],
        user["key"]
    ))

    anon_user = anon(cur)

    log(
        cur=cur,
        user_key=user["key"],
        action="deleted_account",
        entity_type="account",
        misc={"note": request.json["note"]}
    )
    log(
        cur=cur,
        user_key=anon_user["key"],
        action="created",
        entity_type="account",
        misc={
            "from": user["key"],
            "name": user["name"]
        }
    )

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "user": user_schema(anon_user),
        "token": token_tool().dumps(anon_user["key"])
    })


@bp.put("/user/photo")
def add_photo():
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    if 'file' not in request.files:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    file = request.files["file"]
    media, format = file.content_type.split("/")
    if media != "image" or format in ['svg+xml', 'x-icon']:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid file"
        })

    old_photo = None
    if user["photo"]:
        old_photo = user["photo"]
        storage(user["photo"], delete=True)

    file_name = storage(file)

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

    user = token_to_user(cur)
    if not user:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    if user["photo"]:
        storage(user["photo"].split("/")[-1], delete=True)

        cur.execute("""
            UPDATE "user"
            SET photo = NULL
            WHERE key = %s;
        """, (user["key"],))

        log(
            cur=cur,
            user_key=user["key"],
            action="deleted_photo",
            entity_type="user",
            misc={"photo": user["photo"]}
        )

    db_close(con, cur)
    return jsonify({
        "status": 200
    })
