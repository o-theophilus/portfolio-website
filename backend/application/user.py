from flask import Blueprint, jsonify, request
from .postgres import db_open, db_close
from .tools import token_to_user
from .log import log


bp = Blueprint("user", __name__)


@bp.post("/user/theme")
def theme():
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    theme = "light"
    if user["setting_theme"] == "light":
        theme = "dark"

    cur.execute("""
        UPDATE "user"
        SET setting_theme = %s
        WHERE key = %s;
    """, (
        theme,
        user["key"]
    ))

    log(
        cur=cur,
        user_key=user["key"],
        action="changed_theme",
        entity_type="user",
        misc={
            "from": user["setting_theme"],
            "to": theme
        }
    )

    user["setting_theme"] = theme

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "user": user
    })
