import resend
from flask import request, current_app
import os
import random
from datetime import datetime, timezone, timedelta
from psycopg2.extras import Json


reserved_words = [
    "meji", "app", "home", "shop", "save", "cart", "profile", "orders",
    "terms", "admin", "omni", "user", "users", "store", "stores", "item",
    "items", "all"]


def get_session(cur, login=False):
    token = request.headers.get("Authorization")
    if not token:
        return {"status": 404, "error": "invalid or expired token"}

    cur.execute("""SELECT * FROM session WHERE key::TEXT = %s;""", (token,))
    session = cur.fetchone()
    if not session:
        return {"status": 404, "error": "invalid or expired token"}

    if login and session["login"] == "false":
        return {"status": 404, "error": "invalid or expired token"}

    cur.execute("""
        SELECT * FROM "user" WHERE key = %s;
    """, (session["user_key"],))
    user = cur.fetchone()

    if not user:
        return {"status": 404, "error": "invalid or expired token"}

    cur.execute("""
        UPDATE session SET date_updated = %s WHERE key = %s;
    """, (datetime.now(timezone.utc), session["key"]))

    return {"status": 200, "user": user, "login": session["login"] != "false"}


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
            "to": [to],
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
        f"{request.host_url}file/{user['photo']}"
        if user["photo"] else None
    )
    return user
