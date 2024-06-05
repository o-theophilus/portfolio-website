from flask import Blueprint, jsonify, request
from .tools import token_to_user
from math import ceil
from .postgres import db_close, db_open
from uuid import uuid4
from datetime import datetime
import json

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
        if "action" in request.json and request.json["action"]:
            action = request.json["action"]
        if "entity_type" in request.json and request.json["entity_type"]:
            entity_type = request.json["entity_type"]
        if "entity_key" in request.json and request.json["entity_key"]:
            entity_key = request.json["entity_key"]
        if "status" in request.json and request.json["status"]:
            status = int(request.json["status"])
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
        json.dumps(misc)
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
    search = ":all:all:"

    if "page_no" in request.args:
        page_no = int(request.args["page_no"])
    if "page_size" in request.args:
        page_size = int(request.args["page_size"])
    if "search" in request.args:
        search = request.args["search"]
    search = search.split(":")
    if len(search) != 4:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid search"
        })
    user_key, entity_type, user_action, entity_key = search
    user_key = user_key.strip()
    entity_key = entity_key.strip()

    if "log:view" not in user["permissions"]:
        user_key = user["key"]

    cur.execute("""
        SELECT
            log.*,
            "user".name AS user_name,
            COALESCE(usr.name, post.title, log.entity_key
            ) AS entity_name,
            COUNT(*) OVER() AS total_page
        FROM log
        LEFT JOIN "user" ON log.user_key = "user".key
        LEFT JOIN "user" usr ON log.entity_key = usr.key
            AND (log.entity_type = 'user' OR log.entity_type = 'admin')
        LEFT JOIN
            post ON log.entity_key = post.key
            AND log.entity_type = 'post'
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
        user_key, f"%{user_key}%",
        entity_type, entity_type,
        user_action, user_action,
        entity_key, f"%{entity_key}%",
        page_size, (page_no - 1) * page_size
    ))
    logs = cur.fetchall()

    sq = search_query(cur)

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "logs": logs,
        "search_query": sq,
        "total_page": ceil(logs[0]["total_page"] / page_size) if logs else 0
    })
