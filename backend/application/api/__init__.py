import os
import re

from flask import Blueprint, jsonify, request

from ..log import log
from ..postgres import db_close, db_open
from ..tools import rate_limit, send_mail, session

bp = Blueprint("api", __name__)


def delete_anonymous(cur, user):
    cur.execute("""
        DELETE FROM "user"
        WHERE status = 'anonymous'
            AND date_created <= NOW() - INTERVAL '30 days'
        RETURNING key;
    """)
    users = cur.fetchall()
    log(
        cur=cur,
        user_key=user["key"],
        action="cleaned up anonymous users",
        entity_key="maintenance",
        entity_type="app",
        misc={
            "deleted_users": [x["key"] for x in users],
        }
    )


@bp.post("/maintenance/anonymous")
@session(True)
@rate_limit(20, 1)
def user_delete_anonymous(cur, user):
    if "maintenance.anonymous" not in user["access"]:
        return jsonify({
            "status": 403,
            "error": "unauthorized access"
        })

    delete_anonymous(cur, user)

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

    delete_anonymous(cur, user)

    cur.execute("""
        DELETE FROM rate_limit_log
        WHERE created_at < NOW() - INTERVAL '1 day';
    """)

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

    db_close(con, cur)
    return jsonify({
        "status": 200
    })


@bp.post("/contact")
@session(False)
@rate_limit(20, 1)
def footer_send_email(cur, user):

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
