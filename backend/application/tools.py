import os
import random
from datetime import datetime, timedelta, timezone
from functools import wraps

import resend
from flask import current_app, jsonify, request
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
        ['set_access', 3]
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
    if not token:
        return {"status": 401, "error": "invalid or expired token"}

    cur.execute("""SELECT * FROM session WHERE key::TEXT = %s;""", (token,))
    session = cur.fetchone()
    if not session:
        return {"status": 401, "error": "invalid or expired token"}

    if login and session["login"] == "false":
        return {"status": 401, "error": "invalid or expired token"}

    cur.execute("""
        SELECT * FROM "user" WHERE key = %s;
    """, (session["user_key"],))
    user = cur.fetchone()

    cur.execute("""
        UPDATE session SET date_updated = now() WHERE key = %s;
    """, (session["key"],))

    return {"status": 200, "user": user, "login": session["login"] != "false"}


# TODO: Decorators are commonly used for:

# ✅ Logging
# ✅ Permissions

def session(login=False):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            con, cur = db_open()
            try:
                session = get_session(cur, login)
                if session["status"] != 200:
                    return jsonify(session), session["status"]
                return fn(cur, session["user"], *args, **kwargs)
            finally:
                db_close(con, cur)

        return wrapper
    return decorator


def logg(times=20, mins=1):
    def decorator(fn):
        @wraps(fn)
        def wrapper(cur, user, *args, **kwargs):
            print("logg")
            result = fn(cur, user, *args, **kwargs)
            print(result.json)
            return result

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
                return jsonify({
                    "status": 429,
                    "message": f"""Rate limit exceeded.
                        Please wait for
                        {mins} {"minutes" if mins > 1 else "minute"}
                        and try again"""
                }), 429

            cur.execute("""
                INSERT INTO rate_limit_log (user_key, endpoint)
                VALUES (%s, %s)
            """, (user["key"], endpoint))

            return fn(cur, user, *args, **kwargs)

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
