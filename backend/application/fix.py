from flask import Blueprint, jsonify
from .postgres import db_open, db_close


bp = Blueprint("fix", __name__)


# @bp.get("/fix")
def quick_fix():
    con, cur = db_open()

    cur.execute("""
        ALTER TABLE comment
        DROP CONSTRAINT IF EXISTS comment_user_key_fkey,
        DROP CONSTRAINT IF EXISTS comment_post_key_fkey,
        DROP CONSTRAINT IF EXISTS comment_parent_key_fkey;
        ALTER TABLE comment
        ADD FOREIGN KEY (user_key) REFERENCES "user"(key) ON DELETE CASCADE,
        ADD FOREIGN KEY (post_key) REFERENCES post(key) ON DELETE CASCADE,
        ADD FOREIGN KEY (parent_key) REFERENCES comment(key) ON DELETE CASCADE;

        ALTER TABLE report
        DROP CONSTRAINT IF EXISTS report_user_key_fkey;
        ALTER TABLE report
        ADD FOREIGN KEY (user_key) REFERENCES "user"(key) ON DELETE CASCADE;

        ALTER TABLE block
        DROP CONSTRAINT IF EXISTS block_admin_key_fkey,
        DROP CONSTRAINT IF EXISTS block_user_key_fkey;
        ALTER TABLE block
        ADD FOREIGN KEY (admin_key) REFERENCES "user"(key) ON DELETE CASCADE,
        ADD FOREIGN KEY (user_key) REFERENCES "user"(key) ON DELETE CASCADE;

        ALTER TABLE "like"
        DROP CONSTRAINT IF EXISTS like_user_key_fkey;
        ALTER TABLE "like"
        ADD FOREIGN KEY (user_key) REFERENCES "user"(key) ON DELETE CASCADE;

        ALTER TABLE code
        DROP CONSTRAINT IF EXISTS code_user_key_fkey;
        ALTER TABLE code
        ADD FOREIGN KEY (user_key) REFERENCES "user"(key) ON DELETE CASCADE;

        ALTER TABLE session
        DROP CONSTRAINT IF EXISTS session_user_key_fkey;
        ALTER TABLE session
        ADD FOREIGN KEY (user_key) REFERENCES "user"(key) ON DELETE CASCADE;
    """)

    db_close(con, cur)
    return jsonify({
        "status": 200
    })
