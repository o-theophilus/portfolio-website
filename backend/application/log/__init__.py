from flask import Blueprint, jsonify, request
from psycopg2.extras import Json
from ..tools import get_session
from ..postgres import db_close, db_open

bp = Blueprint("log", __name__)


@bp.post("/log")
def log(
    cur=None,
    user_key=None,
    action=None,
    entity_key=None,
    entity_type=None,
    status=200,
    misc={}
):
    close_conn = not cur
    if not cur:
        con, cur = db_open()

    if request.get_json(silent=True):
        if not user_key:
            session = get_session(cur)
            if session["status"] != 200:
                if close_conn:
                    db_close(con, cur)
                return jsonify(session)
            user_key = session["user"]["key"]
        if not action:
            action = request.json.get("action")
        if not entity_type:
            entity_type = request.json.get("entity_type")
        if not entity_key:
            entity_key = request.json.get("entity_key")
        if status == 200:
            status = request.json.get("status", 200)
        if misc == {}:
            misc = request.json.get("misc", {})

    cur.execute("""
        INSERT INTO log (
            user_key, action, entity_key, entity_type, status, misc
        ) VALUES (%s, %s, %s, %s, %s, %s);
    """, (user_key, action, entity_key, entity_type, status, Json(misc)))

    if close_conn:
        db_close(con, cur)
    return jsonify({
        "status": 200
    })
