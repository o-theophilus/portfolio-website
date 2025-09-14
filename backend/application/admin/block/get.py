from flask import Blueprint, jsonify, request
from math import ceil
from ...tools import get_session
from ...postgres import db_close, db_open

bp = Blueprint("block_get", __name__)


@bp.get("/blocks")
def get_many():
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    if "block:view" not in user["access"]:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "unauthorized access"
        })

    search = request.args.get("search", "")
    order = request.args.get("order", "latest")
    page_no = int(request.args.get("page_no", 1))
    page_size = int(request.args.get("page_size", 24))

    order_by = {
        'latest': 'date_created',
        'oldest': 'date_created'
    }
    order_dir = {
        'latest': 'DESC',
        'oldest': 'ASC'
    }

    cur.execute("""
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
        ORDER BY {} {}
        LIMIT %s OFFSET %s;
    """.format(order_by[order], order_dir[order]),
        (
        search, f"%{search}%",
        page_size, (page_no - 1) * page_size
    ))
    items = cur.fetchall()

    for x in items:
        x["admin"]["photo"] = (
            f"{request.host_url}file/{x['admin']['photo']}"
            if x["admin"]["photo"] else None
        )
        x["user"]["photo"] = (
            f"{request.host_url}file/{x['user']['photo']}"
            if x["user"]["photo"] else None
        )

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "items": items,
        "order_by": list(order_by.keys()),
        "total_page": ceil(
            items[0]["_count"] / page_size) if items else 0
    })


@bp.get("/blocked/<key>")
def ckeck(key):
    con, cur = db_open()

    cur.execute("SELECT * FROM block WHERE user_key = %s;", (key,))
    blocked = cur.fetchone()

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "blocked":  True if blocked else False
    })
