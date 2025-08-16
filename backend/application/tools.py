from flask import request, current_app
from itsdangerous import URLSafeTimedSerializer
import os
from uuid import uuid4
import random
from datetime import datetime, timedelta
from psycopg2.extras import Json
import smtplib
import ssl
from email.mime.text import MIMEText


reserved_words = [
    "meji", "app", "home", "shop", "save", "cart", "profile", "orders",
    "terms", "admin", "omni", "user", "users", "store", "stores", "item",
    "items", "all"]


def token_tool():
    return URLSafeTimedSerializer(
        current_app.config["SECRET_KEY"],
        current_app.config["SECURITY_PASSWORD_SALT"]
    )


# TODO: restrict access of blocked users
def token_to_user(cur):
    if (
        "Authorization" not in request.headers or
        not request.headers["Authorization"]
    ):
        return None

    token = request.headers["Authorization"]
    try:
        token = token_tool().loads(token)
    except Exception:
        return None

    cur.execute("""
        SELECT * FROM "user" WHERE key = %s AND status != 'deleted';
    """, (token,))
    user = cur.fetchone()
    return user


def generate_code(cur, key, email, _from, clear=True):
    if clear:
        cur.execute("DELETE FROM code WHERE user_key = %s;", (key,))

    code = f"{random.randint(100000, 999999)}"
    code_key = uuid4().hex

    cur.execute("""
        INSERT INTO code (key, user_key, pin, email)
        VALUES (%s, %s, %s, %s);
    """, (
        code_key,
        key,
        code,
        email
    ))

    cur.execute("""
        INSERT INTO log (
            key, date, user_key, action, entity_key, entity_type, status, misc
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
    """, (
        uuid4().hex,
        datetime.now(),
        key,
        "requested",
        code_key,
        "code",
        200,
        Json({"from": _from, "to": email})
    ))

    return code


def check_code(cur, key, email, n="code"):
    error = None
    if n not in request.json or not request.json[n]:
        error = "cannot be empty"
    elif len(request.json[n]) != 6:
        error = "invalid code"

    cur.execute("""
        SELECT code.*, log.date
        FROM code
        LEFT JOIN log ON
            code.key = log.entity_key
            AND log.entity_type = 'code'
            AND log.action = 'requested'
        WHERE
            code.user_key = %s
            AND code.pin = %s
            AND code.email = %s;
    """, (
        key,
        request.json[n],
        email
    ))
    code = cur.fetchone()

    if not code:
        error = "invalid code"
    elif datetime.now() - code["date"] > timedelta(minutes=15):
        cur.execute("""
            DELETE FROM code WHERE user_key = %s
        ;""", (key,))
        error = "invalid code"

    return error


def send_mail(to, subject, body):
    print(f"Sending email to {to} with subject '{subject}'")

    if current_app.config["DEBUG"]:
        print(body)
    else:
        msg = MIMEText(body, "html")
        msg['Subject'] = subject
        msg['From'] = os.environ["MAIL_USERNAME"]
        msg['To'] = to

        context = ssl.create_default_context()

        try:
            with smtplib.SMTP("workplace.truehost.cloud", 587) as server:
                server.starttls(context=context)
                server.login(os.environ["MAIL_USERNAME"],
                             os.environ["MAIL_PASSWORD"])
                server.sendmail(os.environ["MAIL_USERNAME"], [
                                to], msg.as_string())

            print("Email sent successfully")
        except Exception as e:
            print(f"Error sending email: {e}")


# TODO: move to user_get.py
def user_schema(user):
    del user["password"]
    user["photo"] = (
        f"{request.host_url}file/{user['photo']}"
        if user["photo"] else None
    )
    return user
