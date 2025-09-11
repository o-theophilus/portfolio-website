from flask import Blueprint, jsonify
from ...postgres import db_close, db_open
from ..get import post_schema

bp = Blueprint("post_engage_get", __name__)


@bp.get("/post/engagements/<key>")
def get(key):
    con, cur = db_open()

    cur.execute("""
        SELECT * FROM post WHERE post.slug = %s OR post.key = %s;
    """, (key, key))
    item = cur.fetchone()

    if not item:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    cur.execute("""
        WITH
        _like AS (
            SELECT
                key,
                COALESCE(array_length(likes, 1), 0) -
                COALESCE(array_length(dislikes, 1), 0) AS _count
            FROM post
        ),

        ratings AS (
            SELECT key,
            (jsonb_array_elements(ratings) ->> 'rating')::INTEGER AS ratings
            FROM post
        ),
        rating AS (
            SELECT key, AVG(ratings) AS rating
            FROM ratings
            GROUP BY key
        ),

        comment AS (
            SELECT
                post_key AS key,
                COUNT(*) AS _count
            FROM comment
            GROUP BY post_key
        ),

        view1 AS (
            SELECT
                DISTINCT ON (user_key, entity_key)
                entity_key
            FROM log
            WHERE
                entity_type = 'post'
                AND action = 'viewed'
        ),
        view AS (
            SELECT
                entity_key AS key,
                COUNT(*) AS _count
            FROM view1
            GROUP BY entity_key
        ),

        share1 AS (
            SELECT entity_key
            FROM log
            WHERE
                entity_type = 'post'
                AND action = 'shared'
        ),
        share AS (
            SELECT
                entity_key AS key,
                COUNT(*) AS _count
            FROM share1
            GROUP BY entity_key
        )

        SELECT
            post.*,
            COALESCE(rating.rating, 0) AS rating,
            COALESCE(comment._count, 0) AS comment,
            COALESCE(view._count, 0) AS view,
            COALESCE(share._count, 0) AS share,
            COALESCE(_like._count, 0) AS _like,
            COUNT(*) OVER() AS _count
        FROM post
        LEFT JOIN _like ON post.key = _like.key
        LEFT JOIN rating ON post.key = rating.key
        LEFT JOIN comment ON post.key = comment.key
        LEFT JOIN view ON post.key::TEXT = view.key
        LEFT JOIN share ON post.key::TEXT = share.key

        WHERE post.key = %s
        GROUP BY
            post.key, post.status, post.title, post.slug, post.content,
            post.description, post.files, post.tags,
            _like._count, comment._count, view._count, share._count,
            rating.rating
    ;""", (item["key"],))
    item = cur.fetchone()

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "item": post_schema(item)
    })
