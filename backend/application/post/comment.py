from datetime import datetime, timezone

from flask import Blueprint, jsonify, request

from ..log import log
from ..postgres import db_close, db_open
from ..tools import get_session
from .get import get_comments

bp = Blueprint("comment", __name__)


@bp.delete("/comments/<key>")
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

    cur.execute("""DELETE FROM comment WHERE key = %s;""", (comment["key"],))

    log(
        cur=cur,
        user_key=user["key"],
        action="deleted comment",
        entity_key=comment["key"],
        entity_type="comment",
        misc={"post_key": comment["post_key"]}
    )

    comment_resp = get_comments(comment["post_key"], cur)
    db_close(con, cur)
    return comment_resp


@bp.post("/comments/<key>/like")
def like(key):
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    reaction = request.json.get("reaction")

    if reaction not in ["like", "dislike"]:
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    cur.execute("""SELECT * FROM comment WHERE key = %s;""", (key,))
    if not cur.fetchone():
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    cur.execute("""
        SELECT * FROM "like" WHERE user_key = %s AND comment_key = %s;
    """, (user["key"], key))
    user_reaction = cur.fetchone()

    un = ""
    if not user_reaction:
        cur.execute("""
            INSERT INTO "like" (user_key, comment_key, reaction)
            VALUES (%s, %s, %s);
        """, (user["key"], key, reaction))
    elif user_reaction["reaction"] == reaction:
        un = "un"
        cur.execute("""DELETE FROM "like" WHERE key = %s;""",
                    (user_reaction["key"],))
    else:
        cur.execute("""
            UPDATE "like"
            SET date_created = %s, reaction = %s WHERE key = %s;
        """, (datetime.now(timezone.utc), reaction, user_reaction["key"]))

    log(
        cur=cur,
        user_key=user["key"],
        action=f"{un}{reaction}",
        entity_key=key,
        entity_type="comment"
    )

    cur.execute("""
        SELECT
            COUNT(CASE WHEN user_key != %s
                AND reaction = 'like' THEN 1 END) AS others_like,
            COUNT(CASE WHEN user_key != %s
                AND reaction = 'dislike' THEN 1 END) AS others_dislike,
            MAX(CASE WHEN user_key = %s THEN reaction END) AS user_reaction
        FROM "like"
        WHERE comment_key = %s
    """, (user["key"], user["key"], user["key"], key))
    reactions = cur.fetchone()

    db_close(con, cur)
    return jsonify({
        "status": 200,
        **reactions
    })


@bp.post("/comments/<key>/report")
def report(key):
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    comment = request.json.get("comment", "").strip()
    tags = request.json.get("tags")

    if type(tags) is not list:
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

    cur.execute("""SELECT * FROM comment WHERE key = %s;""", (key,))
    reported_comment = cur.fetchone()
    if not reported_comment:
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    cur.execute("""
        INSERT INTO report (reporter_key, reported_comment_key,
            reporter_comment, tags)
        VALUES (%s, %s, %s, %s) RETURNING *;
    """, (user["key"], reported_comment["key"], comment, tags))
    report = cur.fetchone()

    log(
        cur=cur,
        user_key=user["key"],
        action="reported comment",
        entity_key=report["key"],
        entity_type="report",
        misc={"key": reported_comment["key"]}
    )

    db_close(con, cur)
    return jsonify({
        "status": 200
    })
