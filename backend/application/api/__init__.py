from flask import Blueprint, jsonify, current_app
from itsdangerous import URLSafeTimedSerializer
from datetime import datetime, timedelta


bp = Blueprint("api", __name__)


@bp.route("/")
def index():
    return jsonify({
        "status": 200,
        "message": "Welcome to Theophilus"
    })


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
