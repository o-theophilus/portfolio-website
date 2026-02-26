import os

from flask import Blueprint, jsonify, request

from ...log import log
from ...postgres import db_close, db_open
from ...tools import get_session, user_schema
from .get import get_many

bp = Blueprint("block", __name__)


@bp.post("/block/<key>")
def block(key):
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    me = session["user"]

    comment = request.json.get("comment")

    if "block:block" not in me["access"]:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "unauthorized access"
        })

    cur.execute("""SELECT * FROM "user" WHERE key = %s;""", (key,))
    user = cur.fetchone()

    cur.execute("""SELECT * FROM block WHERE user_key = %s;""", (key,))
    block = cur.fetchone()

    if (
        not user
        or user["key"] == me["key"]
        or user["status"] != "confirmed"
        or user["email"] == os.environ["MAIL_USERNAME"]
        or block
    ):
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    error = {}
    if not comment:
        error["comment"] = "This field is required"
    elif len(comment) > 500:
        error["comment"] = "This field cannot exceed 500 characters"
    if error:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            **error
        })

    cur.execute("""
        INSERT INTO block (admin_key, user_key, comment)
        VALUES (%s, %s, %s);
    """, (me["key"], user["key"], comment))

    cur.execute("""
        DELETE FROM session WHERE user_key = %s;
    """, (user["key"],))

    log(
        cur=cur,
        user_key=me["key"],
        action="blocked",
        entity_key=user["key"],
        entity_type="user",
        misc={"comment":  comment}
    )

    cur.execute("""
        SELECT
            "user".*,
            CASE WHEN block.user_key IS NOT NULL
                THEN true ELSE false END AS blocked
        FROM "user"
        LEFT JOIN block ON "user".key = block.user_key
        WHERE "user".key::TEXT = %s OR "user".username = %s;
    """, (key, key))
    user = cur.fetchone()

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "user": user_schema(user)
    })


@bp.delete("/block/<key>")
def unblock(key):
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    me = session["user"]

    comment = request.json.get("comment")

    if "block:unblock" not in me["access"]:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "unauthorized access"
        })

    cur.execute("""SELECT * FROM "user" WHERE key = %s;""", (key,))
    user = cur.fetchone()

    if (
        not user
        or user["key"] == me["key"]
        or user["status"] != "confirmed"
        or user["email"] == os.environ["MAIL_USERNAME"]
    ):
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    error = {}
    if not comment:
        error["comment"] = "This field is required"
    elif len(comment) > 500:
        error["comment"] = "This field cannot exceed 500 characters"
    if error:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            **error
        })

    cur.execute("DELETE FROM block WHERE user_key = %s;", (user["key"],))

    log(
        cur=cur,
        user_key=me["key"],
        action="unblocked",
        entity_key=user["key"],
        entity_type="user",
        misc={"comment":  comment}
    )

    blocks = get_many(cur).json["blocks"]

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "blocks": blocks
    })
