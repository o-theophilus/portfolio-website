from math import ceil

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

    order_by = {
        'latest': 'c.date_created',
        'oldest': 'c.date_created',
        'most reply': 'reply_count',
        # 'like': '"like"',
        # 'dislike': 'dislike',
        'most relevant': 'most_like',
        # 'most engaged': 'most_engaged',
    }
    order_dir = {
        'latest': 'DESC',
        'oldest': 'ASC',
        'most reply': 'DESC',
        'like': 'DESC',
        'dislike': 'DESC',
        'most relevant': 'DESC',
        'most engaged': 'DESC',
    }

    searchParams = {
        "order": 'most relevant',
        "page_no": 1,
        "page_size": 24
    }
    order = request.args.get("order", searchParams["order"])
    page_no = int(request.args.get("page_no", searchParams["page_no"]))
    page_size = int(request.args.get("page_size", searchParams["page_size"]))
    page_size = min(page_size, 100)

    cur.execute(f"""
        SELECT
            c.key, c.date_created, c.comment, c.parent_key,
            u.key AS user_key, u.name, u.username, u.photo,
            COALESCE(sub_c.reply_count, 0) AS reply_count,
            COALESCE(l."like", 0) AS "like",
            COALESCE(l.dislike, 0) AS dislike,
            COALESCE(l."like", 0) - COALESCE(l.dislike, 0) AS most_like,
            COALESCE(sub_c.reply_count, 0) + COALESCE(l."like", 0)
                + COALESCE(l.dislike, 0) AS most_engaged
        FROM comment c
        JOIN "user" u ON u.key = c.user_key

        LEFT JOIN (
            SELECT parent_key, COUNT(*) AS reply_count
            FROM comment
            WHERE parent_key IS NOT NULL
                AND post_key = %s
            GROUP BY parent_key
        ) sub_c ON sub_c.parent_key = c.key

        LEFT JOIN (
            SELECT comment_key,
                COUNT(*) FILTER (WHERE reaction = 'like') AS "like",
                COUNT(*) FILTER (WHERE reaction = 'dislike') AS dislike
            FROM "like"
            WHERE comment_key IS NOT NULL
            GROUP BY comment_key
        ) l ON l.comment_key = c.key

        WHERE c.post_key = %s AND c.parent_key IS NULL
        ORDER BY {order_by[order]} {order_dir[order]}, c.key DESC
        LIMIT %s OFFSET %s;
    """, (key, key, page_size, (page_no - 1) * page_size))
    comments = cur.fetchall()
    replies = []
    likes = []

    if comments:
        comment_keys = [r["key"] for r in comments]

        cur.execute("""
            SELECT
                c.key, c.date_created, c.comment, c.parent_key,
                u.key AS user_key, u.name, u.username, u.photo
            FROM comment c
            JOIN "user" u ON u.key = c.user_key
            WHERE c.parent_key::TEXT = ANY(%s)
            ORDER BY c.date_created ASC
        """, (comment_keys,))
        replies = cur.fetchall()

        for x in replies:
            comment_keys.append(x["key"])

        cur.execute("""
            SELECT
                comment_key,
                COUNT(*) FILTER (WHERE reaction = 'like' AND user_key != %s)
                    AS others_like,
                COUNT(*) FILTER (WHERE reaction = 'dislike' AND user_key != %s)
                    AS others_dislike,
                MAX(reaction) FILTER (WHERE user_key = %s) AS user_reaction
            FROM "like"
            WHERE comment_key::TEXT = ANY(%s)
            GROUP BY comment_key
        """, (user["key"], user["key"], user["key"], comment_keys))
        likes = cur.fetchall()

    likes_map = {
        x["comment_key"]: {
            "others_like": x["others_like"],
            "others_dislike": x["others_dislike"],
            "user_reaction": x["user_reaction"]
        }
        for x in likes
    }

    replies_map = {}
    for x in replies:
        replies_map.setdefault(x["parent_key"], []).append({
            "key": x["key"],
            "date_created": x["date_created"],
            "comment": x["comment"],
            "user": {
                "key": x["user_key"],
                "name": x["name"],
                "username": x["username"],
                "photo": f'{request.host_url}photo/user/{x["photo"]}' if x[
                    "photo"] else None
            },
            "engagement": likes_map.get(x["key"], {
                "others_like": 0,
                "others_dislike": 0,
                "user_reaction": None
            }),
        })

    final_comments = []
    for x in comments:
        final_comments.append({
            "key": x["key"],
            "date_created": x["date_created"],
            "comment": x["comment"],
            "user": {
                "key": x["user_key"],
                "name": x["name"],
                "username": x["username"],
                "photo": f'{request.host_url}photo/user/{x["photo"]}' if x[
                    "photo"] else None
            },
            "engagement": likes_map.get(x["key"], {
                "others_like": 0,
                "others_dislike": 0,
                "user_reaction": None
            }),
            "replies": replies_map.get(x["key"], [])
        })

    cur.execute("""
        SELECT
            COUNT(*) AS total,
            COUNT(*) FILTER (WHERE parent_key IS NULL) AS total_parent
        FROM comment WHERE post_key = %s;
    """, (key,))
    row = cur.fetchone()
    total = row["total"]
    total_parent = row["total_parent"]

    if close_conn:
        db_close(con, cur)
    return jsonify({
        "status": 200,
        "comments": final_comments,
        "order_by": list(order_by.keys()),
        "total_comment": total,
        "total_page": ceil(total_parent / page_size),
        "searchParams": searchParams,
    })
