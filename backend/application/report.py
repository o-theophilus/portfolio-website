from flask import Blueprint, jsonify, request
from . import db
from .tools import token_to_user
from .schema import report_template


bp = Blueprint("report", __name__)


@bp.post("/report/<key>")
def report(key):

    if "comment" not in request.json or not request.json["comment"]:
        return jsonify({
            "status": 400,
            "comment": "cannot be empty"
        })

    data = db.data()

    user = token_to_user(data)
    entity = db.get_key(key, data)
    if (
        not user or not entity
        or user["status"] != "verified"
        or not user["login"]
        or entity["type"] not in ["user", "comment"]
        or entity["type"] == "comment" and entity["user_key"] == user["key"]
        or entity["type"] == "user" and entity["key"] == user["key"]
        or entity["status"] == "deleted"
    ):
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    db.add(report_template(
        user["key"],
        entity["key"],
        request.json["comment"]
    ))

    return jsonify({
        "status": 200,
    })
