from flask import Blueprint, jsonify, request
from ...tools import get_session
from ...postgres import db_close, db_open
from ...log import log
from .get import get_many

bp = Blueprint("comment", __name__)


@bp.post("/comment/<key>")
def create(key):
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    cur.execute("""
        SELECT * FROM post WHERE slug = %s OR key = %s;
    """, (key, key))
    post = cur.fetchone()
    if not post:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    parent_key = request.json.get("parent_key")
    if parent_key:
        cur.execute("SELECT * FROM comment WHERE key = %s;", (parent_key,))
        if not cur.fetchone():
            db_close(con, cur)
            return jsonify({
                "status": 400,
                "error": "Invalid request"
            })

    comment = request.json.get("comment")
    error = {}
    if not comment:
        error["comment"] = "This field is required"
    elif len(comment) > 500:
        error["comment"] = "This field cannot exceed 500 characters"
    if error != {}:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            **error
        })

    cur.execute("""
        INSERT INTO comment (user_key, post_key, comment, parent_key)
        VALUES (%s, %s, %s, %s) RETURNING *;
    """, (user["key"], post["key"], comment, parent_key))
    comment = cur.fetchone()

    log(
        cur=cur,
        user_key=user["key"],
        action="created",
        entity_key=comment["key"],
        entity_type="comment",
        misc={"post_key": post["key"]}
    )

    items = get_many(post["key"], cur)
    db_close(con, cur)
    return items


@bp.delete("/comment/<key>")
def delete(key):
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    cur.execute("""
        SELECT * FROM comment WHERE key = %s AND user_key = %s;
    """, (key, user["key"]))
    comment = cur.fetchone()

    if not comment:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    cur.execute("""
        DELETE FROM "like"
        WHERE entity_type = 'comment' entity_key = %s;
    """, (comment["key"],))

    cur.execute("""
        WITH RECURSIVE to_delete AS (
            SELECT key
            FROM comment
            WHERE key = %s

            UNION ALL

            SELECT c.key
            FROM comment c
            INNER JOIN to_delete td ON c.parent_key = td.key
        )
        DELETE FROM comment
        WHERE key IN (SELECT key FROM to_delete);
    """, (comment["key"],))

    log(
        cur=cur,
        user_key=user["key"],
        action="deleted",
        entity_key=comment["key"],
        entity_type="comment",
        misc={"post_key": comment["post_key"]}
    )

    items = get_many(comment["post_key"], cur)
    db_close(con, cur)
    return items
