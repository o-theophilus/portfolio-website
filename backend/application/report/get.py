from math import ceil

from flask import Blueprint, jsonify, request

from ..postgres import db_close, db_open
from ..tools import get_session

bp = Blueprint("report_get", __name__)


@bp.get("/reports")
def get_many():
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    user = session["user"]

    if "report:view" not in user["access"]:
        db_close(con, cur)
        return jsonify({
            "status": 400,
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
        "status": "active",
        "type": "all",
        "order": "latest",
        "page_no": 1,
        "page_size": 24
    }
    search = request.args.get("search", searchParams["search"]).strip()
    _type = request.args.get("type", searchParams["type"])
    status = request.args.get("status", searchParams["status"])
    order = request.args.get("order", searchParams["order"])
    page_no = int(request.args.get("page_no", searchParams["page_no"]))
    page_size = int(request.args.get("page_size", searchParams["page_size"]))
    page_size = min(page_size, 100)

    cur.execute(f"""
        SELECT
            report.key,
            report.date_created,
            report.comment,
            report.tags,
            report.reported_key,
            report.comment_key,

            jsonb_build_object(
                'name', "user".name,
                'username', "user".username,
                'photo', "user".photo
            ) AS "user"

        FROM report
        LEFT JOIN "user" ON report.reporter_key = "user".key

        WHERE
            report.status = %s
            AND (
                %s = 'all'
                OR (%s = 'user' AND report.reported_key IS NOT NULL)
                OR (%s = 'comment' AND report.comment_key IS NOT NULL)
            )
            AND (%s = '' OR CONCAT_WS(', ',
                report.key, report.comment, report.tags,
                report.reporter_key, report.reported_key,
                report.comment_key
            ) ILIKE %s)
        ORDER BY {order_by[order]} {order_dir[order]}, report.key DESC
        LIMIT %s OFFSET %s;
    """, (
        status,
        _type, _type, _type,
        search, f"%{search}%",
        page_size, (page_no - 1) * page_size
    ))
    reports = cur.fetchall()
    user_keys = []
    comment_keys = []

    for x in reports:
        if x["reported_user_key"] and x["reported_user_key"] not in user_keys:
            user_keys.append(x["reported_user_key"])
        if x["comment_key"] and x["comment_key"] not in comment_keys:
            comment_keys.append(x["comment_key"])

    if user_keys:
        cur.execute("""
            SELECT key, name, username, photo
            FROM "user" WHERE key = ANY(%s);
        """, (user_keys,))
        users = {x["key"]: x for x in cur.fetchall()}
        for x in reports:
            if x["reported_user_key"]:
                x["reported_user"] = users.get(x["reported_user_key"])

    if comment_keys:
        cur.execute("""
            SELECT
                comment.key, comment.comment, comment.date_created,
                comment.post_key,
                jsonb_build_object(
                    'name', "user".name,
                    'username', "user".username,
                    'photo', "user".photo
                ) AS "user"
            FROM comment
            JOIN "user" ON comment.user_key = "user".key
            WHERE comment.key = ANY(%s);
        """, (comment_keys,))
        comments = {x["key"]: x for x in cur.fetchall()}
        for x in reports:
            if x["comment_key"]:
                x["reported_comment"] = comments.get(x["comment_key"])

    for x in reports:
        x["user"]["photo"] = (
            f"{request.host_url}photo/user/{x['user']['photo']}"
            if x["user"]["photo"] else None
        )
        if x.get("reported_user"):
            x["reported_user"]["photo"] = (
                f"{request.host_url}photo/user/{x['reported_user']['photo']}"
                if x["reported_user"]["photo"] else None
            )
        if x.get("reported_comment"):
            x["reported_comment"]["user"]["photo"] = (
                f"{request.host_url}photo/user/{x['reported_comment']['user'][
                    'photo']}"
                if x["reported_comment"]["user"]["photo"] else None
            )

    cur.execute("""
        SELECT COUNT(*) FROM report
        WHERE
            report.status = %s
            AND (
                %s = 'all'
                OR (%s = 'user' AND report.reported_key IS NOT NULL)
                OR (%s = 'comment' AND report.comment_key IS NOT NULL)
            )
            AND (%s = '' OR CONCAT_WS(', ',
                report.key, report.comment, report.tags,
                report.reporter_key, report.reported_key, report.comment_key
            ) ILIKE %s);
    """, (
        status,
        _type, _type, _type,
        search, f"%{search}%",
    ))
    total_page = cur.fetchone()["count"]

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "reports": reports,
        "order_by": list(order_by.keys()),
        "_status": ["active", "resolved", "dismissed"],
        "type": ["all", "user", "comment"],
        "total_page": ceil(total_page / page_size),
        "searchParams": searchParams
    })
