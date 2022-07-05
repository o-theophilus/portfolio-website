from flask import Blueprint, jsonify


bp = Blueprint("api", __name__)


@bp.route("/")
def index():
    return jsonify({
        "status": 200,
        "message": "Welcome to MEJI API"
    })
