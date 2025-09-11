from flask import Blueprint, jsonify, request
from ...tools import get_session
from ...postgres import db_close, db_open
from ...log import log

bp = Blueprint("comment_engage", __name__)


@bp.post("/comment/like/<key>")
def like(key):
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    cur.execute("""
        SELECT
            comment.key,
            comment.date_created,
            comment.post_key,
            comment.parent_key,
            comment.comment,
            comment.likes,
            comment.dislikes,
            jsonb_build_object(
                'key', "user".key,
                'name', "user".name,
                'photo', "user".photo
            ) AS user

        FROM comment
        LEFT JOIN "user" ON comment.user_key = "user".key
        WHERE comment.key = %s;
    """, (key,))
    comment = cur.fetchone()

    like = request.json.get("like")

    if not comment or type(like) is not bool:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    comment["user"]["photo"] = (
        f"{request.host_url}file/{comment['user']['photo']}"
        if comment["user"]["photo"] else None
    )

    if like:
        if user["key"] in comment["dislikes"]:
            comment["dislikes"].remove(user["key"])
        if user["key"] in comment["likes"]:
            comment["likes"].remove(user["key"])
        else:
            comment["likes"].append(user["key"])
    else:
        if user["key"] in comment["likes"]:
            comment["likes"].remove(user["key"])
        if user["key"] in comment["dislikes"]:
            comment["dislikes"].remove(user["key"])
        else:
            comment["dislikes"].append(user["key"])

    cur.execute("""
        UPDATE comment SET likes = %s, dislikes = %s WHERE key = %s;
    """, (comment["likes"], comment["dislikes"], comment["key"]))

    log(
        cur=cur,
        user_key=user["key"],
        action='liked' if like else 'disliked',
        entity_key=comment["key"],
        entity_type="comment",
        misc={"post_key": comment["post_key"]}
    )

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "comment": comment

    })
