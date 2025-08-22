from flask import Blueprint, jsonify, request
import re
import os
from .tools import send_mail
from .postgres import db_open, db_close
from .postgres import (
    post_table, user_table, log_table, comment_table,
    code_table, setting_table, report_table)
from .admin import access
import psycopg2
import psycopg2.extras
from werkzeug.security import generate_password_hash

bp = Blueprint("api", __name__)


@bp.post("/contact")
def send_email():

    if (
        "email_template" not in request.json
        or not request.json["email_template"]
    ):
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    error = {}

    if "name" not in request.json or not request.json["name"]:
        error["name"] = "cannot be empty"
    if "email" not in request.json or not request.json["email"]:
        error["email"] = "cannot be empty"
    elif not re.match(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", request.json["email"]):
        error["email"] = "invalid email"
    if "message" not in request.json or not request.json["message"]:
        error["message"] = "cannot be empty"

    if error != {}:
        return jsonify({
            "status": 400,
            **error
        })

    message = request.json['email_template'].format(
        name=request.json["name"],
        email=request.json["email"],
        message=request.json["message"])

    send_mail(
        os.environ["MAIL_USERNAME"],
        f"{request.json['name']} from Theophilus Portfolio Website",
        message
    )

    return jsonify({
        "status": 200
    })


@bp.get("/cron")
def cron():
    print("cron is running")

    return jsonify({
        "status": 200
    })


def create_tables():
    con, cur = db_open()

    cur.execute(f"""
        DROP TABLE IF EXISTS setting CASCADE;
        DROP TABLE IF EXISTS "user" CASCADE;
        DROP TABLE IF EXISTS post CASCADE;
        DROP TABLE IF EXISTS comment CASCADE;
        DROP TABLE IF EXISTS report CASCADE;
        DROP TABLE IF EXISTS code CASCADE;
        DROP TABLE IF EXISTS log CASCADE;
        {setting_table}
        {user_table}
        {post_table}
        {comment_table}
        {report_table}
        {code_table}
        {log_table}
    """)

    db_close(con, cur)
    return jsonify({
        "status": 200
    })


def copy_table():
    con1 = psycopg2.connect("postgres://admin:admin@localhost/loup")
    cur1 = con1.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cur1.execute("""SELECT * FROM post;""")
    posts = cur1.fetchall()

    con1.commit()
    cur1.close()
    con1.close()

    con2 = psycopg2.connect(
        "postgresql://postgres.viwdxqnhuoozxslwkbmr:qulWftcsaaIeB8bL@" +
        "aws-0-eu-central-1.pooler.supabase.com:6543/postgres")
    cur2 = con2.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cur2.execute("""
            INSERT INTO "user" (key, status, name, email, password, access)
            VALUES (%s, %s, %s, %s, %s, %s);
        """, (
        "c7a9b3b4b68a4cc5afbc858b1b703ab2",
        "confirmed",
        "Theophilus",
        "theophilus.ogbolu@protonmail.com",
        generate_password_hash(
            os.environ["MAIL_PASSWORD"], method="scrypt"),
        [f"{x}:{y[0]}" for x in access for y in access[x]]
    ))

    for x in posts:
        cur2.execute("""
            INSERT INTO post (
                key,
                status,
                date,
                author_key,
                title,
                slug,
                content,
                description,
                photo
                --files,
                --tags,
                --"like",
                --dislike,
                --ratings
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
        """, (
            x["key"],
            x["status"],
            x["date"],
            x["author_key"],
            x["title"],
            x["slug"],
            x["content"],
            x["description"],
            x["photo"],
            # Json(x["files"]),
            # Json(x["tags"]),
            # Json(x["like"]),
            # Json(x["dislike"]),
            # Json(x["ratings"]),
        ))

    con2.commit()
    cur2.close()
    con2.close()

    return jsonify({
        "status": 200
    })


def fix_access():
    con, cur = db_open()

    cur.execute("""
            UPDATE "user" SET access = %s WHERE email = %s;
        """, (
        [f"{x}:{y[0]}" for x in access for y in access[x]],
        os.environ["MAIL_USERNAME"]
    ))

    db_close(con, cur)
    return jsonify({
        "status": 200
    })


def quick_fix():
    con, cur = db_open()

    cur.execute("""
        DELETE FROM log WHERE key = 'ce2873fdca1d4883b6a3b6badf4ca82c';
    """)

    db_close(con, cur)
    return jsonify({
        "status": 200
    })


# @bp.get("/fix")
def general_fix():
    con, cur = db_open()

    cur.execute("""
        ALTER TABLE log
        ALTER COLUMN date TYPE TIMESTAMPTZ
        USING date AT TIME ZONE 'UTC';
    """)

    cur.execute("""
        ALTER TABLE post
        ALTER COLUMN date TYPE TIMESTAMPTZ
        USING date AT TIME ZONE 'UTC';
    """)

    db_close(con, cur)
    return jsonify({
        "status": 200
    })
