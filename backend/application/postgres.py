from flask import Blueprint
import os
import psycopg2
import psycopg2.extras


bp = Blueprint("postgres", __name__)

setting_table = """CREATE TABLE IF NOT EXISTS setting (
    key VARCHAR(32) PRIMARY KEY,
    misc JSONB DEFAULT '{}'::JSONB
);"""

user_table = """CREATE TABLE IF NOT EXISTS "user" (
    key CHAR(32) PRIMARY KEY,
    status VARCHAR(20) DEFAULT 'anonymous' NOT NULL,

    name VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(100),
    password VARCHAR(200) NOT NULL,
    photo VARCHAR(50),

    access TEXT[] DEFAULT ARRAY[]::TEXT[],
    login BOOLEAN DEFAULT FALSE,

    setting_theme VARCHAR(20) DEFAULT 'dark'
);"""

post_table = """CREATE TABLE IF NOT EXISTS post (
    key CHAR(32) PRIMARY KEY,
    status VARCHAR(20) DEFAULT 'draft' NOT NULL,
    date TIMESTAMP NOT NULL,
    author_key CHAR(32) NOT NULL,

    title VARCHAR(100) NOT NULL,
    slug VARCHAR(255) UNIQUE NOT NULL,
    content TEXT,
    description TEXT,
    files TEXT[] DEFAULT ARRAY[]::TEXT[],
    tags TEXT[] DEFAULT ARRAY[]::TEXT[],
    "like" TEXT[] DEFAULT ARRAY[]::TEXT[],
    dislike TEXT[] DEFAULT ARRAY[]::TEXT[],
    ratings JSONB[] DEFAULT ARRAY[]::JSONB[],

    FOREIGN KEY (author) REFERENCES "user"(key)
);"""


comment_table = """CREATE TABLE IF NOT EXISTS comment (
    key CHAR(32) PRIMARY KEY,
    status VARCHAR(20) DEFAULT 'active' NOT NULL,

    user_key CHAR(32) NOT NULL,
    post_key CHAR(32) NOT NULL,

    comment TEXT NOT NULL,
    path TEXT[] DEFAULT ARRAY[]::TEXT[],
    "like" TEXT[] DEFAULT ARRAY[]::TEXT[],
    dislike TEXT[] DEFAULT ARRAY[]::TEXT[],

    FOREIGN KEY (user_key) REFERENCES "user"(key) ON DELETE CASCADE,
    FOREIGN KEY (post_key) REFERENCES post(key)
);"""


report_table = """CREATE TABLE IF NOT EXISTS report (
    key CHAR(32) PRIMARY KEY,
    status VARCHAR(20) DEFAULT 'unresolved' NOT NULL,

    reporter_key CHAR(32) NOT NULL,
    reported_key CHAR(32) NOT NULL,
    entity_key CHAR(32),
    entity_type VARCHAR(100),

    report TEXT,
    tags TEXT[] DEFAULT ARRAY[]::TEXT[],
    resolve TEXT,

    FOREIGN KEY (reporter_key) REFERENCES "user"(key) ON DELETE CASCADE,
    FOREIGN KEY (reported_key) REFERENCES "user"(key) ON DELETE CASCADE
);"""


code_table = """CREATE TABLE IF NOT EXISTS code (
    key CHAR(32) PRIMARY KEY,

    user_key CHAR(32) NOT NULL,
    pin VARCHAR(10) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,

    FOREIGN KEY (user_key) REFERENCES "user"(key)
);"""

log_table = """CREATE TABLE IF NOT EXISTS log (
    key CHAR(32) PRIMARY KEY,
    date TIMESTAMP NOT NULL,
    user_key CHAR(32) NOT NULL,
    action VARCHAR(20) NOT NULL,
    entity_key TEXT,
    entity_type VARCHAR(100) NOT NULL,
    status INT DEFAULT 200,
    misc JSONB DEFAULT '{}'::JSONB,

    FOREIGN KEY (user_key) REFERENCES "user"(key)
);"""


def db_open():
    con = psycopg2.connect(os.environ["DATABASE_URI"])
    cur = con.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    return con, cur


def db_close(con, cur):
    con.commit()
    cur.close()
    con.close()
