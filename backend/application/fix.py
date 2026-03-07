import os

from flask import Blueprint, jsonify

from .postgres import db_close, db_open
from .tools import access_pass

bp = Blueprint("fix", __name__)


def quick_fix():
    con, cur = db_open()

    # TODO
    cur.execute("""
        UPDATE "user"
        SET status = 'active'
        WHERE status = 'confirmed';
    """)

    db_close(con, cur)
    return jsonify({
        "status": 200
    })


@bp.get("/fix")
def fix_access():
    con, cur = db_open()

    cur.execute("""
        UPDATE "user" SET access=%s WHERE email = %s;
    """, (
        [f"{x}:{y[0]}" for x in access_pass for y in access_pass[x]],
        os.environ["MAIL_USERNAME"]
    ))

    db_close(con, cur)
    return jsonify({
        "status": 200
    })
