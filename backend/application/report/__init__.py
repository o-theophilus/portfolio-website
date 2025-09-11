from flask import Blueprint, jsonify, request
from ..tools import get_session
from ..postgres import db_close, db_open
from ..log import log

bp = Blueprint("report", __name__)


@bp.post("/report")
def create():
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    entity_key = request.json.get("entity_key")
    entity_type = request.json.get("entity_type")
    comment = request.json.get("comment")
    tags = request.json.get("tags")

    # TODO: prevent from reporting self
    if (
        not session["login"]
        or not entity_key
        or not entity_type
        or entity_type not in ["user", "comment"]
        or type(tags) is not list
    ):
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    if not comment:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "comment": "This field is required"
        })

    cur.execute(f"""
        SELECT * FROM "{entity_type}" WHERE key = %s;
    """, (entity_key,))
    entity = cur.fetchone()
    if not entity:
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    cur.execute("""
        INSERT INTO report (user_key, entity_key, entity_type, comment, tags)
        VALUES (%s, %s, %s, %s, %s) RETURNING *;
    """, (user["key"], entity["key"], entity_type, comment, tags))
    report = cur.fetchone()

    log(
        cur=cur,
        user_key=user["key"],
        action="created",
        entity_key=report["key"],
        entity_type="report",
        misc={
            "entity_key":  entity_key,
            "entity_type":  entity_type,
        }
    )

    db_close(con, cur)
    return jsonify({
        "status": 200
    })


@bp.post("/report/resolve/<key>")
def resolve(key):
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    if "report:resolve" not in user["access"]:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "unauthorized access"
        })

    note = request.json.get("note")
    if not note:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "note": "This field is required"
        })
    elif len(note) > 500:
        return jsonify({
            "status": 400,
            "note": "This field cannot exceed 500 characters"
        })

    # TODO: prevent from resolving self
    cur.execute("""
        SELECT * FROM report WHERE key = %s;
    """, (key,))
    report = cur.fetchone()
    if not report:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    log(
        cur=cur,
        user_key=user["key"],
        action="resolved",
        entity_key=report["key"],
        entity_type="report",
        misc={
            "user_key": report["user_key"],
            "entity_type": report["entity_type"],
            "report": report["report"],
            "tags": report["tags"],
            "resolve":  resolve,
        }
    )

    cur.execute("DELETE FROM report key = %s;", (report["key"]))

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "report": report
    })
