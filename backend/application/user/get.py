from flask import Blueprint, request, jsonify
from math import ceil
from ..tools import get_session, user_schema
from ..postgres import db_close, db_open
from ..admin.access import access_pass


bp = Blueprint("user_get", __name__)


@bp.get("/user/<key>")
def get(key):
    con, cur = db_open()

    session = get_session(cur)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)

    cur.execute("""
        SELECT * FROM "user" WHERE key::TEXT = %s OR username = %s;
    """, (key, key))
    item = cur.fetchone()

    if not item:
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
        "item": user_schema(item),
        "access": _access
    })


@bp.get("/users")
def get_many():
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)

    if "user:view" not in session["user"]["access"]:
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

    status = request.args.get("status", "confirmed")
    search = request.args.get("search", "").strip()
    order = request.args.get("order", "latest")
    page_no = int(request.args.get("page_no", 1))
    page_size = int(request.args.get("size", 24))

    cur.execute("""
        SELECT *, COUNT(*) OVER() AS _count
        FROM "user"
        WHERE (
                %s = 'all' OR status = %s
            ) AND (
                %s = ''
                OR CONCAT_WS(', ', key, name, email
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
    items = cur.fetchall()

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "items": [user_schema(x) for x in items],
        "order_by": list(order_by.keys()),
        "_status": ['anonymous', 'signedup', 'confirmed'],
        "total_page": ceil(items[0]["_count"] / page_size) if items else 0
    })
