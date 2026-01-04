from flask import Blueprint, jsonify
import os
import psycopg2
import psycopg2.extras
from psycopg2.extras import Json


bp = Blueprint("postgres", __name__)


def db_open():
    con = psycopg2.connect(os.environ["DATABASE_URI"])
    cur = con.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    return con, cur


def db_close(con, cur):
    con.commit()
    cur.close()
    con.close()


def create_tables():
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


def copy_db():
    def copy_table(from_cur, to_cur, table_name):
        from_cur.execute(f"""SELECT * FROM "{table_name}";""")
        data = from_cur.fetchall()

        print("########################")
        print(table_name, len(data))

        if not data:
            return

        columns = list(data[0].keys())

        values_list = []
        for row in data:
            values = []
            for column in columns:
                if type(row[column]) is dict:
                    row[column] = Json(row[column])
                values.append(row[column])
            values_list.append(tuple(values))

        to_cur.executemany(f"""
            INSERT INTO "{table_name}"({', '.join(columns)})
            VALUES ({', '.join(['%s'] * len(columns))});
        """, values_list)

    from_con = psycopg2.connect(os.environ["LOCAL_DB"])
    from_cur = from_con.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    to_con = psycopg2.connect(os.environ["ONLINE_DB"])
    to_cur = to_con.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    copy_table(from_cur, to_cur, "app")
    copy_table(from_cur, to_cur, "user")
    copy_table(from_cur, to_cur, "post")
    copy_table(from_cur, to_cur, "comment")
    copy_table(from_cur, to_cur, "report")
    copy_table(from_cur, to_cur, "block")
    copy_table(from_cur, to_cur, "like")
    copy_table(from_cur, to_cur, "code")
    copy_table(from_cur, to_cur, "log")
    copy_table(from_cur, to_cur, "session")

    from_con.commit()
    from_cur.close()
    from_con.close()
    to_con.commit()
    to_cur.close()
    to_con.close()

    return jsonify({
        "status": 200
    })
