from flask import Blueprint, request

from ..tools import log, rate_limit, session
from .get import many

bp = Blueprint("comment", __name__)


@bp.post("/comments/<key>/")
@session(True)
@rate_limit(10, 1)
@log("comment")
def add(cur, user, key):
    cur.execute("""
        SELECT * FROM post WHERE slug = %s OR key = %s;
    """, (key, key))
    post = cur.fetchone()
    if not post:
        return {
            "error": "Invalid request"
        }, 404

    parent_key = request.json.get("parent_key")
    comment = request.json.get("comment", "").strip()

    if parent_key:
        cur.execute("SELECT * FROM comment WHERE key = %s;", (parent_key,))
        parent = cur.fetchone()
        if not parent or parent["parent_key"] is not None:
            return {
                "error": "Invalid request"
            }, 404

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
        INSERT INTO comment (user_key, post_key, comment, parent_key)
        VALUES (%s, %s, %s, %s) RETURNING *;
    """, (user["key"], post["key"], comment, parent_key))
    comment = cur.fetchone()

    _many = many(cur, user, key)

    return {
        "comments": _many["comments"],
        "total_comment": _many["total_comment"],
        "total_page": _many["total_page"],
        "log": {
            "entity_key": comment["key"],
            "action": "comment.create",
            "misc": {
                "post_key": post["key"]
            }
        }
    }, 200


@bp.delete("/comments/<key>")
@session(True)
@rate_limit(20, 1)
@log("comment")
def delete(cur, user, key):
    cur.execute("""
        SELECT * FROM comment WHERE key = %s AND user_key = %s;
    """, (key, user["key"]))
    comment = cur.fetchone()
    if not comment:
        return {
            "error": "Invalid request"
        }, 404

    cur.execute("""DELETE FROM comment WHERE key = %s;""", (comment["key"],))

    _many = many(cur, user, key)

    return {
        "comments": _many["comments"],
        "total_comment": _many["total_comment"],
        "total_page": _many["total_page"],
        "log": {
            "entity_key": comment["key"],
            "misc": {
                "post_key": comment["post_key"]
            }
        }
    }, 200
