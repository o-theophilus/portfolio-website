import os

from flask import Blueprint

from .postgres import db_close, db_open
from .tools import access_pass

bp = Blueprint("fix", __name__)


# @bp.get("/fix")
def quick_fix():
    con, cur = db_open()

    # cur.execute("""
    #     CREATE TABLE IF NOT EXISTS rate_limit_log (
    #         key UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    #         user_key UUID NOT NULL REFERENCES "user"(key) ON DELETE CASCADE,
    #         endpoint TEXT NOT NULL,
    #         date_created TIMESTAMPTZ DEFAULT NOW()
    #     );
    #     CREATE INDEX idx_rate_limit_lookup
    #         ON rate_limit_log (user_key, endpoint, date_created);
    # """)

    # cur.execute("""
    #     ALTER TABLE log
    #     ALTER COLUMN entity_key DROP NOT NULL;
    # """)

    cur.execute("""
        DROP TABLE IF EXISTS session CASCADE;
        CREATE TABLE IF NOT EXISTS session (
            key UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            date_created TIMESTAMPTZ DEFAULT now(),
            date_updated TIMESTAMPTZ DEFAULT now(),
            user_key UUID NOT NULL REFERENCES "user"(key) ON DELETE CASCADE,
            login BOOL NOT NULL DEFAULT FALSE,
            remember BOOL NOT NULL DEFAULT FALSE
        );
    """)

    db_close(con, cur)
    return {
        "status": 200
    }, 200


def fix_access():
    con, cur = db_open()

    cur.execute("""
        UPDATE "user" SET access=%s WHERE email = %s;
    """, (
        [f"{x}.{y[0]}" for x in access_pass for y in access_pass[x]],
        os.environ["MAIL_USERNAME"]
    ))

    db_close(con, cur)
    return {
        "status": 200
    }, 200
