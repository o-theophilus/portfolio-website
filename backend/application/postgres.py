from flask import Blueprint, jsonify
import os
import psycopg2
import psycopg2.extras
from werkzeug.security import generate_password_hash
from .tools import access_pass


bp = Blueprint("postgres", __name__)


def db_open():
    con = psycopg2.connect(os.environ["DATABASE_URI"])
    cur = con.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    return con, cur


def db_close(con, cur):
    con.commit()
    cur.close()
    con.close()


# @bp.get("/fix")
def create_tables():
    # con = psycopg2.connect(os.environ["ONLINE_DB"])
    # cur = con.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    con, cur = db_open()

    cur.execute('CREATE EXTENSION IF NOT EXISTS "pgcrypto";')
    cur.execute("""
        DROP TABLE IF EXISTS app CASCADE;
        DROP TABLE IF EXISTS "user" CASCADE;
        DROP TABLE IF EXISTS post CASCADE;
        DROP TABLE IF EXISTS comment CASCADE;
        DROP TABLE IF EXISTS report CASCADE;
        DROP TABLE IF EXISTS block CASCADE;
        DROP TABLE IF EXISTS "like" CASCADE;
        DROP TABLE IF EXISTS code CASCADE;
        DROP TABLE IF EXISTS log CASCADE;
        DROP TABLE IF EXISTS session CASCADE;

        CREATE TABLE IF NOT EXISTS app (
            key UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            alias TEXT UNIQUE NOT NULL,
            value JSONB DEFAULT '{}'::jsonb
        );

        CREATE TABLE IF NOT EXISTS "user" (
            key UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            status TEXT NOT NULL DEFAULT 'anonymous',
            date_created TIMESTAMPTZ DEFAULT now(),
            name TEXT NOT NULL,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            phone TEXT,
            photo TEXT,
            access TEXT[] DEFAULT '{}'::TEXT[],
            theme TEXT NOT NULL DEFAULT 'dark'
        );

        CREATE TABLE IF NOT EXISTS post (
            key UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            status TEXT NOT NULL DEFAULT 'draft',
            date_created TIMESTAMPTZ DEFAULT now(),
            author_key UUID NOT NULL REFERENCES "user"(key),
            title TEXT NOT NULL,
            slug TEXT UNIQUE NOT NULL,
            content TEXT,
            description TEXT,
            photo TEXT,
            files TEXT[] DEFAULT '{}'::TEXT[],
            tags TEXT[] DEFAULT '{}'::TEXT[]
        );

        CREATE TABLE IF NOT EXISTS comment (
            key UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            date_created TIMESTAMPTZ DEFAULT now(),
            user_key UUID NOT NULL REFERENCES "user"(key) ON DELETE CASCADE,
            post_key UUID NOT NULL REFERENCES post(key) ON DELETE CASCADE,
            parent_key UUID REFERENCES comment(key) ON DELETE CASCADE,
            comment TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS report (
            key UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            date_created TIMESTAMPTZ DEFAULT now(),
            user_key UUID NOT NULL REFERENCES "user"(key) ON DELETE CASCADE,
            entity_key UUID NOT NULL,
            entity_type TEXT NOT NULL,
            comment TEXT NOT NULL,
            tags TEXT[] DEFAULT '{}'::TEXT[]
        );

        CREATE TABLE IF NOT EXISTS block (
            key UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            date_created TIMESTAMPTZ DEFAULT now(),
            admin_key UUID NOT NULL REFERENCES "user"(key) ON DELETE CASCADE,
            user_key UUID NOT NULL REFERENCES "user"(key) ON DELETE CASCADE,
            comment TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS "like" (
            key UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            date_created TIMESTAMPTZ DEFAULT now(),
            user_key UUID NOT NULL REFERENCES "user"(key) ON DELETE CASCADE,
            entity_type TEXT NOT NULL,
            entity_key UUID NOT NULL,
            reaction TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS code (
            key UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            date_created TIMESTAMPTZ DEFAULT now(),
            user_key UUID NOT NULL REFERENCES "user"(key) ON DELETE CASCADE,
            pin TEXT NOT NULL,
            email TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS log (
            key UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            date_created TIMESTAMPTZ DEFAULT now(),
            user_key UUID NOT NULL,
            action TEXT NOT NULL,
            entity_key TEXT NOT NULL,
            entity_type TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT '200',
            misc JSONB DEFAULT '{}'::jsonb
        );

        CREATE TABLE IF NOT EXISTS session (
            key UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            date_created TIMESTAMPTZ DEFAULT now(),
            date_updated TIMESTAMPTZ DEFAULT now(),
            user_key UUID NOT NULL REFERENCES "user"(key) ON DELETE CASCADE,
            login TEXT NOT NULL DEFAULT 'false',
            remember BOOL NOT NULL DEFAULT FALSE
        );
    """)

    db_close(con, cur)
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
