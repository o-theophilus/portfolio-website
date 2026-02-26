import os

from flask import Blueprint, jsonify

from .postgres import db_close, db_open
from .tools import access_pass

bp = Blueprint("fix", __name__)


# @bp.get("/fix")
def quick_fix():
    con, cur = db_open()
    cur.execute("""
        DROP TABLE IF EXISTS app CASCADE;
    """)

    cur.execute("""
        ALTER TABLE report
        RENAME COLUMN comment TO reporter_comment;
    """)

    cur.execute("""
        ALTER TABLE report
        RENAME COLUMN resolve_comment TO resolver_comment;
    """)

    cur.execute("""
        ALTER TABLE report
        RENAME COLUMN reported_key TO reported_user_key;
    """)

    cur.execute("""
        ALTER TABLE report
        RENAME COLUMN comment_key TO reported_comment_key;
    """)

    cur.execute("""
        DROP TABLE IF EXISTS block CASCADE;
    """)

    cur.execute("""
            CREATE TABLE IF NOT EXISTS block (
            key UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            date_created TIMESTAMPTZ DEFAULT now(),
            admin_key UUID NOT NULL REFERENCES "user"(key) ON DELETE CASCADE,
            user_key UUID UNIQUE NOT NULL REFERENCES
                "user"(key) ON DELETE CASCADE,
            comment TEXT NOT NULL
        );
    """)

    db_close(con, cur)
    return jsonify({
        "status": 200
    })


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
