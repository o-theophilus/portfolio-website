from flask import Blueprint, jsonify, current_app, request
from . import db
import re
import os
from .tools import send_mail
from deta import Deta
from .postgres import db_open, db_close
from .postgres import post_table, user_table, log_table
from uuid import uuid4


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
        current_app.config["DEFAULT_ADMIN"][1],
        current_app.config["DEFAULT_ADMIN"][0],
        f"{request.json['name']} from Designdev",
        message
    )

    return jsonify({
        "status": 200
    })


@bp.get("/cron")
def cron():
    print("cron is running")
    data = db.data()

    for row in data:
        if (
            row["type"] == "user"
            and row["status"] == "anonymous"
        ):
            db.rem(row["key"])

    return jsonify({
        "status": 200
    })


@bp.get("/fix")
def fix():
    con, cur = db_open()

    cur.execute(f"""
        DROP TABLE IF EXISTS "user" CASCADE;
        DROP TABLE IF EXISTS post CASCADE;
        DROP TABLE IF EXISTS log CASCADE;
        {user_table}
        {post_table}
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

    for x in entities:
        if x["type"] == "post":
            cur.execute("""
                INSERT INTO post (
                    key,
                    status,
                    title,
                    slug,
                    content,
                    description,
                    photos,
                    videos,
                    tags
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
            """, (
                x["key"],
                x["status"],
                x["title"],
                x["slug"],
                x["content"],
                x["description"],
                x["photos"],
                x["videos"],
                x["tags"]
            ))

            cur.execute("""
                INSERT INTO log (
                    key, date, user_key, action, entity_key, entity_type
                ) VALUES (%s, %s, %s, %s, %s, %s);
            """, (
                uuid4().hex,
                x["date_c"],
                "admin_key_replace",
                "created",
                x["key"],
                "post"
            ))

    db_close(con, cur)
    return jsonify({
        "status": 200
    })
