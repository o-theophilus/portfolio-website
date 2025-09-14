from flask import Blueprint, jsonify
from ...postgres import db_close, db_open
from ...tools import get_session

bp = Blueprint("post_engage_get", __name__)


@bp.get("/post/engagement/<key>")
def engagement(key):
    con, cur = db_open()

    cur.execute("""
        WITH
        "like" AS (
            SELECT
                entity_key AS key,
                COUNT(*) FILTER (WHERE reaction = 'like') -
                COUNT(*) FILTER (WHERE reaction = 'dislike') AS _count
            FROM "like"
            WHERE entity_type = 'post'
            GROUP BY entity_key
        ),

        comment AS (
            SELECT post_key AS key, COUNT(*) AS _count
            FROM comment
            GROUP BY post_key
        ),

        view AS (
            SELECT entity_key::UUID AS key, COUNT(DISTINCT user_key) AS _count
            FROM log
            WHERE entity_type = 'post' AND action = 'viewed'
            GROUP BY entity_key
        ),

        share AS (
            SELECT entity_key::UUID AS key, COUNT(*) AS _count
            FROM log
            WHERE entity_type = 'post' AND action = 'shared'
            GROUP BY entity_key
        )

        SELECT
            COALESCE(comment._count, 0) AS comment,
            COALESCE(view._count, 0) AS view,
            COALESCE(share._count, 0) AS share,
            COALESCE("like"._count, 0) AS "like"
        FROM post
        LEFT JOIN "like" ON post.key = "like".key
        LEFT JOIN comment ON post.key = comment.key
        LEFT JOIN view ON post.key = view.key
        LEFT JOIN share ON post.key = share.key

        WHERE post.slug = %s OR post.key::TEXT = %s
        GROUP BY
            post.key, post.status, post.title, post.slug, post.content,
            post.description, post.files, post.tags,
            "like"._count, comment._count, view._count, share._count
    """, (key, key))
    engagement = cur.fetchone()

    if not engagement:
        db_close(con, cur)
        return jsonify({
            "status": 404,
            "error": "Invalid request"
        })

    db_close(con, cur)
    return jsonify({
        "status": 200,
        **engagement
    })


@bp.get("/post/user_engagements/<key>")
def get(key):
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    cur.execute("""
        SELECT * FROM "like"
        WHERE user_key != %s AND entity_type = 'post' AND entity_key = %s
    ;""", (user["key"], key))
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
        WHERE user_key = %s AND entity_type = 'post' AND entity_key = %s
    ;""", (user["key"], key))
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
