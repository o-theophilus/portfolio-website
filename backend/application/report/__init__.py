from flask import Blueprint, jsonify, request

from ..log import log
from ..postgres import db_close, db_open
from ..tools import get_session

bp = Blueprint("report", __name__)


@bp.post("/report")
def create():
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    entity_key = request.json.get("entity_key")
    entity_type = request.json.get("entity_type")
    comment = request.json.get("comment")
    tags = request.json.get("tags")

    if (
        not entity_key
        or entity_key == user["key"]
        or not entity_type
        or entity_type not in ["user", "comment"]
        or type(tags) is not list
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

    cur.execute(f"""
        SELECT * FROM "{entity_type}" WHERE key = %s;
    """, (entity_key,))
    entity = cur.fetchone()
    if not entity:
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    if entity_type == "user":
        column = "reported_key"
    if entity_type == "comment":
        column = "comment_key"

    cur.execute(f"""
        INSERT INTO report (reporter_key, {column}, comment, tags)
        VALUES (%s, %s, %s, %s) RETURNING *;
    """, (user["key"], entity["key"], comment, tags))
    report = cur.fetchone()

    log(
        cur=cur,
        user_key=user["key"],
        action="created report",
        entity_key=report["key"],
        entity_type="report",
        misc={
            "key": entity_key,
            "type": entity_type
        }
    )

    db_close(con, cur)
    return jsonify({
        "status": 200
    })


@bp.put("/report/<key>")
def resolve(key):
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    if "report:resolve" not in user["access"]:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "unauthorized access"
        })

    cur.execute("SELECT * FROM report WHERE key = %s;", (key,))
    report = cur.fetchone()
    if (
        not report
        or report["reported_key"] == user["key"]
        or report["status"] == "resolved"
    ):
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    comment = request.json.get("comment")
    status = request.json.get("status")
    delete_comment = request.json.get("delete_comment", False)

    error = {}
    if not comment:
        error["comment"] = "This field is required"
    elif len(comment) > 500:
        error["comment"] = "This field cannot exceed 500 characters"

    if not status or status not in ["resolved", "dismissed"]:
        error["status"] = "This field is required"
    if error:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            **error
        })

    cur.execute("""
        UPDATE report
        SET status = %s, date_resolved = now(),
        resolver_key = %s, resolve_comment = %s,
        WHERE key = %s;
    """, (status, user["key"], comment, key))

    if report["comment_key"]:
        entity_type = "comment"
        entity_key = report["comment_key"]
    elif report["reported_key"]:
        entity_type = "user"
        entity_key = report["reported_key"]

    log(
        cur=cur,
        user_key=user["key"],
        action="resolved report",
        entity_key=report["key"],
        entity_type="report",
        misc={
            "entity_key": entity_key,
            "entity_type": entity_type,
        }
    )

    if report["comment_key"] and delete_comment:
        cur.execute(
            "DELETE FROM comment WHERE key = %s RETURNING *;",
            (report["comment_key"],))
        comment = cur.fetchone()

        log(
            cur=cur,
            user_key=user["key"],
            action="deleted comment",
            entity_key=comment["key"],
            entity_type="comment",
            misc={"post_key": comment["post_key"]}
        )

    db_close(con, cur)
    return jsonify({
        "status": 200
    })
