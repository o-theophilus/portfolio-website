from flask import Blueprint, request

from ..tools import log, rate_limit, session

bp = Blueprint("like", __name__)


@bp.post("/like/post/<key>")
@session(True)
@rate_limit(10, 1)
@log("post")
def like_post(cur, user, key):
    cur.execute("""SELECT * FROM post WHERE key = %s;""", (key,))
    if not cur.fetchone():
        return {
            "error": "Invalid request"
        }, 404

    reaction = request.json.get("reaction")
    if reaction not in ["like", "dislike"]:
        return {
            "error": "Invalid request"
        }, 422

    cur.execute("""
        SELECT * FROM "like"
        WHERE user_key = %s AND post_key = %s;
    """, (user["key"], key))
    user_reaction = cur.fetchone()

    un = ""
    if not user_reaction:
        cur.execute("""
            INSERT INTO "like" (user_key, reaction, post_key)
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

    cur.execute("""
        SELECT
            COUNT(CASE WHEN user_key != %s
                AND reaction = 'like' THEN 1 END) AS others_like,
            COUNT(CASE WHEN user_key != %s
                AND reaction = 'dislike' THEN 1 END) AS others_dislike,
            MAX(CASE WHEN user_key = %s THEN reaction END) AS user_reaction
        FROM "like"
        WHERE post_key = %s;
    """, (user["key"], user["key"], user["key"], key))
    reactions = cur.fetchone()

    return {
        **reactions,
        "log": {
            "entity_key": key,
            "misc": {
                "action": f"{un}{reaction}"
            }
        }
    }, 200


@bp.post("/like/comment/<key>")
@session(True)
@rate_limit(20, 1)
@log("comment")
def like_comment(cur, user, key):
    cur.execute("""SELECT * FROM comment WHERE key = %s;""", (key,))
    if not cur.fetchone():
        return {
            "error": "Invalid request"
        }, 404

    reaction = request.json.get("reaction")
    if reaction not in ["like", "dislike"]:
        return {
            "error": "Invalid request"
        }, 422

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

    return {
        **reactions,
        "log": {
            "entity_key": key,
            "misc": {
                "action": f"{un}{reaction}"
            }
        }
    }, 200
