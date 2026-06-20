import os
import random
from datetime import datetime, timedelta, timezone
from functools import wraps

import resend
from flask import current_app, request
from psycopg2.extras import Json

from .postgres import db_close, db_open

reserved_words = [
    "meji", "app", "home", "shop", "save", "cart", "profile", "orders",
    "terms", "admin", "omni", "user", "users", "store", "stores", "item",
    "items", "all"]

access_pass = {
    "user": [
        ['view', 1],
        ['reset_name', 2],
        ['reset_username', 2],
        ['reset_photo', 2],
        ['block', 2],
        ['edit_access', 3]
    ],
    "admin": [
        ['manage_files', 3]
    ],
    "post": [
        ['add', 2],
        ['edit_photo', 2],
        ['edit_title', 2],
        ['edit_date', 2],
        ['edit_description', 2],
        ['edit_content', 2],
        ['edit_files', 2],
        ['edit_tags', 2],
        ['edit_status', 2],
        ['edit_author', 2],
        ['edit_featured', 2]
    ],
    "comment": [
        ['delete_others', 3]
    ],
    "report": [
        ['view', 1],
        ['resolve', 3]
    ],
    "block": [
        ['view', 1],
        ['unblock', 3]
    ],
    "log": [
        ['view', 1],
        ['view_others', 2],
    ],
    "maintenance": [
        ['anonymous', 1]
    ]
}


def get_session(cur, login=False):
    token = request.headers.get("Authorization")
    print(token)
    if not token:
        print(1)
        return {
            "status": 401,
            "error": "invalid or expired token"
        }

    cur.execute("""SELECT * FROM session WHERE key::TEXT = %s;""", (token,))
    session = cur.fetchone()
    if not session:
        return {
            "status": 401,
            "error": "invalid or expired token"
        }

    if login and not session["login"]:
        return {
            "status": 401,
            "error": "invalid or expired token"
        }

    cur.execute("""
        SELECT * FROM "user" WHERE key = %s;
    """, (session["user_key"],))
    user = cur.fetchone()
    user["login"] = session["login"]

    cur.execute("""
        UPDATE session SET date_updated = now() WHERE key = %s;
    """, (session["key"],))

    return {
        "status": 200,
        "user": user
    }


def session(login=False):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            con, cur = db_open()
            try:
                session = get_session(cur, login)
                if request.endpoint == "auth.init":
                    return fn(cur, session, *args, **kwargs)
                elif session["status"] != 200:
                    return session, session["status"]
                return fn(cur, session["user"], *args, **kwargs)
            finally:
                db_close(con, cur)

        return wrapper
    return decorator


def rate_limit(times=20, mins=1):
    def decorator(fn):
        @wraps(fn)
        def wrapper(cur, user, *args, **kwargs):
            endpoint = request.endpoint

            cur.execute("""
                SELECT COUNT(*)
                FROM rate_limit_log
                WHERE user_key = %s
                AND endpoint = %s
                AND date_created > NOW() - INTERVAL %s
            """, (user["key"], endpoint, f"{mins} minutes"))
            count = cur.fetchone()["count"]

            if count >= times:
                return {
                    "status": 429,
                    "message": f"""Rate limit exceeded.
                        Please wait for
                        {mins} {"minutes" if mins > 1 else "minute"}
                        and try again"""
                }, 429

            cur.execute("""
                INSERT INTO rate_limit_log (user_key, endpoint)
                VALUES (%s, %s)
            """, (user["key"], endpoint))

            return fn(cur, user, *args, **kwargs)

        return wrapper
    return decorator


def log(entity_type):
    def decorator(fn):
        @wraps(fn)
        def wrapper(cur, user, *args, **kwargs):
            result = fn(cur, user, *args, **kwargs)

            body, status = result, 200
            if isinstance(result, tuple):
                body, status = result

            _log = {
                "user_key": user["key"],
                "action": request.endpoint,
                "entity_key": None,
                "entity_type": entity_type,
                "status": status,
                "misc": body
            }

            log_data = body.pop("log", None)
            if log_data:
                _log = {**_log, **log_data}

            cur.execute("""
                INSERT INTO log (
                    user_key, action, entity_key, entity_type, status, misc
                ) VALUES (%s, %s, %s, %s, %s, %s);
            """, (
                _log["user_key"], _log["action"], _log["entity_key"],
                _log["entity_type"], _log["status"], Json(_log["misc"])
            ))

            return body, status

        return wrapper
    return decorator


def generate_code(cur, key, email, _from, clear=True):
    if clear:
        cur.execute("DELETE FROM code WHERE user_key = %s;", (key,))

    code = f"{random.randint(100000, 999999)}"

    cur.execute("""
        INSERT INTO code (user_key, pin, email)
        VALUES (%s, %s, %s) RETURNING *;
    """, (key, code, email))
    _code = cur.fetchone()

    cur.execute("""
        INSERT INTO log (
            user_key, action, entity_key, entity_type, status, misc
        ) VALUES (%s, %s, %s, %s, %s, %s);
    """, (
        key,
        "requested",
        _code["key"],
        "code",
        200,
        Json({"from": _from, "to": email})
    ))

    return code


def check_code(cur, user_key, email, n="code"):
    pin = request.json.get(n)
    error = None
    if not pin:
        error = "This field is required"
    elif len(pin) != 6:
        error = "invalid code"

    # TODO: use the time SQL time keyword
    cur.execute("""
        SELECT * FROM code WHERE user_key = %s AND pin = %s AND email = %s;
    """, (user_key, pin, email))
    code = cur.fetchone()

    if not code:
        error = "invalid code"
    elif datetime.now(timezone.utc) - code[
            "date_created"] > timedelta(minutes=15):
        cur.execute("DELETE FROM code WHERE user_key = %s;", (user_key,))
        error = "invalid code"

    return error


def send_mail(to, subject, body):
    print(f"Sending email to {to} with subject '{subject}'")

    if current_app.config["DEBUG"]:
        print(body)
    else:
        resend.api_key = os.environ["RESEND_API_KEY"]
        params = {
            "from": "Theophilus <info@theophilus.website>",
            "to": [to] if type(to) is not list else to,
            "subject": subject,
            "html": body,
        }

        try:
            email = resend.Emails.send(params)
            print("Email sent successfully", email)
        except Exception as e:
            print(f"Error sending email: {e}")


def user_schema(user):
    del user["password"]
    user["photo"] = (
        f"{request.host_url}photo/user/{user['photo']}"
        if user["photo"] else None
    )
    return user
