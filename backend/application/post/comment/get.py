from flask import Blueprint, jsonify, request
from ...postgres import db_close, db_open

bp = Blueprint("comment_get", __name__)


@bp.get("/<key>/comments")
def get_many(key, cur=None):
    close_conn = not cur
    if not cur:
        con, cur = db_open()

    order = request.args.get("order", "oldest")

    order_by = {
        'latest': 'comment.date_created',
        'oldest': 'comment.date_created',
        'likes': 'likes_count',
        'dislikes': 'dislikes_count',
        'most_liked': 'most_liked',
        'reply': 'reply_count',
        'most_reaction': 'total_reactions',
    }

    order_dir = {
        'latest': 'DESC',
        'oldest': 'ASC',
        'likes': 'DESC',
        'dislikes': 'DESC',
        'most_liked': 'DESC',
        'reply': 'DESC',
        'most_reaction': 'DESC',
    }

    cur.execute(f"""
        WITH stats AS (
            SELECT
                key,
                COALESCE(array_length(likes, 1), 0) AS likes_count,
                COALESCE(array_length(dislikes, 1), 0) AS dislikes_count,
                COALESCE(array_length(likes, 1), 0)
                    - COALESCE(array_length(dislikes, 1), 0) AS most_liked
            FROM comment
            WHERE post_key = %s
        ),
        reply AS (
            SELECT parent_key AS key, COUNT(*) AS reply_count
            FROM comment
            WHERE parent_key IS NOT NULL AND post_key = %s
            GROUP BY parent_key
        )

        SELECT
            comment.key,
            comment.comment,
            comment.parent_key,
            comment.likes,
            comment.dislikes,
            comment.date_created,
            jsonb_build_object(
                'key', "user".key,
                'name', "user".name,
                'photo', "user".photo
            ) AS user,

            stats.likes_count AS likes_count,
            stats.dislikes_count AS dislikes_count,
            stats.most_liked AS most_liked,
            COALESCE(reply.reply_count, 0) AS reply_count,
            (stats.likes_count + stats.dislikes_count
                + COALESCE(reply.reply_count, 0)) AS total_reactions


        FROM comment
        LEFT JOIN stats ON comment.key = stats.key
        LEFT JOIN reply ON comment.key = reply.key
        LEFT JOIN "user" ON comment.user_key = "user".key

        WHERE comment.post_key = %s

        ORDER BY {order_by[order]} {order_dir[order]};
    """, (key, key, key))

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
