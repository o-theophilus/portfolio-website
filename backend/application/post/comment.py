from flask import Blueprint, jsonify, request

from ..log import log
from ..tools import rate_limit, session

bp = Blueprint("comment", __name__)


@bp.delete("/comments/<key>")
@session(True)
@rate_limit(20, 1)
def delete(cur, user, key):
    cur.execute("""
        SELECT * FROM comment WHERE key = %s AND user_key = %s;
    """, (key, user["key"]))
    comment = cur.fetchone()
    if not comment:
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    cur.execute("""DELETE FROM comment WHERE key = %s;""", (comment["key"],))

    log(
        cur=cur,
        user_key=user["key"],
        action="deleted comment",
        entity_type="comment",
        entity_key=comment["key"],
        misc={"post_key": comment["post_key"]}
    )

    return jsonify({
        "status": 200,
    })


@bp.post("/comments/<key>/like")
@session(True)
@rate_limit(20, 1)
def like(cur, user, key):
    reaction = request.json.get("reaction")

    cur.execute("""SELECT * FROM comment WHERE key = %s;""", (key,))
    if not cur.fetchone() or reaction not in ["like", "dislike"]:
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    cur.execute("""
        SELECT * FROM "like"
        WHERE user_key = %s AND comment_key = %s;
    """, (user["key"], key))
    user_reaction = cur.fetchone()

    un = ""
    if not user_reaction:
        cur.execute("""
            INSERT INTO "like" (user_key, reaction, comment_key)
            VALUES (%s, %s, %s);
        """, (user["key"], reaction, key))
    elif user_reaction["reaction"] == reaction:
        un = "un"
        cur.execute("""DELETE FROM "like" WHERE key = %s;""",
                    (user_reaction["key"],))
    else:
        cur.execute("""
            UPDATE "like"
            SET date_created = now(), reaction = %s WHERE key = %s;
        """, (reaction, user_reaction["key"]))

    log(
        cur=cur,
        user_key=user["key"],
        action=f"{un}{reaction} comment",
        entity_type="comment",
        entity_key=key,
    )

    cur.execute("""
        SELECT
            COUNT(CASE WHEN user_key != %s
                AND reaction = 'like' THEN 1 END) AS others_like,
            COUNT(CASE WHEN user_key != %s
                AND reaction = 'dislike' THEN 1 END) AS others_dislike,
            MAX(CASE WHEN user_key = %s THEN reaction END) AS user_reaction
        FROM "like"
        WHERE comment_key = %s;
    """, (user["key"], user["key"], user["key"], key))
    reactions = cur.fetchone()

    return jsonify({
        "status": 200,
        **reactions
    })


@bp.post("/comments/<key>/report")
@session(True)
@rate_limit(10, 1)
def report(cur, user, key):
    comment = request.json.get("comment", "").strip()
    tags = request.json.get("tags")

    if type(tags) is not list:
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    error = {}
    if not comment:
        error["comment"] = "This field is required"
    elif len(comment) > 500:
        error["comment"] = "This field cannot exceed 500 characters"
    if error:
        return jsonify({
            "status": 400,
            **error
        })

    cur.execute("""SELECT * FROM comment WHERE key = %s;""", (key,))
    reported_comment = cur.fetchone()
    if not reported_comment:
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    cur.execute("""
        INSERT INTO report (reporter_key, reporter_comment, tags,
            reported_key, reported_comment_key)
        VALUES (%s, %s, %s, %s, %s) RETURNING *;
    """, (
        user["key"], comment, tags,
        reported_comment["user_key"], reported_comment["key"])
    )
    report = cur.fetchone()

    log(
        cur=cur,
        user_key=user["key"],
        action="reported comment",
        entity_type="comment",
        entity_key=reported_comment["key"],
        misc={
            "report_key": report["key"]
        }
    )

    return jsonify({
        "status": 200
    })
