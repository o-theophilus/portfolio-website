from flask import Blueprint, jsonify, request
import re
import os
from .tools import send_mail
from deta import Deta
from .postgres import db_open, db_close
from .postgres import (
    post_table, user_table, log_table, comment_table,
    code_table, setting_table, report_table)
from uuid import uuid4
from .admin import access


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
    elif not re.match(r"\S+@\S+\.\S+", request.json["email"]):
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
        f"{request.json['name']} from Loup",
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


def deta_to_postgres():
    con, cur = db_open()

    source = Deta(os.environ["DETA_KEY"]).Base("live")

    res = source.fetch()
    entities = res.items
    while res.last:
        res = source.fetch(last=res.last)
        entities += res.items

    cur.execute('SELECT * FROM "user" WHERE email = %s;',
                (os.environ["MAIL_USERNAME"],))
    admin = cur.fetchone()

    for x in entities:
        if x["type"] == "post":

            cur.execute("""
                INSERT INTO post (
                    key,
                    status,
                    date,
                    author,
                    title,
                    slug,
                    content,
                    description,
                    photos,
                    tags
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
            """, (
                x["key"],
                "active" if x["status"] == "publish" else x["status"],
                x["created_at"],
                admin["key"],
                x["title"],
                x["slug"],
                x["content"],
                x["description"],
                x["photos"],
                x["tags"]
            ))

            cur.execute("""
                INSERT INTO log (
                    key, date, user_key, action, entity_key, entity_type
                ) VALUES (%s, %s, %s, %s, %s, %s);
            """, (
                uuid4().hex,
                x["created_at"],
                admin["key"],
                "created",
                x["key"],
                "post"
            ))

    db_close(con, cur)
    return jsonify({
        "status": 200
    })


@bp.get("/fix")
def general_fix():
    con, cur = db_open()

    # cur.execute("""
    #     ALTER TABLE item
    #     RENAME COLUMN old_price
    #     TO discount_time;

    #     ALTER TABLE item
    #     ALTER COLUMN discount_time
    #     TYPE VARCHAR(32);

    #     ALTER TABLE item
    #     ALTER COLUMN discount_time
    #     SET DEFAULT 'TRUE';

    #     UPDATE item
    #     SET discount_time = 'TRUE';

    # ALTER TABLE post
    # DROP COLUMN videos;

    # DROP TABLE IF EXISTS rating;

    #     ALTER TABLE order_item
    #     ADD COLUMN price FLOAT DEFAULT 0 NOT NULL;
    # """)

    db_close(con, cur)
    return jsonify({
        "status": 200
    })


def fix_access():
    con, cur = db_open()

    cur.execute("""
            UPDATE "user"
            SET access = %s
            WHERE email = %s;
        """, (
        [f"{x}:{y[0]}" for x in access for y in access[x]],
        os.environ["MAIL_USERNAME"]
    ))

    db_close(con, cur)
    return jsonify({
        "status": 200
    })


def videos():
    con, cur = db_open()

    cur.execute("""
        SELECT
            post.slug,
            post.videos
        FROM post
        WHERE
            post.content ILIKE '{#video}'
    ;""")
    posts = cur.fetchall()

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "posts": posts
    })
