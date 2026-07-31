from math import ceil

from flask import Blueprint, request

from ..tools import access_pass, session, user_schema

bp = Blueprint("user_get", __name__)


@bp.get("/users/<key>")
@session(False)
def get(cur, _user, key):
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
        return {
            "error": "Oops! The user you're looking for doesn't exist"
        }, 404

    _access = {}
    for x in access_pass:
        if x not in _access:
            _access[x] = {}
            for y in access_pass[x]:
                if y[1] not in _access[x]:
                    _access[x][y[1]] = []
                _access[x][y[1]].append(y[0])

    return {
        "user": user_schema(user),
        "access": _access
    }, 200


@bp.get("/users")
@session(True)
def many(cur, user):
    if "user.view" not in user["access"]:
        return {
            "error": "unauthorized access"
        }, 403

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

    search_params = {
        "search": "",
        "status": "active",
        "order": "latest",
        "page_no": 1,
        "page_size": 24
    }
    search = request.args.get("search", search_params["search"]).strip()
    status = request.args.get("status", search_params["status"])
    order = request.args.get("order", search_params["order"])
    page_no = int(request.args.get("page_no", search_params["page_no"]))
    page_size = int(request.args.get("page_size", search_params["page_size"]))
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

    return {
        "users": [user_schema(x) for x in users],
        "order_by": list(order_by.keys()),
        "status": ['anonymous', 'signedup', 'active'],
        "total_page": ceil(total_page / page_size),
        "search_params": search_params
    }, 200


@bp.get("/users/admin")
@session(True)
def many_admin(cur, user):
    if "user.edit_access" not in user["access"]:
        return {
            "error": "unauthorized access"
        }, 403

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

    search_params = {
        "entity_type": "all",
        "action": "all",
        "search": "",
        "order": "latest",
        "page_no": 1,
        "page_size": 24
    }
    entity_type = request.args.get("entity_type", search_params["entity_type"])
    action = request.args.get("action", search_params["action"])
    search = request.args.get("search", search_params["search"]).strip()
    order = request.args.get("order", search_params["order"])
    page_no = int(request.args.get("page_no", search_params["page_no"]))
    page_size = int(request.args.get("page_size", search_params["page_size"]))
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
        entity_type, f"%{entity_type}.%",
        action, f"%{entity_type}.{action}%",
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

    return {
        "users": [user_schema(x) for x in users],
        "access": access,
        "order_by": list(order_by.keys()),
        "total_page": ceil(users[0]["_count"] / page_size) if users else 0,
        "search_params": search_params
    }, 200
