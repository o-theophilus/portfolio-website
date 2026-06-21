import os
import re

from flask import Blueprint, request
from psycopg2.extras import Json

from ..postgres import db_close, db_open
from ..tools import rate_limit, send_mail, session

bp = Blueprint("api", __name__)


def delete_anonymous_user(cur, user):
    cur.execute("""
        DELETE FROM "user"
        WHERE status = 'anonymous'
            AND date_created <= NOW() - INTERVAL '30 days'
        RETURNING key;
    """)
    users = cur.fetchall()

    cur.execute("""
        INSERT INTO log (
            user_key, action, entity_type, misc
        ) VALUES (%s, %s, %s, %s);
    """, (
        user["key"], "api.delete_anonymous_user", "app",
        Json({"deleted_users": [x["key"] for x in users]})
    ))


@bp.post("/maintenance/anonymous")
@session(True)
@rate_limit(20, 1)
def user_delete_anonymous(cur, user):
    if "maintenance.anonymous" not in user["access"]:
        return {
            "status": 403,
            "error": "unauthorized access"
        }, 403

    delete_anonymous_user(cur, user)

    return {
        "status": 200
    }, 200


@bp.get("/cron")
def cron():
    con, cur = db_open()

    cur.execute("""
        SELECT key FROM "user" WHERE email = %s;
    """, (os.environ["MAIL_USERNAME"],))
    user = cur.fetchone()

    delete_anonymous_user(cur, user)

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
    return {
        "status": 200
    }, 200


@bp.post("/contact")
@session(False)
@rate_limit(20, 1)
def footer_send_email(cur, user):
    email_template = request.json.get("email_template")
    name = request.json.get("name")
    email = request.json.get("email")
    message = request.json.get("message")

    if not email_template:
        return {
            "status": 422,
            "error": "Invalid request"
        }, 422

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
        return {
            "status": 422,
            **error
        }, 422

    message = email_template.format(
        name=name, email=email, message=message)

    send_mail(
        os.environ["MAIL_USERNAME"],
        f"{name} from Theophilus Portfolio Website",
        message
    )

    return {
        "status": 200
    }, 200
