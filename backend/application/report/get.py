from flask import Blueprint, jsonify, request
from math import ceil
from ..tools import get_session
from ..postgres import db_close, db_open

bp = Blueprint("report_get", __name__)


@bp.get("/reports")
def get_reports():
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

    search = request.args.get("search", "")
    _type = request.args.get("type", "")
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
            report.key,
            report.date_created,
            report.comment,
            report.tags,
            report.entity_type,
            report.entity_key,

            jsonb_build_object(
                'name', "user".name,
                'username', "user".username,
                'photo', "user".photo
            ) AS "user",

            jsonb_build_object(
                'comment', comment.comment,
                'post_key', comment.post_key
            ) AS comment,
            jsonb_build_object(
                'name', usr.name,
                'username', usr.username,
                'photo', usr.photo
            ) AS reported_user,

            COUNT(*) OVER() AS _count

        FROM report
        LEFT JOIN "user" ON report.user_key = "user".key
        LEFT JOIN comment ON report.entity_key = comment.key
            AND report.entity_type = 'comment'
        LEFT JOIN "user" usr ON report.entity_key = usr.key
            AND report.entity_type = 'user'

        WHERE
            (%s = '' OR CONCAT_WS(', ',
                report.key, report.comment, report.tags,
                "user".key, "user".name, "user".email,
                report.entity_key, comment.comment
            ) ILIKE %s)
            AND (%s = '' OR report.entity_type = %s)
        ORDER BY {} {}
        LIMIT %s OFFSET %s;
    """.format(order_by[order], order_dir[order]),
        (
        search, f"%{search}%",
        _type, _type,
        page_size, (page_no - 1) * page_size
    ))

    # TODO: include user as json if entity_type != "user"
    reports = cur.fetchall()
    # for x in reports:
    #     x["reported"]["photo"] = (
    #         f"{request.host_url}file/{x['reported']['photo']}"
    #         if x["reported"]["photo"] else None
    #     )

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "reports": reports,
        "order_by": list(order_by.keys()),
        "_type": ["user", "comment"],
        "_status": ["unresolved", "resolved"],
        "total_page": ceil(reports[0]["_count"] / page_size
                           ) if reports else 0
    })
