from flask import Blueprint, jsonify, request
from datetime import datetime, timezone
from ...tools import get_session
from ...postgres import db_close, db_open
from ...log import log

bp = Blueprint("post_engage", __name__)


@bp.post("/like")
def like():
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    entity_key = request.json.get("entity_key")
    entity_type = request.json.get("entity_type")
    reaction = request.json.get("reaction")

    if (
        entity_type not in ["post", "comment"]
        or reaction not in ["like", "dislike"]
    ):
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    cur.execute(f"""
        SELECT * FROM {entity_type} WHERE key = %s;
    """, (entity_key,))
    if not cur.fetchone():
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    cur.execute("""
        SELECT * FROM "like"
        WHERE user_key = %s AND entity_type = %s AND entity_key = %s;
    """, (user["key"], entity_type, entity_key))
    like = cur.fetchone()

    un = ""
    if not like:
        cur.execute("""
            INSERT INTO "like" (user_key, entity_type, entity_key, reaction)
            VALUES (%s, %s, %s, %s);
        """, (user["key"], entity_type, entity_key, reaction))
    elif (
            like["reaction"] == "like" and reaction == "dislike"
            or like["reaction"] == "dislike" and reaction == "like"
    ):
        cur.execute("""
            UPDATE "like"
            SET date_created = %s, reaction = %s WHERE key = %s;
        """, (datetime.now(timezone.utc), reaction, like["key"]))
    else:
        un = "un"
        cur.execute("""DELETE FROM "like" WHERE key = %s;""", (like["key"],))

    log(
        cur=cur,
        user_key=user["key"],
        action=f"{un}{reaction}",
        entity_key=entity_key,
        entity_type=entity_type
    )

    cur.execute("""
        SELECT * FROM "like"
        WHERE user_key != %s AND entity_type = %s AND entity_key = %s
    ;""", (user["key"], entity_type, entity_key))
    reactions = cur.fetchall()

    like = 0
    dislike = 0
    for x in reactions:
        if x["reaction"] == "like":
            like += 1
        if x["reaction"] == "dislike":
            dislike += 1

    cur.execute("""
        SELECT * FROM "like"
        WHERE user_key = %s AND entity_type = %s AND entity_key = %s
    ;""", (user["key"], entity_type, entity_key))
    user_reaction = cur.fetchone()

    user_like = None
    if user_reaction:
        user_like = user_reaction["reaction"]

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "like": like,
        "dislike": dislike,
        "user_like": user_like,
    })
