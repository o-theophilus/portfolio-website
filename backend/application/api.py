from flask import Blueprint, jsonify, request
import re
import os
from .tools import send_mail
from .postgres import db_open, db_close, create_tables_query
from .admin import access
import psycopg2
from psycopg2.extras import Json
from werkzeug.security import generate_password_hash

bp = Blueprint("api", __name__)


@bp.post("/contact")
def send_email():

    if (
        "email_template" not in request.json
        or not request.json["email_template"]
    ):
        return jsonify({
            "status": 400,
            "error": "Invalid request"
        })

    error = {}

    if "name" not in request.json or not request.json["name"]:
        error["name"] = "This field is required"
    if "email" not in request.json or not request.json["email"]:
        error["email"] = "This field is required"
    elif not re.match(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", request.json["email"]):
        error["email"] = "Invalid email address"
    if "message" not in request.json or not request.json["message"]:
        error["message"] = "This field is required"

    if error != {}:
        return jsonify({
            "status": 400,
            **error
        })

    message = request.json['email_template'].format(
        name=request.json["name"],
        email=request.json["email"],
        message=request.json["message"])

    send_mail(
        os.environ["MAIL_USERNAME"],
        f"{request.json['name']} from Theophilus Portfolio Website",
        message
    )

    return jsonify({
        "status": 200
    })


@bp.get("/cron")
def cron():
    con, cur = db_open()
    print("cron is running")

    cur.execute("""
        DELETE FROM session
        WHERE (
                stay_loggedin = FALSE
                AND updated_at <= NOW() - INTERVAL '1 day'
            ) OR (
                stay_loggedin = TRUE
                AND updated_at <= NOW() - INTERVAL '3 days'
            );
    """)

    db_close(con, cur)
    return jsonify({
        "status": 200
    })


def create_tables():
    con, cur = db_open()

    tables = ['setting', '"user"', 'post', 'comment',
              'report', 'code', 'log', 'session']
    tables = [f"DROP TABLE IF EXISTS {x} CASCADE;" for x in tables]
    query = "\n".join(tables) + "\n\n" + create_tables_query()

    cur.execute('CREATE EXTENSION IF NOT EXISTS "pgcrypto";')
    cur.execute(query)

    db_close(con, cur)
    return jsonify({
        "status": 200
    })


def copy_post_table():
    con = psycopg2.connect(os.environ["ONLINE_DB"])
    cur = con.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cur.execute("SELECT * FROM post;")
    data = cur.fetchall()
    con.commit()
    cur.close()
    con.close()

    con = psycopg2.connect(os.environ["LOCAL_DB"])
    cur = con.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cur.execute("""
            INSERT INTO "user"
            (status, name, username, email, password, access)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING *;
        """, (
        "confirmed",
        "Theophilus",
        "theophilus",
        os.environ["MAIL_USERNAME"],
        generate_password_hash(
            os.environ["MAIL_PASSWORD"], method="scrypt"),
        [f"{x}:{y[0]}" for x in access for y in access[x]]
    ))
    user = cur.fetchone()

    for x in data:
        cur.execute("""
            INSERT INTO post(
                key,
                status,
                date_created,
                author_key,
                title,
                slug,
                content,
                description,
                photo,
                files,
                tags,
                likes,
                dislikes,
                ratings
            )
            VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """, (
            x["key"],
            x["status"],
            x["date"],
            user["key"],
            x["title"],
            x["slug"],
            x["content"],
            x["description"],
            x["photo"],
            x["files"],
            x["tags"],
            x["like"],
            x["dislike"],
            Json(x["ratings"]),
        ))

    con.commit()
    cur.close()
    con.close()

    return jsonify({
        "status": 200
    })


def fix_access():
    con, cur = db_open()

    cur.execute("""
            UPDATE "user" SET access=% s WHERE email = % s;
        """, (
        [f"{x}:{y[0]}" for x in access for y in access[x]],
        os.environ["MAIL_USERNAME"]
    ))

    db_close(con, cur)
    return jsonify({
        "status": 200
    })


# @bp.get("/fix")
def quick_fix():
    con, cur = db_open()

    cur.execute("""
        ALTER TABLE setting ADD COLUMN alias TEXT UNIQUE NOT NULL;
    """)

    db_close(con, cur)
    return jsonify({
        "status": 200
    })


def general_fix():
    con, cur = db_open()

    # cur.execute(f"""
    #     DROP TABLE IF EXISTS session CASCADE;
    #     {session_table}
    # """)

    # cur.execute("""
    #     ALTER TABLE report DROP COLUMN reported_key;
    #     ALTER TABLE "user" DROP COLUMN login;
    # """)

    # cur.execute("""
    #     ALTER TABLE log
    #     DROP CONSTRAINT log_user_key_fkey;
    # """)

    # cur.execute("""
    #     ALTER TABLE report RENAME COLUMN reporter_key TO user_key;
    #     ALTER TABLE post RENAME COLUMN "like" TO likes;
    #     ALTER TABLE post RENAME COLUMN dislike TO dislikes;
    #     ALTER TABLE comment RENAME COLUMN "like" TO likes;
    #     ALTER TABLE comment RENAME COLUMN dislike TO dislikes;
    # """)

    ##########################
    # cur.execute(
    #     "ALTER TABLE post ADD COLUMN ratings_new jsonb DEFAULT '[]'::jsonb;")
    # cur.execute("""
    #     UPDATE post
    #     SET ratings_new = COALESCE(
    #         (SELECT jsonb_agg(elem) FROM unnest(ratings) AS elem),
    #         '[]'::jsonb
    #     );
    # """)
    # cur.execute("ALTER TABLE post DROP COLUMN ratings;")
    # cur.execute("ALTER TABLE post RENAME COLUMN ratings_new TO ratings;")

    ##########################
    # cur.execute("ALTER TABLE comment ADD COLUMN parent_key TEXT;")
    # cur.execute(
    #     "UPDATE comment SET
    #       parent_key = path[array_length(path, 1)];")
    # cur.execute("ALTER TABLE comment DROP COLUMN path;")

    ##########################
    # cur.execute("""
    #     ALTER TABLE comment ADD COLUMN created_at TIMESTAMPTZ;
    # """)
    # cur.execute("""
    #     UPDATE comment SET created_at = now() WHERE created_at IS NULL;
    # """)
    # cur.execute("""
    #     ALTER TABLE comment ALTER COLUMN created_at SET NOT NULL;
    # """)

    db_close(con, cur)
    return jsonify({
        "status": 200
    })
