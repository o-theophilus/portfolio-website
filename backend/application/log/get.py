from flask import Blueprint, jsonify, request
from math import ceil
from ..tools import get_session
from ..postgres import db_close, db_open

bp = Blueprint("log_get", __name__)


def search_query(cur):
    cur.execute("""
        SELECT DISTINCT ON (entity_type, action) entity_type, action
        FROM log;
    """)

    actions = {"all": ["all"]}
    for x in cur.fetchall():
        if x["entity_type"] in actions:
            actions[x["entity_type"]].append(x["action"])
        else:
            actions[x["entity_type"]] = ["all", x["action"]]

    return actions


@bp.get("/log")
def get_many():
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    u_search = request.args.get("u_search", "").strip()
    entity_type = request.args.get("entity_type", "all")
    action = request.args.get("action", "all")
    e_search = request.args.get("e_search", "").strip()
    page_no = int(request.args.get("page_no", 1))
    page_size = int(request.args.get("page_size", 24))

    if "log:view" not in user["access"]:
        u_search = user["key"]

    cur.execute("""
        SELECT
            log.key,
            log.date_created,
            log.status,
            log.misc,
            log.action,

            jsonb_build_object(
                'key', "user".key,
                'username', "user".username,
                'name', "user".name
            ) AS user,

            jsonb_build_object(
                'key', log.entity_key,
                'type', log.entity_type,
                'name', COALESCE(usr.name, post.title, comment.comment,
                    log.entity_key)
            ) AS entity,

            COUNT(*) OVER() AS _count

        FROM log
        LEFT JOIN "user" ON log.user_key = "user".key
        LEFT JOIN "user" usr ON log.entity_key = usr.key::TEXT
            AND (log.entity_type = 'user' OR log.entity_type = 'admin')
        LEFT JOIN
            post ON log.entity_key = post.key::TEXT
            AND log.entity_type = 'post'
        LEFT JOIN
            comment ON log.entity_key = comment.key::TEXT
            AND log.entity_type = 'comment'

        WHERE
            (%s = '' OR CONCAT_WS(
                ', ', log.user_key, "user".name, "user".email
            ) ILIKE %s)
            AND (%s = 'all' OR log.entity_type = %s)
            AND (%s = 'all' OR log.action = %s)
            AND (%s = '' OR CONCAT_WS(
                ', ', log.entity_key, usr.name, usr.email, post.title
            ) ILIKE %s)
        ORDER BY log.date_created DESC
        LIMIT %s OFFSET %s;
    """, (
        u_search, f"%{u_search}%",
        entity_type, entity_type,
        action, action,
        e_search, f"%{e_search}%",
        page_size, (page_no - 1) * page_size
    ))
    items = cur.fetchall()

    for x in items:
        if x["entity"]["type"] == "page":
            x["action"] = "viewed"

        elif x["entity"]["type"] == "report":
            x["entity"]["name"] = x["entity"]["name"][-10:]

        elif x["entity"]["type"] == "comment":
            length = 20
            ellipsis = "..." if len(x["entity"]["name"]) > length else ""
            x["entity"]["name"] = f"{x['entity']['name'][:length]}{ellipsis}"

        elif x["entity"]["type"] == "user":
            if x["action"] == "viewed":
                if x["user"]["key"] == x["entity"]["key"]:
                    x["entity"]["type"] = "profile"
            elif x["action"] == "changed_theme":
                x["entity"]["type"] = ""
                x["entity"]["key"] = ""

    sq = search_query(cur)
    db_close(con, cur)
    return jsonify({
        "status": 200,
        "items": items,
        "search_query": sq,
        "total_page": ceil(items[0]["_count"] / page_size) if items else 0
    })
