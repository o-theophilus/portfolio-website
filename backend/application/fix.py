from flask import Blueprint, jsonify
from .postgres import db_open, db_close


bp = Blueprint("fix", __name__)


# @bp.get("/fix")
def quick_fix():
    con, cur = db_open()

    cur.execute("""
        ALTER TABLE session ADD COLUMN remember BOOL DEFAULT FALSE;
    """)

    # cur.execute(f"""
    #     DROP TABLE IF EXISTS "like" CASCADE;
    #     {create_tables_query()}
    # """)
    # cur.execute(create_tables_query())

    db_close(con, cur)
    return jsonify({
        "status": 200
    })
