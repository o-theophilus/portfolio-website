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

    if "report.resolve" not in user["access"]:
        db_close(con, cur)
        return jsonify({
            "status": 403,
            "error": "unauthorized access"
        })

    cur.execute("SELECT * FROM report WHERE key = %s;", (key,))
    report = cur.fetchone()
    if (
        not report
        or report["reported_key"] == user["key"]
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
        entity_type="report",
        entity_key=report["key"],
    )

    if handle:
        if (
            not report["reported_comment_key"]
            and "user.block" in user["access"]
        ):
            cur.execute("""
                INSERT INTO block (admin_key, user_key, comment)
                VALUES (%s, %s, %s);
            """, (user["key"], report["reported_key"], comment))

            cur.execute("""
                DELETE FROM session WHERE user_key = %s;
            """, (user["key"],))

            log(
                cur=cur,
                user_key=user["key"],
                action="blocked user",
                entity_type="user",
                entity_key=report["reported_key"],
                misc={"comment":  comment}
            )

        elif (
            report["reported_comment_key"]
            and "comment.delete_others" in user["access"]
        ):
            cur.execute(
                "DELETE FROM comment WHERE key = %s;",
                (report["reported_comment_key"],))

            log(
                cur=cur,
                user_key=user["key"],
                action="deleted comment",
                entity_type="comment",
                entity_key=report["reported_comment_key"],
                misc={"comment": comment}
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

    if "report.resolve" not in user["access"]:
        db_close(con, cur)
        return jsonify({
            "status": 403,
            "error": "unauthorized access"
        })

    cur.execute("SELECT * FROM report WHERE key = %s;", (key,))
    report = cur.fetchone()
    if (
        not report
        or report["reported_key"] == user["key"]
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
        entity_type="report",
        entity_key=report["key"],
    )

    reports = get_many(cur)
    db_close(con, cur)
    return reports
