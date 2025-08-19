from flask import Blueprint, jsonify, request
from .tools import token_to_user
from math import ceil
from .postgres import db_close, db_open
from uuid import uuid4
from datetime import datetime
from psycopg2.extras import Json

bp = Blueprint("log", __name__)


@bp.post("/log")
def log(
    cur=None,
    user_key=None,
    action=None,
    entity_key=None,
    entity_type=None,
    status=200,
    misc={}
):
    close_conn = not cur
    if not cur:
        con, cur = db_open()

    try:
        if (
            not action
            and "action" in request.json
            and request.json["action"]
        ):
            action = request.json["action"]
        if (
            not entity_type
            and "entity_type" in request.json
            and request.json["entity_type"]
        ):
            entity_type = request.json["entity_type"]
        if (
            not entity_key
            and "entity_key" in request.json
            and request.json["entity_key"]
        ):
            entity_key = request.json["entity_key"]
        if (
            status == 200
            and "status" in request.json
            and request.json["status"]
            and request.json["status"] is int
        ):
            status = request.json["status"]
        if (
            misc == {}
            and "misc" in request.json
            and type(request.json["misc"]) is dict
        ):
            misc = request.json["misc"]
    except Exception:
        pass

    if not user_key:
        user = token_to_user(cur)
        if not user:
            if close_conn:
                db_close(con, cur)
            return jsonify({
                "status": 400,
                "error": "invalid user"
            })
        user_key = user["key"]

    cur.execute("""
        INSERT INTO log (
            key, date, user_key, action, entity_key, entity_type, status, misc
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
    """, (
        uuid4().hex,
        datetime.now(),
        user_key,
        action,
        entity_key,
        entity_type,
        status,
        Json(misc)
    ))

    if close_conn:
        db_close(con, cur)
    return jsonify({
        "status": 200
    })


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

    user = token_to_user(cur)
    if not user:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    page_no = 1
    page_size = 24
    u_search = ""
    entity_type = "all"
    action = "all"
    e_search = ""

    if "page_no" in request.args:
        page_no = int(request.args["page_no"])
    if "page_size" in request.args:
        page_size = int(request.args["page_size"])
    if "u_search" in request.args:
        u_search = request.args["u_search"].strip()
    if "entity_type" in request.args:
        entity_type = request.args["entity_type"]
    if "action" in request.args:
        action = request.args["action"]
    if "e_search" in request.args:
        e_search = request.args["e_search"].strip()

    if "log:view" not in user["access"]:
        u_search = user["key"]

    cur.execute("""
        SELECT
            log.key,
            log.date,
            log.status,
            log.misc,
            log.action,

            jsonb_build_object(
                'key', "user".key,
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
        LEFT JOIN "user" usr ON log.entity_key = usr.key
            AND (log.entity_type = 'user' OR log.entity_type = 'admin')
        LEFT JOIN
            post ON log.entity_key = post.key
            AND log.entity_type = 'post'
        LEFT JOIN
            comment ON log.entity_key = comment.key
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
        ORDER BY log.date DESC
        LIMIT %s OFFSET %s;
    """, (
        u_search, f"%{u_search}%",
        entity_type, entity_type,
        action, action,
        e_search, f"%{e_search}%",
        page_size, (page_no - 1) * page_size
    ))
    logs = cur.fetchall()

    for x in logs:
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

    sq = search_query(cur)
    db_close(con, cur)
    return jsonify({
        "status": 200,
        "logs": logs,
        "search_query": sq,
        "total_page": ceil(logs[0]["_count"] / page_size) if logs else 0
    })
