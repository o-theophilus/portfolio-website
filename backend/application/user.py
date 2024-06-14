from flask import Blueprint, jsonify, request
from .postgres import db_open, db_close
from .tools import token_to_user, user_schema, send_mail, token_tool
from .log import log
import random
from uuid import uuid4
from datetime import datetime, timedelta
import re
from werkzeug.security import generate_password_hash, check_password_hash
from .storage import storage


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


@bp.put("/user/<key>")
def edit_user(key):
    con, cur = db_open()

    user = token_to_user(cur)
    if not user or user["key"] != key:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    error = {}

    if "name" in request.json:
        if not request.json["name"]:
            error['name'] = "this field is required"
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
            error['phone'] = "this field is required"
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


@bp.post("/user/email/otp")
def send_email_otp():
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    if (
        "email" not in request.json
        or not request.json["email"]
        or "email_template" not in request.json
        or not request.json["email_template"]
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

    cur.execute("DELETE FROM otp WHERE user_key = %s;", (user["key"],))

    otp_1 = str(random.randint(100000, 999999))
    otp_2 = str(random.randint(100000, 999999))
    key_1 = uuid4().hex
    key_2 = uuid4().hex

    cur.execute("""
            INSERT INTO otp (key, user_key, pin, email)
            VALUES (%s, %s, %s, %s), (%s, %s, %s, %s);
        """, (
        key_1,
        user["key"],
        otp_1,
        user['email'],

        key_2,
        user["key"],
        otp_2,
        request.json["email"]
    ))

    log(
        cur=cur,
        user_key=user["key"],
        action="requested",
        entity_key=key_1,
        entity_type="otp",
        misc={"to": user['email']}
    )
    log(
        cur=cur,
        user_key=user["key"],
        action="requested",
        entity_key=key_2,
        entity_type="otp",
        misc={"to": request.json['email']}
    )

    send_mail(
        user["email"],
        "Email Change Confirmation - One-Time Password (OTP)",
        request.json['email_template'].format(otp=otp_1)
    )
    send_mail(
        request.json["email"],
        "Email Change Confirmation - One-Time Password (OTP)",
        request.json['email_template'].format(otp=otp_2)
    )

    db_close(con, cur)
    return jsonify({
        "status": 200
    })


@bp.put("/user/email")
def email():
    con, cur = db_open()

    user = token_to_user(cur)

    error = {}
    cur.execute('SELECT * FROM "user" WHERE email = %s;',
                (request.json["email"],))
    email_exist = cur.fetchone()

    if "email" not in request.json or not request.json["email"]:
        error["email"] = "this field is required"
    elif not re.match(r"\S+@\S+\.\S+", request.json["email"]):
        error["email"] = "Please enter a valid email"
    elif user["email"] == request.json["email"]:
        error["email"] = "please use a different email form your current email"
    elif email_exist:
        error["email"] = "email is already in use"

    if "otp_1" not in request.json or not request.json["otp_1"]:
        error["otp_1"] = "this field is required"
    else:
        cur.execute("""
            SELECT otp.*, log.date
            FROM otp
            LEFT JOIN log ON otp.key = log.entity_key
            WHERE
                otp.user_key = %s
                AND otp.pin = %s
                AND otp.email = %s
                AND log.entity_type = 'otp'
                AND log.action = 'requested';
        """, (
            user['key'],
            request.json["otp_1"],
            user['email']
        ))
        otp_1 = cur.fetchone()

        if not otp_1:
            error["otp_1"] = "invalid OTP"
        elif datetime.now() - otp_1["date"] > timedelta(minutes=15):
            cur.execute("DELETE FROM otp WHERE user_key = %s;", (user["key"],))
            error["otp_1"] = "invalid OTP"

    if "otp_2" not in request.json or not request.json["otp_2"]:
        error["otp_2"] = "this field is required"
    else:
        cur.execute("""
            SELECT otp.*, log.date
            FROM otp
            LEFT JOIN log ON otp.key = log.entity_key
            WHERE
                otp.user_key = %s
                AND otp.pin = %s
                AND otp.email = %s
                AND log.entity_type = 'otp'
                AND log.action = 'requested';
        """, (
            user['key'],
            request.json["otp_2"],
            request.json["email"]
        ))
        otp_2 = cur.fetchone()

        if not otp_2:
            error["otp_2"] = "invalid OTP"
        elif datetime.now() - otp_2["date"] > timedelta(minutes=15):
            cur.execute("DELETE FROM otp WHERE user_key = %s;", (user["key"],))
            error["otp_2"] = "invalid OTP"

    if error != {}:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            **error
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
        UPDATE "user"
        SET email = %s
        WHERE key = %s
        RETURNING *;
    """, (
        request.json["email"],
        user["key"]
    ))
    user = cur.fetchone()
    cur.execute("DELETE FROM otp WHERE user_key = %s;", (user["key"],))

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "user": user_schema(user)
    })


@bp.post("/user/password/otp")
def send_password_otp():
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

    cur.execute("DELETE FROM otp WHERE user_key = %s;", (user["key"],))

    otp = str(random.randint(100000, 999999))
    key = uuid4().hex

    cur.execute("""
            INSERT INTO otp (key, user_key, pin, email)
            VALUES (%s, %s, %s, %s);
        """, (
        key,
        user["key"],
        otp,
        user["email"]
    ))

    log(
        cur=cur,
        user_key=user["key"],
        action="requested",
        entity_key=key,
        entity_type="otp",
        misc={"to": user['email']}
    )

    send_mail(
        user["email"],
        "Password Change Confirmation - One-Time Password (OTP)",
        request.json['email_template'].format(
            otp=otp
        )
    )

    db_close(con, cur)
    return jsonify({
        "status": 200
    })


@bp.put("/user/password")
def password():
    con, cur = db_open()

    user = token_to_user(cur)

    error = {}
    if "password" not in request.json or not request.json["password"]:
        error["password"] = "this field is required"
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
        error["confirm_password"] = "this field is required"
    elif (
            request.json["password"]
            and "password" not in error
            and request.json["confirm_password"] != request.json["password"]
    ):
        error["confirm_password"] = """Password and confirm_password password
         does not match"""

    if "otp" not in request.json or not request.json["otp"]:
        error["otp"] = "this field is required"
    else:
        cur.execute("""
            SELECT otp.*, log.date
            FROM otp
            LEFT JOIN log ON
                otp.key = log.entity_kty
            WHERE
                otp.user = %s
                AND otp.pin = %s
                AND otp.email = %s;
                AND log.entity_type = 'otp'
                AND log.action = 'requested'
        """, (
            user['key'],
            request.json["otp"],
            user["email"]
        ))
        otp = cur.fetchone()

        if not otp:
            error["otp"] = "invalid OTP"
        elif datetime.now() - otp["date"] > timedelta(minutes=15):
            cur.execute("DELETE FROM otp WHERE user_key = %s;", (user["key"],))
            error["otp"] = "invalid OTP"

    if error != {}:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            **error
        })

    log(
        cur=cur,
        user_key=user["key"],
        action="changed_password",
        entity_type="user"
    )

    cur.execute("""
        UPDATE "user"
        SET password = %s
        WHERE key = %s;
    """, (
        generate_password_hash(request.json["password"], method="scrypt"),
        user["key"]
    ))
    cur.execute("DELETE FROM otp WHERE user_key = %s;", (user["key"],))

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
        error["note"] = "this field is required"
    if "password" not in request.json or not request.json["password"]:
        error["password"] = "this field is required"

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
        SET status = 'deleted', login = %s, permissions = %s
        WHERE key = %s;
    """, (
        False,
        [],
        user["key"]
    ))

    cur.execute("""
        INSERT INTO "user" (key, version, email, password, setting_theme)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING *;
    """, (
        uuid4().hex, uuid4().hex, uuid4().hex,
        generate_password_hash(uuid4().hex, method="scrypt"),
        user["setting_theme"]
    ))
    anon_user = cur.fetchone()

    log(
        cur=cur,
        user_key=user["key"],
        action="deleted_account",
        entity_type="user",
        misc={"note": request.json["note"]}
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
