from flask import Blueprint, jsonify
from .postgres import db_open, db_close, create_tables_query


bp = Blueprint("fix", __name__)


# @bp.get("/fix")
def quick_fix():
    con, cur = db_open()

    # print(create_tables_query())
    # cur.execute("""
    #     ALTER TABLE block RENAME COLUMN blocked_user_key TO admin_key;
    # """)

    cur.execute(f"""
        DROP TABLE IF EXISTS "like" CASCADE;
        {create_tables_query()}
    """)
    # cur.execute(create_tables_query())

    db_close(con, cur)
    return jsonify({
        "status": 200
    })
