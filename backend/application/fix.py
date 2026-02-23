import os

from flask import Blueprint, jsonify

from .postgres import db_close, db_open
from .tools import access_pass

bp = Blueprint("fix", __name__)


# @bp.get("/fix")
def quick_fix():
    con, cur = db_open()

    cur.execute("""
        ALTER TABLE "like"
        ADD COLUMN IF NOT EXISTS post_key UUID REFERENCES post(key)
            ON DELETE CASCADE,
        ADD COLUMN IF NOT EXISTS comment_key UUID REFERENCES comment(key)
            ON DELETE CASCADE;
    """)

    cur.execute("""
        UPDATE "like"
        SET post_key = entity_key::UUID
        WHERE entity_type = 'post';
    """)

    cur.execute("""
        UPDATE "like"
        SET comment_key = entity_key::UUID
        WHERE entity_type = 'comment';
    """)

    cur.execute("""
        ALTER TABLE "like"
        DROP COLUMN IF EXISTS entity_type,
        DROP COLUMN IF EXISTS entity_key;
    """)

    cur.execute("""
        DROP TABLE IF EXISTS report CASCADE;

         CREATE TABLE IF NOT EXISTS report (
            key UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            date_created TIMESTAMPTZ DEFAULT now(),
            status TEXT NOT NULL DEFAULT 'active',

            reporter_key UUID NOT NULL REFERENCES "user"(key),

            reported_key UUID REFERENCES "user"(key) ON DELETE CASCADE,
            comment_key UUID REFERENCES comment(key) ON DELETE CASCADE,

            comment TEXT NOT NULL,
            tags TEXT[] DEFAULT '{}'::TEXT[],

            resolver_key UUID REFERENCES "user"(key),
            resolve_comment TEXT,
            date_resolved TIMESTAMPTZ
        );
    """)

    cur.execute("""
        ALTER TABLE "user"
        ALTER COLUMN theme SET DEFAULT 'system';
    """)

    cur.execute("""
        ALTER TABLE post
        ADD COLUMN IF NOT EXISTS featured INT DEFAULT 0;
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
