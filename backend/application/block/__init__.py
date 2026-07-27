import os

from flask import Blueprint, request

from ..tools import log, rate_limit, session, user_schema
from .get import many

bp = Blueprint("block", __name__)


@bp.post("/blocks/<key>")
@session(True)
@rate_limit(20, 1)
@log("user")
def block(cur, user, key):
    if "user.block" not in user["access"]:
        return {
            "error": "unauthorized access"
        }, 403

    cur.execute("""SELECT * FROM "user" WHERE key = %s;""", (key,))
    user2 = cur.fetchone()
    cur.execute("""SELECT * FROM block WHERE user_key = %s;""", (key,))
    block = cur.fetchone()
    if (
        not user2
        or user2["key"] == user["key"]
        or user2["status"] != "active"
        or user2["email"] == os.environ["MAIL_USERNAME"]
        or block
    ):
        return {
            "error": "Invalid request"
        }, 404

    comment = request.json.get("comment", "").strip()

    error = {}
    if not comment:
        error["comment"] = "This field is required"
    elif len(comment) > 500:
        error["comment"] = "This field cannot exceed 500 characters"
    if error:
        return {
            **error
        }, 422

    cur.execute("""
        INSERT INTO block (admin_key, user_key, comment)
        VALUES (%s, %s, %s);
    """, (user["key"], user2["key"], comment))

    cur.execute("""
        DELETE FROM session WHERE user_key = %s;
    """, (user2["key"],))

    cur.execute("""
        SELECT
            "user".*,
            CASE WHEN block.user_key IS NOT NULL
                THEN true ELSE false END AS blocked
        FROM "user"
        LEFT JOIN block ON "user".key = block.user_key
        WHERE "user".key::TEXT = %s OR "user".username = %s;
    """, (key, key))
    user2 = cur.fetchone()

    return {
        "user": user_schema(user2),
        "log": {
            "entity_key": user2["key"],
            "misc": {
                "comment":  comment
            }
        }
    }, 200


@bp.delete("/blocks/<key>")
@session(True)
@rate_limit(20, 1)
@log("user")
def unblock(cur, user, key):
    if "block.unblock" not in user["access"]:
        return {
            "error": "unauthorized access"
        }, 403

    cur.execute("""SELECT * FROM "user" WHERE key = %s;""", (key,))
    user2 = cur.fetchone()

    if (
        not user2
        or user2["key"] == user["key"]
        or user2["status"] != "active"
        or user2["email"] == os.environ["MAIL_USERNAME"]
    ):
        return {
            "error": "Invalid request"
        }, 404

    comment = request.json.get("comment", "").strip()

    error = {}
    if not comment:
        error["comment"] = "This field is required"
    elif len(comment) > 500:
        error["comment"] = "This field cannot exceed 500 characters"
    if error:
        return {
            **error
        }, 422

    cur.execute("DELETE FROM block WHERE user_key = %s;", (user2["key"],))

    return {
        "blocks": many(cur, user)["blocks"],
        "log": {
            "entity_key": user2["key"],
            "misc": {
                "comment":  comment
            }
        }
    }, 200
