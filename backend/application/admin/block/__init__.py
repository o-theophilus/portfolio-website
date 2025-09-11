from flask import Blueprint, jsonify, request
from ...tools import get_session
from ...postgres import db_close, db_open
from ...log import log

bp = Blueprint("block", __name__)


@bp.post("/block/<key>")
def block(key):
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    comment = request.json.get("comment")
    blocked = request.json.get("blocked")

    if (
        block and "block:block" not in user["access"]
        or not block and "block:unblock" not in user["access"]
    ):
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "unauthorized access"
        })

    cur.execute("""SELECT * FROM "user" WHERE key = %s;""", (key,))
    blocked_user = cur.fetchone()

    if not blocked_user or blocked_user["key"] == user["key"]:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

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

    if blocked:
        cur.execute("""
            INSERT INTO block (admin_key, user_key, comment)
            VALUES (%s, %s, %s);
        """, (user["key"], blocked_user["key"], comment))

        cur.execute("""
            DELETE FROM session WHERE user_key = %s;
        """, (blocked_user["key"],))
    else:
        cur.execute("DELETE FROM block WHERE user_key = %s;",
                    (blocked_user["key"],))

    log(
        cur=cur,
        user_key=user["key"],
        action="blocked" if blocked else "unblocked",
        entity_key=blocked_user["key"],
        entity_type="user",
        misc={"comment":  comment}
    )

    db_close(con, cur)
    return jsonify({
        "status": 200
    })
