from flask import Blueprint, jsonify
from . import user_schema, db, token_to_user, now


bp = Blueprint("user", __name__)


@ bp.post("/user/theme")
def user_theme():
    user = token_to_user()
    if not user:
        return jsonify({
            "status": 401,
            "message": "invalid request"
        })

    if user["setting"]["theme"] == "dark":
        user["setting"]["theme"] = "light"
    else:
        user["setting"]["theme"] = "dark"

    user["updated_at"] = now()
    user = db.add(user)

    return jsonify({
        "status": 200,
        "message": "successful",
        "data": {
            "user": user_schema(user)
        }
    })
