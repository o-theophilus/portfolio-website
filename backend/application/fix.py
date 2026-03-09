import os

from flask import Blueprint, jsonify

from .postgres import db_close, db_open
from .tools import access_pass

bp = Blueprint("fix", __name__)


# @bp.get("/fix")
def quick_fix():
    con, cur = db_open()

    cur.execute("""
        DROP TABLE IF EXISTS "like";
        DROP TABLE IF EXISTS report;

        CREATE TABLE IF NOT EXISTS "like" (
            key UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            date_created TIMESTAMPTZ DEFAULT now(),
            user_key UUID NOT NULL REFERENCES "user"(key) ON DELETE CASCADE,
            reaction TEXT NOT NULL DEFAULT 'like',
            entity_type TEXT NOT NULL, -- item, review
            entity_key UUID NOT NULL,
            UNIQUE (user_key, entity_key)
        );

        CREATE TABLE IF NOT EXISTS report (
            key UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            status TEXT NOT NULL DEFAULT 'active',
            date_created TIMESTAMPTZ DEFAULT now(),
            reporter_key UUID NOT NULL REFERENCES "user"(key),
            reporter_comment TEXT NOT NULL,
            tags TEXT[] DEFAULT '{}'::TEXT[],
            date_resolved TIMESTAMPTZ,
            resolver_key UUID REFERENCES "user"(key),
            resolver_comment TEXT,
            entity_type TEXT NOT NULL, -- user, review
            entity_key UUID NOT NULL
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
