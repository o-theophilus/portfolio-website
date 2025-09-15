from flask import Blueprint, jsonify, request
from ...postgres import db_close, db_open
from ...tools import get_session

bp = Blueprint("comment_get", __name__)


@bp.get("/<key>/comments")
def get_many(key, cur=None):
    close_conn = not cur
    if not cur:
        con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    order = request.args.get("order", "oldest")

    order_by = {
        'latest': 'comment.date_created',
        'oldest': 'comment.date_created',
        'like': 'engagement."like"',
        'dislike': 'engagement.dislike',
        'most_like': 'engagement.most_like',
        'reply': 'engagement.reply',
        'most_engaged': 'engagement.total',
    }

    order_dir = {
        'latest': 'DESC',
        'oldest': 'ASC',
        'like': 'DESC',
        'dislike': 'DESC',
        'most_like': 'DESC',
        'reply': 'DESC',
        'most_engaged': 'DESC',
    }

    cur.execute(f"""
        WITH
        _like AS (
            SELECT
                entity_key AS key,
                COUNT(*) FILTER (WHERE reaction = 'like') AS "like",
                COUNT(*) FILTER (WHERE reaction = 'dislike') AS dislike
            FROM "like"
            WHERE entity_type = 'comment' AND user_key != %s
            GROUP BY entity_key
        ),
        user_like AS (
            SELECT
                entity_key AS key, reaction
            FROM "like"
            WHERE entity_type = 'comment' AND user_key = %s
        ),
        reply AS (
            SELECT
                parent_key AS key,
                COUNT(*) AS reply_count
            FROM comment
            WHERE parent_key IS NOT NULL
            GROUP BY parent_key
        ),

        engagement AS (
            SELECT
                comment.key,
                COALESCE(_like."like", 0) AS "like",
                COALESCE(_like.dislike, 0) AS dislike,
                COALESCE(_like."like", 0)
                - COALESCE(_like.dislike, 0) AS most_like,
                COALESCE(reply.reply_count, 0) AS reply,
                COALESCE(_like."like", 0)
                + COALESCE(_like.dislike, 0)
                + COALESCE(reply.reply_count, 0) AS total
            FROM comment
            LEFT JOIN _like ON comment.key = _like.key
            LEFT JOIN reply ON comment.key = reply.key
        )

        SELECT
            comment.key,
            comment.date_created,
            comment.comment,
            comment.parent_key,
            jsonb_build_object(
                'key', "user".key,
                'name', "user".name,
                'username', "user".username,
                'photo', "user".photo
            ) AS user,
            jsonb_build_object(
                'like', COALESCE(engagement."like", 0),
                'dislike', COALESCE(engagement.dislike, 0),
                'most_like', COALESCE(engagement.most_like, 0),
                'reply', COALESCE(engagement.reply, 0),
                'most_engaged', COALESCE(engagement.total, 0),

                'user_like', user_like.reaction
            ) AS engagement
        FROM comment
        LEFT JOIN engagement ON comment.key = engagement.key
        LEFT JOIN "user" ON comment.user_key = "user".key
        LEFT JOIN user_like ON comment.key = user_like.key
        WHERE comment.post_key = %s
        ORDER BY {order_by[order]} {order_dir[order]};
    """, (user["key"], user["key"], key))

    items = cur.fetchall()

    for x in items:
        x["user"]["photo"] = (
            f"{request.host_url}file/{x['user']['photo']}"
            if x["user"]["photo"] else None
        )

    if close_conn:
        db_close(con, cur)
    return jsonify({
        "status": 200,
        "items": items,
        "order_by": list(order_by.keys()),
    })
