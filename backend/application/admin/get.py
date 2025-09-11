from flask import Blueprint, request, jsonify
from math import ceil
from ..tools import get_session, user_schema
from ..postgres import db_close, db_open
from ..admin.access import access_pass


bp = Blueprint("admin_get", __name__)


@bp.get("/admin/user")
def get_admins():
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    if "user:set_access" not in user["access"]:
        db_close(con, cur)
        return jsonify({
            "status": 400,
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

    entity_type = request.args.get("entity_type", "all")
    action = request.args.get("action", "all")
    search = request.args.get("search", "").strip()
    order = request.args.get("order", "latest")
    page_no = int(request.args.get("page_no", 1))
    page_size = int(request.args.get("size", 24))

    cur.execute("""
        SELECT *, COUNT(*) OVER() AS _count
        FROM "user"
        WHERE
            array_length(access, 1) IS NOT NULL
            -- AND status = "confirmed"
            AND (%s = ''
                OR CONCAT_WS(', ', key, name, email)
                ILIKE %s)
            AND (%s = 'all' OR ARRAY_TO_STRING(access, ',')
                ILIKE %s)
            AND (%s = 'all' OR ARRAY_TO_STRING(access, ',')
                ILIKE %s)
        ORDER BY {} {}
        LIMIT %s OFFSET %s;
    """.format(
        order_by[order], order_dir[order]
    ), (
        search, f"%{search}%",
        entity_type, f"%{entity_type}:%",
        action, f"%{entity_type}:{action}%",
        page_size, (page_no - 1) * page_size
    ))
    items = cur.fetchall()

    _access = {
        "all": ['all']
    }
    for x in access_pass:
        if x not in _access:
            _access[x] = ["all"]
            for y in access_pass[x]:
                _access[x].append(y[0])

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "items": [user_schema(x) for x in items],
        "search_query": _access,
        "order_by": list(order_by.keys()),
        "total_page": ceil(items[0]["_count"] / page_size) if items else 0
    })
