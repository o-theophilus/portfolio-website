from flask import Blueprint, jsonify
from .postgres import db_open, db_close


bp = Blueprint("fix", __name__)


@bp.get("/fix")
def quick_fix():
    con, cur = db_open()

    cur.execute("""
        ALTER TABLE block RENAME COLUMN blocked_user_key TO admin_key;
    """)

    db_close(con, cur)
    return jsonify({
        "status": 200
    })
