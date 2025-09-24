from flask import Blueprint, jsonify, request
import re
import os
from ..tools import send_mail
from ..postgres import db_open, db_close
from ..log import log
from ..auth import delete_user


bp = Blueprint("api", __name__)


@bp.get("/cron")
def cron():
    con, cur = db_open()

    cur.execute("""
        DELETE FROM session
        WHERE (
                remember = FALSE
                AND date_updated <= NOW() - INTERVAL '3 days'
            ) OR (
                remember = TRUE
                AND date_updated <= NOW() - INTERVAL '14 days'
            )
        RETURNING *;
    """)
    sessions = cur.fetchall()
    session_keys = [x["key"] for x in sessions]

    cur.execute("""
        SELECT * FROM "user"
        WHERE status = 'anonymous'
            AND date_created <= NOW() - INTERVAL '30 days';
    """)
    users = cur.fetchall()
    user_keys = [x["key"] for x in users]

    for x in user_keys:
        delete_user(cur, x)

    cur.execute("""
        SELECT * FROM "user" WHERE email = %s;
    """, (os.environ["MAIL_USERNAME"],))
    user = cur.fetchone()
    log(
        cur=cur,
        user_key=user["key"],
        action="run cron",
        entity_key="app",
        entity_type="app",
        misc={
            "deleted_sessions": session_keys,
            "deleted_users": user_keys,
        }
    )

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "deleted_sessions": session_keys,
        "deleted_users": user_keys,
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
    if error != {}:
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
