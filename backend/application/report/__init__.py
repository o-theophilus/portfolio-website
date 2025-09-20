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

    if (
        not session["login"]
        or not entity_key
        or entity_key == user["key"]
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


@bp.delete("/report/<key>")
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

    cur.execute("SELECT * FROM report WHERE key = %s;", (key,))
    report = cur.fetchone()
    if not report or report["entity_key"] == user["key"]:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    comment = request.json.get("comment")
    delete_comment = request.json.get("delete_comment", False)

    error = {}
    if not comment:
        error["comment"] = "This field is required"
    elif len(comment) > 500:
        error["comment"] = "This field cannot exceed 500 characters"
    if error != {}:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            **error
        })

    misc = {
        "user_key": report["user_key"],
        "entity_key": report["entity_key"],
        "entity_type": report["entity_type"],
        "comment": report["comment"],
        "tags": report["tags"]
    }

    cur.execute("DELETE FROM report WHERE key = %s;", (report["key"],))
    if report["entity_type"] == "comment" and delete_comment:
        cur.execute("DELETE FROM comment WHERE key = %s;",
                    (report["entity_key"],))
        misc["deleted_comment"] = report["entity_key"]

    log(
        cur=cur,
        user_key=user["key"],
        action="resolved",
        entity_key=report["key"],
        entity_type="report",
        misc=misc
    )

    db_close(con, cur)
    return jsonify({
        "status": 200
    })
