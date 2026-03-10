from math import ceil

from flask import Blueprint, jsonify, request

from ..postgres import db_close, db_open
from ..tools import access_pass, get_session, user_schema

bp = Blueprint("user_get", __name__)


@bp.get("/users/<key>")
def get_user(key):
    con, cur = db_open()

    session = get_session(cur)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)

    cur.execute("""
        SELECT
            "user".*,
            CASE WHEN block.user_key IS NOT NULL
                THEN true ELSE false END AS blocked
        FROM "user"
        LEFT JOIN block ON "user".key = block.user_key
        WHERE "user".key::TEXT = %s OR "user".username = %s;
    """, (key, key))
    user = cur.fetchone()

    if not user:
        db_close(con, cur)
        return jsonify({
            "status": 404,
            "error": "Oops! The user you're looking for doesn't exist"
        })

    _access = {}
    for x in access_pass:
        if x not in _access:
            _access[x] = {}
            for y in access_pass[x]:
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
def get_users():
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)

    if "user.view" not in session["user"]["access"]:
        db_close(con, cur)
        return jsonify({
            "status": 403,
            "error": "unauthorized access"
        })

    order_by = {
        'latest': 'date_created',
        'oldest': 'date_created',
        'name (a-z)': 'name',
        'name (z-a)': 'name'
    }

    order_dir = {
        'latest': 'DESC',
        'oldest': 'ASC',
        'name (a-z)': 'ASC',
        'name (z-a)': 'DESC'
    }

    searchParams = {
        "search": "",
        "status": "active",
        "order": "latest",
        "page_no": 1,
        "page_size": 24
    }
    search = request.args.get("search", searchParams["search"]).strip()
    status = request.args.get("status", searchParams["status"])
    order = request.args.get("order", searchParams["order"])
    page_no = int(request.args.get("page_no", searchParams["page_no"]))
    page_size = int(request.args.get("page_size", searchParams["page_size"]))
    page_size = min(page_size, 100)

    cur.execute(f"""
        SELECT
            "user".*,
            CASE WHEN block.user_key IS NOT NULL
                THEN true ELSE false END AS blocked
        FROM "user"
        LEFT JOIN block ON "user".key = block.user_key
        WHERE (
                %s = 'all' OR "user".status = %s
            ) AND (
                %s = ''
                OR CONCAT_WS(', ', "user".key, "user".name, "user".email
            ) ILIKE %s
        )
        ORDER BY {order_by[order]} {order_dir[order]}, "user".key DESC
        LIMIT %s OFFSET %s;
    """, (
        status, status,
        search, f"%{search}%",
        page_size, (page_no - 1) * page_size
    ))
    users = cur.fetchall()

    cur.execute("""
        SELECT COUNT(*) FROM "user"
        WHERE (
                %s = 'all' OR status = %s
            ) AND (%s = '' OR CONCAT_WS(', ', key, name, email) ILIKE %s
        );
    """, (
        status, status,
        search, f"%{search}%",
    ))
    total_page = cur.fetchone()["count"]

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "users": [user_schema(x) for x in users],
        "order_by": list(order_by.keys()),
        "_status": ['anonymous', 'signedup', 'active'],
        "total_page": ceil(total_page / page_size),
        "searchParams": searchParams
    })


@bp.get("/users/admin")
def get_admin_users():
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    if "user.set_access" not in user["access"]:
        db_close(con, cur)
        return jsonify({
            "status": 403,
            "error": "unauthorized access"
        })

    order_by = {
        'latest': 'date_created',
        'oldest': 'date_created',
        'name (a-z)': 'name',
        'name (z-a)': 'name'
    }

    order_dir = {
        'latest': 'DESC',
        'oldest': 'ASC',
        'name (a-z)': 'ASC',
        'name (z-a)': 'DESC'
    }

    searchParams = {
        "entity_type": "all",
        "action": "all",
        "search": "",
        "order": "latest",
        "page_no": 1,
        "page_size": 24
    }
    entity_type = request.args.get("entity_type", searchParams["entity_type"])
    action = request.args.get("action", searchParams["action"])
    search = request.args.get("search", searchParams["search"]).strip()
    order = request.args.get("order", searchParams["order"])
    page_no = int(request.args.get("page_no", searchParams["page_no"]))
    page_size = int(request.args.get("page_size", searchParams["page_size"]))
    page_size = min(page_size, 100)

    cur.execute(f"""
        SELECT
            "user".*,
            CASE WHEN block.user_key IS NOT NULL
                THEN true ELSE false END AS blocked,
            COUNT(*) OVER() AS _count
        FROM "user"
        LEFT JOIN block ON "user".key = block.user_key
        WHERE
            array_length("user".access, 1) IS NOT NULL
            AND (%s = '' OR CONCAT_WS(
                ', ', "user".key, "user".name, "user".email) ILIKE %s)
            AND (%s = 'all' OR ARRAY_TO_STRING("user".access, ',') ILIKE %s)
            AND (%s = 'all' OR ARRAY_TO_STRING("user".access, ',') ILIKE %s)
        ORDER BY {order_by[order]} {order_dir[order]}, "user".key DESC
        LIMIT %s OFFSET %s;
    """, (
        search, f"%{search}%",
        entity_type, f"%{entity_type}:%",
        action, f"%{entity_type}:{action}%",
        page_size, (page_no - 1) * page_size
    ))
    users = cur.fetchall()

    access = {
        "all": ['all']
    }
    for x in access_pass:
        if x not in access:
            access[x] = ["all"]
            for y in access_pass[x]:
                access[x].append(y[0])

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "users": [user_schema(x) for x in users],
        "access": access,
        "order_by": list(order_by.keys()),
        "total_page": ceil(users[0]["_count"] / page_size) if users else 0,
        "searchParams": searchParams
    })


@bp.get("/users/block")
def get_blocked_users(cur=None):
    close_conn = not cur
    if not cur:
        con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        if close_conn:
            db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    if "block.view" not in user["access"]:
        if close_conn:
            db_close(con, cur)
        return jsonify({
            "status": 403,
            "error": "unauthorized access"
        })

    order_by = {
        'latest': 'date_created',
        'oldest': 'date_created'
    }
    order_dir = {
        'latest': 'DESC',
        'oldest': 'ASC'
    }

    searchParams = {
        "search": "",
        "order": "latest",
        "page_no": 1,
        "page_size": 24
    }
    search = request.args.get("search", searchParams["search"]).strip()
    order = request.args.get("order", searchParams["order"])
    page_no = int(request.args.get("page_no", searchParams["page_no"]))
    page_size = int(request.args.get("page_size", searchParams["page_size"]))
    page_size = min(page_size, 100)

    cur.execute(f"""
        SELECT
            block.key,
            block.date_created,
            block.comment,

            jsonb_build_object(
                'key', admin.key,
                'name', admin.name,
                'username', admin.username,
                'photo', admin.photo
            ) AS admin,

            jsonb_build_object(
                'key', "user".key,
                'name', "user".name,
                'username', "user".username,
                'photo', "user".photo
            ) AS "user",

            COUNT(*) OVER() AS _count

        FROM block
        LEFT JOIN "user" admin ON block.admin_key = admin.key
        LEFT JOIN "user" ON block.user_key = "user".key

        WHERE
            (%s = '' OR CONCAT_WS(', ',
                block.key, block.comment,
                "user".key, "user".name, "user".email,
                admin.key, admin.name, admin.email
            ) ILIKE %s)
        ORDER BY {order_by[order]} {order_dir[order]}, block.key DESC
        LIMIT %s OFFSET %s;
    """, (
        search, f"%{search}%",
        page_size, (page_no - 1) * page_size
    ))
    blocks = cur.fetchall()

    for x in blocks:
        x["admin"]["photo"] = (
            f"{request.host_url}photo/user/{x['admin']['photo']}"
            if x["admin"]["photo"] else None
        )
        x["user"]["photo"] = (
            f"{request.host_url}photo/user/{x['user']['photo']}"
            if x["user"]["photo"] else None
        )

    if close_conn:
        db_close(con, cur)
    return jsonify({
        "status": 200,
        "blocks": blocks,
        "total_page": ceil(blocks[0]["_count"] / page_size) if blocks else 0,
        "order_by": list(order_by.keys()),
        "searchParams": searchParams,
    })
