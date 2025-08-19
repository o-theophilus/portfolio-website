from flask import Blueprint, jsonify, request
from .tools import token_to_user
from uuid import uuid4
from .postgres import db_close, db_open
from .log import log
from math import ceil

bp = Blueprint("report", __name__)


@bp.get("/reports")
def get_reports():
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    if "report:view" not in user["access"]:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "unauthorized access"
        })

    page_no = 1
    page_size = 4
    order = "latest"
    search = ""
    _type = ""
    _status = "unresolved"

    if "page_no" in request.args:
        page_no = int(request.args["page_no"])
    if "page_size" in request.args:
        page_size = int(request.args["page_size"])
    if "order" in request.args:
        order = request.args["order"]
    if "search" in request.args:
        search = request.args["search"]
    if "type" in request.args:
        _type = request.args["type"]
    if "status" in request.args:
        _status = request.args["status"]

    order_by = {
        'latest': 'log.date',
        'oldest': 'log.date'
    }

    order_dir = {
        'latest': 'DESC',
        'oldest': 'ASC'
    }

    cur.execute("""
        SELECT
            report.key,
            report.status,
            report.report,
            report.resolve,
            report.tags,
            log.date,

            jsonb_build_object(
                'key', reporter.key,
                'name', reporter.name
            ) AS reporter,

            jsonb_build_object(
                'key', reported.key,
                'name', reported.name,
                'photo', reported.photo
            ) AS reported,

            jsonb_build_object(
                'type', report.entity_type,
                'key', report.entity_key,
                'extra_1', COALESCE(comment.comment, NULL),
                'extra_2', COALESCE(comment.post_key, NULL)
            ) AS entity,

            COUNT(*) OVER() AS _count

        FROM report
        LEFT JOIN
            "user" reporter ON report.reporter_key = reporter.key
        LEFT JOIN
            "user" reported ON report.reported_key = reported.key
        LEFT JOIN
            comment ON report.entity_key = comment.key
            AND report.entity_type = 'comment'
        LEFT JOIN
            log ON report.key = log.entity_key
            AND log.entity_type = 'report'
            AND log.action = 'created'

        WHERE
            (%s = '' OR CONCAT_WS(', ',
                report.key, report.report, report.tags,
                reporter.key, reporter.name, reporter.email,
                reported.key, reported.name, reported.email,
                report.entity_key, comment.comment
            ) ILIKE %s)
            AND (%s = '' OR report.entity_type = %s)
            AND (%s = '' OR report.status = %s)
        ORDER BY {} {}
        LIMIT %s OFFSET %s;
    """.format(order_by[order], order_dir[order]),
        (
        search, f"%{search}%",
        _type, _type,
        _status, _status,
        page_size, (page_no - 1) * page_size
    ))
    reports = cur.fetchall()
    for x in reports:
        x["reported"]["photo"] = (
            f"{request.host_url}file/{x['reported']['photo']}"
            if x["reported"]["photo"] else None
        )

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


@bp.post("/report")
def create():
    con, cur = db_open()

    user = token_to_user(cur)
    if not user or not user["login"]:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    if (
        "entity_key" not in request.json
        or not request.json["entity_key"]
        or "entity_type" not in request.json
        or not request.json["entity_type"]
        or request.json["entity_type"] not in ["user", "comment"]
        or "tags" not in request.json
        or type(request.json["tags"]) is not list
    ):
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    if "report" not in request.json or not request.json["report"]:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "report": "cannot be empty"
        })

    cur.execute(f"""
        SELECT * FROM "{request.json['entity_type']}" WHERE key = %s;
    """, (request.json["entity_key"],))
    entity = cur.fetchone()
    if not entity:
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    cur.execute("""
        INSERT INTO report (key, reporter_key, reported_key,
            entity_key, entity_type, report, tags)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        RETURNING *;
    """, (
        uuid4().hex,
        user["key"],
        entity["user_key"],
        entity["key"],
        request.json["entity_type"],
        request.json["report"],
        request.json["tags"]
    ))
    report = cur.fetchone()

    log(
        cur=cur,
        user_key=user["key"],
        action="created",
        entity_key=report["key"],
        entity_type="report",
        misc={
            "entity_key":  request.json["entity_key"],
            "entity_type":  request.json["entity_type"],
        }
    )

    db_close(con, cur)
    return jsonify({
        "status": 200
    })


@bp.post("/report/status/<key>")
def status(key):
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    if "report:edit_status" not in user["access"]:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "unauthorized access"
        })

    if "note" not in request.json or not request.json["note"]:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "note": "cannot be empty"
        })

    cur.execute("""
        SELECT * FROM report WHERE key = %s;
    """, (key,))
    report = cur.fetchone()
    if (
        not report
        or report["status"] == "resolved"
        or "status" not in request.json
        or not request.json["status"]
        or request.json["status"] not in ["resolved"]
    ):
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    log(
        cur=cur,
        user_key=user["key"],
        action="changed_status",
        entity_key=report["key"],
        entity_type="report",
        misc={
            "from": report["status"],
            "to":  request.json["status"]
        }
    )

    cur.execute("""
        UPDATE report
        SET
            status = %s,
            resolve = %s
        WHERE key = %s
        RETURNING *;
    """, (
        request.json["status"],
        request.json["note"],
        report["key"]
    ))

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "report": report
    })
