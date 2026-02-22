import os
import re

from flask import Blueprint, jsonify, request

from ..log import log
from ..postgres import db_close, db_open
from ..tools import get_session, send_mail

bp = Blueprint("api", __name__)


def delete_session(cur, user_key):
    cur.execute("""
        DELETE FROM session
        WHERE (
                remember = FALSE
                AND date_updated <= NOW() - INTERVAL '3 days'
            ) OR (
                remember = TRUE
                AND date_updated <= NOW() - INTERVAL '14 days'
            )
        RETURNING key;
    """)
    sessions = cur.fetchall()
    log(
        cur=cur,
        user_key=user_key,
        action="cleaned up expired sessions",
        entity_key="maintenance",
        entity_type="app",
        misc={
            "deleted_sessions": [x["key"] for x in sessions],
        }
    )


def delete_anonymous(cur, user_key):
    cur.execute("""
        DELETE FROM "user"
        WHERE status = 'anonymous'
            AND date_created <= NOW() - INTERVAL '30 days'
        RETURNING key;
    """)
    users = cur.fetchall()
    log(
        cur=cur,
        user_key=user_key,
        action="cleaned up anonymous users",
        entity_key="maintenance",
        entity_type="app",
        misc={
            "deleted_users": [x["key"] for x in users],
        }
    )


@bp.post("/maintenance/session")
def user_delete_session():
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    if "maintenance:session" not in user["access"]:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "unauthorized access"
        })

    delete_session(cur, user["key"])

    db_close(con, cur)
    return jsonify({
        "status": 200
    })


@bp.post("/maintenance/anonymous")
def user_delete_anonymous():
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    if "maintenance:anonymous" not in user["access"]:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "unauthorized access"
        })

    delete_session(cur, user["key"])

    db_close(con, cur)
    return jsonify({
        "status": 200
    })


@bp.get("/cron")
def cron():
    con, cur = db_open()

    cur.execute("""
        SELECT key FROM "user" WHERE email = %s;
    """, (os.environ["MAIL_USERNAME"],))
    user = cur.fetchone()

    delete_session(cur, user["key"])
    delete_anonymous(cur, user["key"])

    db_close(con, cur)
    return jsonify({
        "status": 200
    })


@bp.post("/contact")
def footer_send_email():

    email_template = request.json.get("email_template")
    name = request.json.get("name")
    email = request.json.get("email")
    message = request.json.get("message")

    if not email_template:
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    error = {}
    if not name:
        error["name"] = "This field is required"
    elif len(name) > 100:
        error["name"] = "This field cannot exceed 100 characters"

    if not email:
        error["email"] = "This field is required"
    elif not re.match(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", email):
        error["email"] = "Invalid email address"
    elif len(email) > 255:
        error["email"] = "This field cannot exceed 255 characters"

    if not message:
        error["message"] = "This field is required"
    if error:
        return jsonify({
            "status": 400,
            **error
        })

    message = email_template.format(
        name=name, email=email, message=message)

    send_mail(
        os.environ["MAIL_USERNAME"],
        f"{name} from Theophilus Portfolio Website",
        message
    )

    return jsonify({
        "status": 200
    })
