from flask import Blueprint, request
from psycopg2.extras import Json

from ..tools import session

bp = Blueprint("log", __name__)


@bp.post("/logs")
@session(False)
def log(cur, user):

    action = request.json.get("action")
    entity_key = request.json.get("entity_key")
    entity_type = request.json.get("entity_type")
    status = request.json.get("status", 200)
    misc = request.json.get("misc", {})

    cur.execute("""
        INSERT INTO log (
            user_key, action, entity_key, entity_type, status, misc
        ) VALUES (%s, %s, %s, %s, %s, %s);
    """, (user["key"], action, entity_key, entity_type, status, Json(misc)))

    return {
        "status": 200
    }, 200
