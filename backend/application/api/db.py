from flask import Blueprint, jsonify
import os
import psycopg2
from werkzeug.security import generate_password_hash
from ..postgres import create_tables_query
from ..admin.access import access_pass

bp = Blueprint("api_db", __name__)


def create_tables():
    con = psycopg2.connect(os.environ["ONLINE_DB"])
    cur = con.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    tables = ['app', '"user"', 'post', 'comment', 'report',
              'block', '"like"', 'code', 'log', 'session']
    tables = [f"DROP TABLE IF EXISTS {x} CASCADE;" for x in tables]
    query = "\n".join(tables) + "\n\n" + create_tables_query()

    cur.execute('CREATE EXTENSION IF NOT EXISTS "pgcrypto";')
    cur.execute(query)

    con.commit()
    cur.close()
    con.close()
    return jsonify({
        "status": 200
    })


def copy_post_table():
    con = psycopg2.connect(os.environ["LOCAL_DB"])
    cur = con.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    cur.execute("SELECT * FROM post;")
    data = cur.fetchall()
    con.commit()
    cur.close()
    con.close()

    con = psycopg2.connect(os.environ["ONLINE_DB"])
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
        [f"{x}:{y[0]}" for x in access_pass for y in access_pass[x]]
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
                tags
            )
            VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """, (
            x["key"],
            x["status"],
            x["date_created"],
            user["key"],
            x["title"],
            x["slug"],
            x["content"],
            x["description"],
            x["photo"],
            x["files"],
            x["tags"]
        ))

    con.commit()
    cur.close()
    con.close()

    return jsonify({
        "status": 200
    })
