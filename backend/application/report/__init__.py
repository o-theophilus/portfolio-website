from flask import Blueprint, request

from ..tools import log, rate_limit, session
from .get import many

bp = Blueprint("report", __name__)


# TODO: user report and comment report can be unified
@bp.post("/reports/user/<key>")
@session(True)
@rate_limit(20, 1)
@log("report")
def report_user(cur, user, key):
    cur.execute("""SELECT * FROM "user" WHERE key = %s;""", (key,))
    user2 = cur.fetchone()
    if not user2:
        return {
            "error": "Invalid request"
        }, 404

    comment = request.json.get("comment", "").strip()
    tags = request.json.get("tags")

    if type(tags) is not list:
        return {
            "error": "Invalid request"
        }, 422

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
        INSERT INTO report (reporter_key, reporter_comment,
            tags, reported_key)
        VALUES (%s, %s, %s, %s) RETURNING *;
    """, (user["key"], comment, tags, user2["key"]))
    report = cur.fetchone()

    return {
        "log": {
            "entity_key": report["key"],
            "misc": {
                "entity_key": user2["key"],
                "entity_type": "user"
            }

        }
    }, 200


@bp.post("/reports/comment/<key>")
@session(True)
@rate_limit(10, 1)
@log("report")
def report_comment(cur, user, key):
    cur.execute("""SELECT * FROM comment WHERE key = %s;""", (key,))
    reported_comment = cur.fetchone()
    if not reported_comment:
        return {
            "error": "Invalid request"
        }, 404

    comment = request.json.get("comment", "").strip()
    tags = request.json.get("tags")

    if type(tags) is not list:
        return {
            "error": "Invalid request"
        }, 422

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
        INSERT INTO report (reporter_key, reporter_comment, tags,
            reported_key, reported_comment_key)
        VALUES (%s, %s, %s, %s, %s) RETURNING *;
    """, (
        user["key"], comment, tags,
        reported_comment["user_key"], reported_comment["key"])
    )
    report = cur.fetchone()

    return {
        "log": {
            "entity_key": report["key"],
            "misc": {
                "entity_key": reported_comment["key"],
                "entity_type": "comment"
            }
        }
    }, 200


@bp.put("/reports/<key>")
@session(True)
@rate_limit(20, 1)
@log("report")
def resolve(cur, user, key):
    if "report.resolve" not in user["access"]:
        return {
            "error": "unauthorized access"
        }, 403

    cur.execute("""
        SELECT * FROM report
        WHERE key = %s AND reported_key != %s AND status = 'active';
    """, (key, user["key"]))
    report = cur.fetchone()
    if not report:
        return {
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

            cur.execute("""
                INSERT INTO log (
                    user_key, action, entity_type, entity_key, misc
                ) VALUES (%s, 'user_block.block', 'user', %s, %s);
            """, (
                user["key"], report["reported_key"],
                {"comment":  comment}
            ))

        elif (
            report["reported_comment_key"]
            and "comment.delete_others" in user["access"]
        ):
            cur.execute(
                "DELETE FROM comment WHERE key = %s;",
                (report["reported_comment_key"],))

            cur.execute("""
                INSERT INTO log (
                    user_key, action, entity_type, entity_key, misc
                ) VALUES (%s, 'comment.delete', 'comment', %s, %s);
            """, (
                user["key"], report["reported_comment_key"],
                {"comment":  comment}
            ))

    _many = many(cur, user)

    return {
        "reports": _many["reports"],
        "total_page": _many["total_page"],
        "log": {
            "misc": {
                "entity_key": report["key"]
            }
        }
    }, 200


@bp.delete("/reports/<key>")
@session(True)
@rate_limit(20, 1)
@log("report")
def dismiss(cur, user, key):
    if "report.resolve" not in user["access"]:
        return {
            "error": "unauthorized access"
        }, 403

    cur.execute("""
        SELECT * FROM report
        WHERE key = %s AND reported_key != %s AND status = 'active';
    """, (key, user["key"]))
    report = cur.fetchone()
    if not report:
        return {
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

    _many = many(cur, user)

    return {
        "reports": _many["reports"],
        "total_page": _many["total_page"],
        "log": {
            "entity_key": report["key"],
        }
    }, 200
