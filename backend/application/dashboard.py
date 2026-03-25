from flask import Blueprint, jsonify, request

from .postgres import db_close, db_open
from .tools import get_session

bp = Blueprint("dashboard", __name__)


def new_users(cur, interval):
    cur.execute(f"""
        WITH revenue AS (
            SELECT
                SUM(
                    CASE
                        WHEN log.date_created
                            >= NOW() - INTERVAL '{interval}'
                        THEN 1
                    END
                ) AS value,

                SUM(
                    CASE
                        WHEN log.date_created
                            >= NOW() - INTERVAL '{interval}' * 2
                        AND log.date_created
                            < NOW() - INTERVAL '{interval}'
                        THEN 1
                    END
                ) AS prev_value
            FROM log
            WHERE log.entity_type = 'user'
            AND log.action = 'signedup'
        )

        SELECT
            COALESCE(value, 0) AS value,

            CASE
                WHEN prev_value = 0 AND value > 0 THEN 100
                WHEN prev_value = 0 AND value = 0 THEN 0
                ELSE ROUND(((value - prev_value) * 100.0) / prev_value, 0)
            END AS change

        FROM revenue;
    """)
    return cur.fetchone()


def top_users(cur):
    cur.execute("""
        SELECT
            u.key,
            u.username,
            u.name,
            COUNT(o.key) AS orders,
            SUM(o.order_cost + o.delivery_cost) AS spent
        FROM "order" o
        LEFT JOIN "user" u ON o.user_key = u.key
        WHERE o.status NOT IN ('cart','canceled','returned')
        GROUP BY u.key, u.username, u.name
        ORDER BY spent DESC
        LIMIT 5;
    """)
    return cur.fetchall()


def sales_chart(cur, interval):
    cur.execute(f"""
        SELECT
            date_trunc(
                CASE
                    WHEN '{interval}' IN ('24 hours','today') THEN 'hour'
                    WHEN '{interval}' = '7days' THEN 'day'
                    ELSE 'month'
                END,
                (o.timeline->>'created')::timestamp
            ) AS period,

            SUM(o.order_cost + o.delivery_cost) AS value

        FROM "order" o
        WHERE o.status NOT IN ('cart','canceled','returned')
        AND (o.timeline->>'created')::timestamp
            >= NOW() - INTERVAL '{interval}'

        GROUP BY period
        ORDER BY period;
    """)

    rows = cur.fetchall()
    print(rows)

    return [
        {
            "label": r["period"].strftime("%b") if interval == "1 month"
            else r["period"].strftime("%d %b")
            if interval == "7 days"
            else r["period"].strftime("%H:%M"),
            "value": r["value"]
        }
        for r in rows
    ]


def order_count(cur, interval):
    cur.execute(f"""
        WITH revenue AS (
            SELECT
                SUM(
                    CASE
                        WHEN (o.timeline->>'created')::timestamp
                            >= NOW() - INTERVAL '{interval}'
                        THEN 1
                    END
                ) AS value,

                SUM(
                    CASE
                        WHEN (o.timeline->>'created')::timestamp
                            >= NOW() - INTERVAL '{interval}' * 2
                        AND (o.timeline->>'created')::timestamp
                            < NOW() - INTERVAL '{interval}'
                        THEN 1
                    END
                ) AS prev_value
            FROM "order" o
            WHERE o.status NOT IN ('cart')
        )

        SELECT
            COALESCE(value, 0) AS value,

            CASE
                WHEN prev_value = 0 AND value > 0 THEN 100
                WHEN prev_value = 0 AND value = 0 THEN 0
                ELSE ROUND(((value - prev_value) * 100.0) / prev_value, 0)
            END AS change

        FROM revenue;
    """)
    return cur.fetchone()


def order_revenue(cur, interval):
    cur.execute(f"""
        WITH revenue AS (
            SELECT
                SUM(
                    CASE
                        WHEN (o.timeline->>'created')::timestamp
                            >= NOW() - INTERVAL '{interval}'
                        THEN o.order_cost + o.delivery_cost
                        ELSE 0
                    END
                ) AS value,

                SUM(
                    CASE
                        WHEN (o.timeline->>'created')::timestamp
                            >= NOW() - INTERVAL '{interval}' * 2
                        AND (o.timeline->>'created')::timestamp
                            < NOW() - INTERVAL '{interval}'
                        THEN o.order_cost + o.delivery_cost
                        ELSE 0
                    END
                ) AS prev_value
            FROM "order" o
            WHERE o.status NOT IN ('cart', 'canceled', 'returned')
        )

        SELECT
            COALESCE(value, 0) AS value,

            CASE
                WHEN prev_value = 0 AND value > 0 THEN 100
                WHEN prev_value = 0 AND value = 0 THEN 0
                ELSE ROUND(((value - prev_value) * 100.0) / prev_value, 0)
            END AS change

        FROM revenue;
    """)
    return cur.fetchone()


def order_recent(cur):
    cur.execute("""
        SELECT
            o.key,
            o.status,
            o.order_cost + o.delivery_cost AS total,
            u.username,
            u.name
        FROM "order" o
        LEFT JOIN "user" u ON o.user_key = u.key
        WHERE o.status != 'cart'
        ORDER BY (o.timeline->>'created')::timestamp DESC
        LIMIT 5;
    """)
    return cur.fetchall()


def post_summary(cur):
    item_status = ['active', 'draft']

    cur.execute("""
        SELECT s.status AS label, COUNT(post.*) AS count
        FROM unnest(%s::text[]) AS s(status)
        LEFT JOIN post ON post.status = s.status
        GROUP BY s.status
        ORDER BY array_position(%s, s.status);
    """, (item_status, item_status))
    return cur.fetchall()


def item_available(cur):
    cur.execute("""
        SELECT COUNT(*) AS value
        FROM item
        WHERE status = 'active';
    """)
    return cur.fetchone()


def item_low_quantity(cur):
    cur.execute("""
        SELECT name, slug, quantity
        FROM item
        WHERE quantity < 10
        ORDER BY quantity ASC
        LIMIT 5;
    """)
    return cur.fetchall()


def item_top_purchase(cur, interval):
    cur.execute(f"""
        SELECT
            i.name,
            i.slug,
            SUM(oi.quantity) AS units,
            SUM(oi.quantity * i.price) AS total
        FROM order_item oi
        JOIN "order" o ON o.key = oi.order_key
        JOIN item_version i
            ON i.key = oi.item_key
        WHERE o.status NOT IN ('cart', 'canceled', 'returned')
        AND (o.timeline->>'created')::timestamp
            >= NOW() - INTERVAL '{interval}'
        GROUP BY i.item_key, i.name, i.slug
        ORDER BY units DESC
        LIMIT 10;
    """)
    return cur.fetchall()
    # TODO: JOIN item_version


@bp.get("/dashboard")
def dashboard():
    con, cur = db_open()

    session = get_session(cur, True)
    if session["status"] != 200:
        db_close(con, cur)
        return jsonify(session)
    # user = session["user"]

    intervals = {
        "today": "1 day",
        "24 hours": "24 hours",
        "7 days": "7 days",
        "1 month": "1 month",
    }

    searchParams = {
        "interval": "24 hours",
    }

    interval = request.args.get("interval", searchParams["interval"])

    _new_users = new_users(cur, intervals[interval])
    _post_summary = post_summary(cur)
    # _top_users = top_users(cur)
    # _item_available = item_available(cur)

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "new_users": _new_users,
        "post_summary": _post_summary,
        # "top_users": _top_users,
        # "item_available": _item_available,
        "searchParams": searchParams,
        "filters": list(intervals.keys()),
    })
