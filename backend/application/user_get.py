from flask import Blueprint, request, jsonify
from .tools import token_to_user, user_schema
from math import ceil
from .postgres import db_close, db_open
from .admin import access


bp = Blueprint("user_get", __name__)


@bp.get("/user")
def get():
    con, cur = db_open()

    me = token_to_user(cur)
    if not me:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    user = None
    if "search" in request.args:
        if request.args["search"]:
            cur.execute("""
                SELECT *
                FROM "user"
                WHERE key = %s OR email = %s;
            """, (
                request.args["search"],
                request.args["search"]
            ))
            user = cur.fetchone()

        if not user:
            db_close(con, cur)
            return jsonify({
                "status": 400,
                "error": "user not found"
            })
    else:
        user = me

    _access = {}
    for x in access:
        if x not in _access:
            _access[x] = {}
            for y in access[x]:
                if y[1] not in _access[x]:
                    _access[x][y[1]] = []
                _access[x][y[1]].append(y[0])

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "user": user_schema(user),
        "access": _access
    })


@bp.get("/users")
def get_many():
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    if "user:view" not in user["access"]:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "unauthorized access"
        })

    order_by = {
        'latest': 'log.date',
        'oldest': 'log.date',
        'name (a-z)': '"user".name',
        'name (z-a)': '"user".name'
    }

    order_dir = {
        'latest': 'DESC',
        'oldest': 'ASC',
        'name (a-z)': 'ASC',
        'name (z-a)': 'DESC'
    }

    order = list(order_by.keys())[0]
    status = ""
    search = ""
    page_no = 1
    page_size = 24

    if "status" in request.args:
        status = request.args["status"]
    if "search" in request.args:
        search = request.args["search"].strip()
    if "order" in request.args:
        order = request.args["order"]
    if "page_no" in request.args:
        page_no = int(request.args["page_no"])
    if "size" in request.args:
        page_size = int(request.args["size"])

    cur.execute("""
        SELECT
            "user".*,
            log.date AS date,
            COUNT(*) OVER() AS _count
        FROM "user"
        LEFT JOIN log ON
            "user".key = log.user_key
            AND log.action = 'created'
            AND log.entity_type = 'account'
        WHERE
            (
                %s = '' OR "user".status = %s
            ) AND (
                %s = ''
                OR CONCAT_WS(', ', "user".key, "user".name, "user".email
                ) ILIKE %s
            )
        ORDER BY {} {}
        LIMIT %s OFFSET %s;
    """.format(
        order_by[order], order_dir[order]
    ), (
        status, status,
        search, f"%{search}%",
        page_size, (page_no - 1) * page_size
    ))
    users = cur.fetchall()

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "users": [user_schema(x) for x in users],
        "order_by": list(order_by.keys()),
        "_status": ['anonymous', 'signedup', 'confirmed', "deleted"],
        "total_page": ceil(users[0]["_count"] / page_size) if users else 0
    })


@bp.get("/admin/user")
def get_admins():
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    if "user:set_access" not in user["access"]:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "unauthorized access"
        })

    order_by = {
        'latest': 'log.date',
        'oldest': 'log.date',
        'name (a-z)': '"user".name',
        'name (z-a)': '"user".name'
    }

    order_dir = {
        'latest': 'DESC',
        'oldest': 'ASC',
        'name (a-z)': 'ASC',
        'name (z-a)': 'DESC'
    }

    order = list(order_by.keys())[0]
    page_no = 1
    page_size = 24
    search = ":all:all"

    if "order" in request.args:
        order = request.args["order"]
    if "page_no" in request.args:
        page_no = int(request.args["page_no"])
    if "size" in request.args:
        page_size = int(request.args["size"])
    if "search" in request.args:
        search = request.args["search"]
    search = search.split(":")
    if len(search) != 3:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid search"
        })
    user_key, _type, _action = search
    user_key = user_key.strip()

    cur.execute("""
        SELECT
            "user".*,
            COUNT(*) OVER() AS _count
        FROM "user"
        LEFT JOIN log ON
            "user".key = log.user_key
            AND log.action = 'created'
            AND log.entity_type = 'account'
        WHERE
            array_length("user".access, 1) IS NOT NULL
            -- AND "user".status = "confirmed"
            AND (%s = ''
                OR CONCAT_WS(', ', "user".key, "user".name, "user".email)
                ILIKE %s)
            AND (%s = 'all' OR ARRAY_TO_STRING("user".access, ',')
                ILIKE %s)
            AND (%s = 'all' OR ARRAY_TO_STRING("user".access, ',')
                ILIKE %s)
        ORDER BY {} {}
        LIMIT %s OFFSET %s;
    """.format(
        order_by[order], order_dir[order]
    ), (
        user_key, f"%{user_key}%",
        _type, f"%{_type}:%",
        _action, f"%{_type}:{_action}%",
        page_size, (page_no - 1) * page_size
    ))
    users = cur.fetchall()

    _access = {
        "all": ['all']
    }
    for x in access:
        if x not in _access:
            _access[x] = ["all"]
            for y in access[x]:
                _access[x].append(y[0])

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "users": [user_schema(x) for x in users],
        "access": _access,
        "order_by": list(order_by.keys()),
        "total_page": ceil(users[0]["_count"] / page_size) if users else 0
    })
