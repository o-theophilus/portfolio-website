from flask import Blueprint, jsonify
import os
from werkzeug.security import generate_password_hash
from ..postgres import db_open, db_close
from ..log import log
from .access import access_pass


bp = Blueprint("admin", __name__)


@bp.get("/admin/default")
def default():
    con, cur = db_open()
    email = os.environ["MAIL_USERNAME"]

    cur.execute('SELECT * FROM "user" WHERE email = %s;', (email,))
    if not cur.fetchone():
        cur.execute("""
                INSERT INTO "user"
                (status, name, username, email, password, access)
                VALUES (%s, %s, %s, %s, %s, %s) RETURNING *;
            """, (
            "confirmed",
            "Theophilus",
            "omni",
            email,
            generate_password_hash(
                os.environ["MAIL_PASSWORD"], method="scrypt"),
            [f"{x}:{y[0]}" for x in access_pass for y in access_pass[x]]
        ))
        user = cur.fetchone()

        log(
            cur=cur,
            user_key=user["key"],
            action="created",
            entity_type="account"
        )
        log(
            cur=cur,
            user_key=user["key"],
            action="signedup",
            entity_type="account"
        )
        log(
            cur=cur,
            user_key=user["key"],
            action="confirmed",
            entity_type="account"
        )

    db_close(con, cur)
    return jsonify({
        "status": 200
    })


@bp.get("/admin/default_access")
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
