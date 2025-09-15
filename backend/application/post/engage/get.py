from flask import Blueprint, jsonify
from ...postgres import db_close, db_open
from ...tools import get_session

bp = Blueprint("post_engage_get", __name__)


@bp.get("/post/engagement/<key>")
def engagement(key):
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    cur.execute("""
        WITH
        _like AS (
            SELECT
                entity_key AS key,
                COUNT(*) FILTER (WHERE reaction = 'like') AS "like",
                COUNT(*) FILTER (WHERE reaction = 'dislike') AS dislike
            FROM "like"
            WHERE entity_type = 'post' AND user_key != %s
            GROUP BY entity_key
        ),

        user_like AS (
            SELECT
                entity_key AS key, reaction
            FROM "like"
            WHERE entity_type = 'post' AND user_key = %s
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
            COALESCE(_like."like", 0) AS "like",
            COALESCE(_like.dislike, 0) AS dislike,
            user_like.reaction AS user_like
        FROM post
        LEFT JOIN _like ON post.key = _like.key
        LEFT JOIN comment ON post.key = comment.key
        LEFT JOIN view ON post.key = view.key
        LEFT JOIN share ON post.key = share.key
        LEFT JOIN user_like ON post.key = user_like.key

        WHERE post.key = %s
        GROUP BY
            post.key, post.status, post.title, post.slug, post.content,
            post.description, post.files, post.tags,
            _like."like", _like.dislike, comment._count, view._count,
            share._count, user_like.reaction
    """, (user["key"], user["key"], key))
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
