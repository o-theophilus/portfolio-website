from flask import request, current_app
from itsdangerous import URLSafeTimedSerializer
import smtplib
from email.utils import formataddr
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os


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
