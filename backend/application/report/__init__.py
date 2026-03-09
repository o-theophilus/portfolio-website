from flask import Blueprint, jsonify, request

from ..log import log
from ..postgres import db_close, db_open
from ..tools import get_session
from .get import get_many

bp = Blueprint("report", __name__)


@bp.put("/reports/<key>")
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
            "status": 403,
            "error": "unauthorized access"
        })

    cur.execute("SELECT * FROM report WHERE key = %s;", (key,))
    report = cur.fetchone()
    if (
        not report
        or report["entity_key"] == user["key"]
        or report["status"] != "active"
    ):
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    comment = request.json.get("comment", "").strip()
    handle = request.json.get("handle", False)

    error = {}
    if not comment:
        error["comment"] = "This field is required"
    elif len(comment) > 500:
        error["comment"] = "This field cannot exceed 500 characters"

    cur.execute("""
        UPDATE report
        SET status = 'resolved', date_resolved = now(),
        resolver_key = %s, resolver_comment = %s
        WHERE key = %s;
    """, (user["key"], comment, key))

    log(
        cur=cur,
        user_key=user["key"],
        action="resolved report",
        entity_key=report["key"],
        entity_type="report",
        misc={
            "entity_key": report["entity_key"],
            "entity_type": report["entity_type"],
        }
    )

    if handle:
        if (
            report["entity_type"] == "user"
            and "user:block" in user["access"]
        ):
            cur.execute("""
                INSERT INTO block (admin_key, user_key, comment)
                VALUES (%s, %s, %s);
            """, (user["key"], report["entity_key"], comment))

            cur.execute("""
                DELETE FROM session WHERE user_key = %s;
            """, (user["key"],))

            log(
                cur=cur,
                user_key=user["key"],
                action="blocked",
                entity_key=report["entity_key"],
                entity_type="user",
                misc={"comment":  comment}
            )

        elif (
            report["entity_type"] == "comment"
            and "comment:delete_others" in user["access"]
        ):
            cur.execute(
                "DELETE FROM comment WHERE key = %s RETURNING *;",
                (report["entity_key"],))
            _comment = cur.fetchone()

            log(
                cur=cur,
                user_key=user["key"],
                action="deleted comment",
                entity_key=_comment["key"],
                entity_type="comment",
                misc={
                    "item_key": _comment["item_key"],
                    "comment": comment
                }
            )

    reports = get_many(cur)
    db_close(con, cur)
    return reports


@bp.delete("/reports/<key>")
def dismiss(key):
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    if "report:resolve" not in user["access"]:
        db_close(con, cur)
        return jsonify({
            "status": 403,
            "error": "unauthorized access"
        })

    cur.execute("SELECT * FROM report WHERE key = %s;", (key,))
    report = cur.fetchone()
    if (
        not report
        or report["entity_key"] == user["key"]
        or report["status"] != "active"
    ):
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    comment = request.json.get("comment", "").strip()

    error = {}
    if not comment:
        error["comment"] = "This field is required"
    elif len(comment) > 500:
        error["comment"] = "This field cannot exceed 500 characters"

    cur.execute("""
        UPDATE report
        SET status = 'dismissed', date_resolved = now(),
        resolver_key = %s, resolver_comment = %s
        WHERE key = %s;
    """, (user["key"], comment, key))

    log(
        cur=cur,
        user_key=user["key"],
        action="dismissed report",
        entity_key=report["key"],
        entity_type="report",
        misc={
            "entity_key": report["entity_key"],
            "entity_type": report["entity_type"],
        }
    )

    reports = get_many(cur)
    db_close(con, cur)
    return reports
