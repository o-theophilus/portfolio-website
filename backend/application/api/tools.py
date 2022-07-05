from flask import request, current_app
from itsdangerous import URLSafeTimedSerializer
from datetime import datetime, timedelta
from .detabase import db_get


def token_tool():
    return URLSafeTimedSerializer(
        current_app.config["SECRET_KEY"],
        current_app.config["SECURITY_PASSWORD_SALT"]
    )


def now(day=0):
    return (datetime.now() + timedelta(days=1) * day).replace(
        microsecond=0).isoformat()


reserved_words = [
    "admin", "omni", "user", "users", "store", "stores", "item",
    "items"]  # property, cart, save


def token_to_user(db=[]):
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

    return db_get(db, "user", "key", token)
