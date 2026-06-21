from flask import Blueprint, request

from ..tools import log, rate_limit, session

bp = Blueprint("report", __name__)


@bp.put("/reports/<key>")
@session(True)
@rate_limit(20, 1)
@log("report")
def resolve(cur, user, key):
    if "report.resolve" not in user["access"]:
        return {
            "status": 403,
            "error": "unauthorized access"
        }, 403

    cur.execute("""
        SELECT * FROM report
        WHERE key = %s AND reported_key != %s AND status = 'active';
    """, (key, user["key"]))
    report = cur.fetchone()
    if not report:
        return {
            "status": 404,
            "error": "Invalid request"
        }, 404

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

    misc = {
        "entity_key": report["key"],
    }

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

            misc["action"] = "block"
            misc["entity_type"] = "user"
            misc["entity_key"] = report["reported_key"]
            misc["comment"] = comment

        elif (
            report["reported_comment_key"]
            and "comment.delete_others" in user["access"]
        ):
            cur.execute(
                "DELETE FROM comment WHERE key = %s;",
                (report["reported_comment_key"],))

            misc["action"] = "delete"
            misc["entity_type"] = "comment"
            misc["entity_key"] = report["reported_comment_key"]
            misc["comment"] = comment

    return {
        "status": 200,
        "log": {
            "misc": misc
        }
    }, 200


@bp.delete("/reports/<key>")
@session(True)
@rate_limit(20, 1)
@log("report")
def dismiss(cur, user, key):
    if "report.resolve" not in user["access"]:
        return {
            "status": 403,
            "error": "unauthorized access"
        }, 403

    cur.execute("""
        SELECT * FROM report
        WHERE key = %s AND reported_key != %s AND status = 'active';
    """, (key, user["key"]))
    report = cur.fetchone()
    if not report:
        return {
            "status": 404,
            "error": "Invalid request"
        }, 404

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

    return {
        "status": 200,
        "log": {
            "entity_key": report["key"],
        }
    }, 200
