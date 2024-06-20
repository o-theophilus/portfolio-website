from flask import request, current_app
from itsdangerous import URLSafeTimedSerializer
import smtplib
from email.utils import formataddr
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from uuid import uuid4
import random
from datetime import datetime, timedelta
import json


reserved_words = [
    "meji", "app", "home", "shop", "save", "cart", "profile", "orders",
    "terms", "admin", "omni", "user", "users", "store", "stores", "item",
    "items", "all"]


def token_tool():
    return URLSafeTimedSerializer(
        current_app.config["SECRET_KEY"],
        current_app.config["SECURITY_PASSWORD_SALT"]
    )


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


def generate_otp(cur, key, email, _from):
    cur.execute("DELETE FROM otp WHERE user_key = %s;", (key,))

    otp = f"{random.randint(100000, 999999)}"
    otp_key = uuid4().hex

    cur.execute("""
        INSERT INTO otp (key, user_key, pin, email)
        VALUES (%s, %s, %s, %s);
    """, (
        otp_key,
        key,
        otp,
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
        otp_key,
        "otp",
        200,
        json.dumps({
            "from": _from,
            "to": email
        })
    ))

    return otp


def check_otp(cur, key, email, n="otp"):
    error = None
    if n not in request.json or not request.json[n]:
        error = "cannot be empty"
    elif (
        type(request.json[n]) is not int
        or request.json[n] < 100000
        or request.json[n] > 999999
    ):
        error = "invalid"

    cur.execute("""
        SELECT otp.*, log.date
        FROM otp
        LEFT JOIN log ON
            otp.key = log.entity_key
            AND log.entity_type = 'otp'
            AND log.action = 'requested'
        WHERE
            otp.user_key = %s
            AND otp.pin = %s
            AND otp.email = %s;
    """, (
        key,
        f"{request.json['otp']}",
        email
    ))
    otp = cur.fetchone()

    if not otp:
        error = "invalid OTP"
    elif datetime.now() - otp["date"] > timedelta(minutes=15):
        cur.execute("""
            DELETE FROM otp WHERE user_key = %s
        ;""", (key,))
        error = "invalid OTP"

    return error


def send_mail(to, subject, body):
    if current_app.config["DEBUG"]:
        print(body)
    else:
        admin = os.environ["MAIL_USERNAME"]

        msg = MIMEMultipart()
        msg['From'] = formataddr(("Meji", admin))
        msg['To'] = to
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'html'))

        server = smtplib.SMTP('smtp.office365.com', 587)
        server.starttls()
        server.login(
            admin,
            os.environ["MAIL_PASSWORD"]
        )
        server.sendmail(admin, to, msg.as_bytes())
        server.quit()


def user_schema(user, saves=[]):
    del user["password"]
    user["photo"] = (f"{request.host_url}photo/{user['photo']}"
                     if user["photo"] else None)
    user["saves"] = saves
    return user
