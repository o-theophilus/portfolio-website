from flask import Blueprint, jsonify
from psycopg2.extras import Json
from ...postgres import db_open, db_close
from ...post import post_schema


bp = Blueprint("highlight_get", __name__)


@bp.get("/highlights")
def get_many(cur=None):
    close_conn = not cur
    if not cur:
        con, cur = db_open()

    cur.execute("SELECT * FROM app WHERE alias = 'highlight';",)
    highlight = cur.fetchone()
    if not highlight:
        cur.execute("""
            INSERT INTO app (alias, value)
            VALUES ('highlight', %s)
            RETURNING *;
        """, (Json({"post_keys": []}),))
        highlight = cur.fetchone()
    keys = highlight["value"]["post_keys"]

    cur.execute("""
        SELECT * FROM post WHERE status = 'active' AND key::TEXT = ANY(%s);
    """, (keys,))
    items = cur.fetchall()
    items = sorted(items, key=lambda d: keys.index(d['key']))

    if close_conn:
        db_close(con, cur)
    return jsonify({
        "status": 200,
        "items": [post_schema(x) for x in items]
    })
