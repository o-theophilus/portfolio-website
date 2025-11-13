from flask import Blueprint
import os
import psycopg2
import psycopg2.extras


bp = Blueprint("postgres", __name__)


schema = {
    "app": {
        "key": {
            "type": "uuid",
        },
        "alias": {
            "type": "text",
            "unique": True,
        },
        "value": {
            "type": "dict",
        },
    },

    "user": {
        "key": {
            "type": "uuid",
        },
        "status": {
            "type": "text",
            "default": "anonymous",
            "values": ["anonymous", "signedup", "confirmed", "blocked"]
        },
        "date_created": {
            "type": "datetime",
        },
        "name": {
            "type": "text",
            "max_length": 100,
        },
        "username": {
            "type": "text",
            "max_length": 20,
            "unique": True,
            "validate": r"^[A-Za-z][A-Za-z0-9-]*$"
        },
        "email": {
            "type": "text",
            "max_length": 255,
            "unique": True,
            "validate": r"^[^\s@]+@[^\s@]+\.[^\s@]+$"
        },
        "password": {
            "type": "text",
            "max_length": 18,
            "min_length": 8,
            "validate": r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]+$"
        },
        "phone": {
            "type": "text",
            "max_length": 20,
            "nullable": True
        },
        "photo": {
            "type": "text",
            "max_length": 40,
            "nullable": True
        },
        "access": {
            "type": "array_text",
        },
        "theme": {
            "type": "text",
            "default": "dark",
            "values": ["dark", "light"]
        },
    },

    "post": {
        "key": {
            "type": "uuid",
        },
        "status": {
            "type": "text",
            "default": "draft",
            "values": ["draft", "live"]
        },
        "date_created": {
            "type": "datetime",
        },
        "author_key": {
            "type": "uuid",
            "foreign_key": ["user", "key"]
        },
        "title": {
            "type": "text",
            "max_length": 100,
        },
        "slug": {
            "type": "text",
            "max_length": 100,
            "unique": True,
            "validate": "^[a-z][a-z0-9-]*$"
        },
        "content": {
            "type": "text",
            "nullable": True
        },
        "description": {
            "max_length": 500,
            "type": "text",
            "nullable": True
        },
        "photo": {
            "type": "text",
            "nullable": True
        },
        "files": {
            "type": "array_text",
        },
        "tags": {
            "type": "array_text",
        },
    },

    "comment": {
        "key": {
            "type": "uuid",
        },
        "date_created": {
            "type": "datetime",
        },
        "user_key": {
            "type": "uuid",
            "foreign_key": ["user", "key"]
        },
        "post_key": {
            "type": "uuid",
            "foreign_key": ["post", "key"]
        },
        "parent_key": {
            "type": "uuid",
            "foreign_key": ["comment", "key"],
            "nullable": True,
        },
        "comment": {
            "type": "text",
            "max_length": 500,
        },
    },

    "report": {
        "key": {
            "type": "uuid",
        },
        "date_created": {
            "type": "datetime",
        },
        "user_key": {
            "type": "uuid",
            "foreign_key": ["user", "key"]
        },
        "entity_key": {
            "type": "uuid",
        },
        "entity_type": {
            "type": "text",
            "max_length": 20,
        },
        "comment": {
            "type": "text",
            "max_length": 500,
        },
        "tags": {
            "type": "array_text",
        },
    },

    "block": {
        "key": {
            "type": "uuid",
        },
        "date_created": {
            "type": "datetime",
        },
        "admin_key": {
            "type": "uuid",
            "foreign_key": ["user", "key"]
        },
        "user_key": {
            "type": "uuid",
        },
        "comment": {
            "type": "text",
            "max_length": 500,
        },
    },

    "like": {
        "key": {
            "type": "uuid",
        },
        "date_created": {
            "type": "datetime",
        },
        "user_key": {
            "type": "uuid",
            "foreign_key": ["user", "key"]
        },
        "entity_type": {
            "type": "text",
            "max_length": 100,
        },
        "entity_key": {
            "type": "uuid",
        },
        "reaction": {
            "type": "text",
            "values": ["like", "dislike"]
        },
    },

    "code": {
        "key": {
            "type": "uuid",
        },
        "date_created": {
            "type": "datetime",
        },
        "user_key": {
            "type": "uuid",
            "foreign_key": ["user", "key"]
        },
        "pin": {
            "type": "text",
            "max_length": 10,
            "min_length": 10,
        },
        "email": {
            "type": "text",
            "max_length": 255,
            "validate": r"^[^\s@]+@[^\s@]+\.[^\s@]+$"
        },
    },

    "log": {
        "key": {
            "type": "uuid",
        },
        "date_created": {
            "type": "datetime",
        },
        "user_key": {
            "type": "uuid",
        },
        "action": {
            "type": "text",
            "max_length": 20,
        },
        "entity_key": {
            "type": "text",
            "max_length": 100,
        },
        "entity_type": {
            "type": "text",
            "max_length": 100,
        },
        "status": {
            "type": "text",
            "default": "200",
            "values": ["200", "201", "400"],
        },
        "misc": {
            "type": "dict",
        },
    },

    "session": {
        "key": {
            "type": "uuid",
        },
        "date_created": {
            "type": "datetime",
        },
        "date_updated": {
            "type": "datetime",
        },
        "user_key": {
            "type": "uuid",
            "foreign_key": ["user", "key"]
        },
        "login": {
            "type": "text",
            "default": "false",
            "values": ["false", "true", "persist"]
        },
        "remember": {
            "type": "bool",
            "default": False,
        },
    },
}

keywords = ["user", "like"]


def get_col(name, ppt):
    column = []

    default = ppt.get("default")
    _type = ppt.get("type")
    fk = ppt.get("foreign_key")

    column.append(name)

    if _type == "uuid":
        column.append("UUID")
    elif _type == "datetime":
        column.append("TIMESTAMPTZ")
    elif _type == "array_text":
        column.append("TEXT[]")
    elif _type == "array_dict":
        column.append("JSONB")
    elif _type == "dict":
        column.append("JSONB")
    elif _type == "int":
        column.append("INT")
    elif _type == "bool":
        column.append("BOOL")
    else:
        column.append("TEXT")

    if name == "key":
        column.append("PRIMARY KEY")
    elif ppt.get("unique"):
        column.append("UNIQUE")

    if (
        not ppt.get("nullable")
        and name != "key"
        and _type != "datetime"
        and _type != "dict"
        and _type != "array_text"
        and _type != "array_dict"
    ):
        column.append("NOT NULL")

    if _type == "uuid" and name == "key":
        column.append("DEFAULT gen_random_uuid()")
    elif _type == "datetime":
        column.append("DEFAULT now()")
    elif _type == "dict":
        column.append("DEFAULT '{}'::jsonb")
    elif _type == "array_text":
        column.append("DEFAULT '{}'::TEXT[]")
    elif _type == "array_dict":
        column.append("DEFAULT '[]'::jsonb")
    elif _type == "int":
        column.append("DEFAULT 0")
    elif _type == "bool":
        column.append("DEFAULT FALSE")
    elif default is not None and _type == "text":
        column.append(f"DEFAULT '{default}'")

    if fk:
        ref_table = fk[0] if fk[0] not in keywords else f'"{fk[0]}"'
        ref_col = fk[1]
        column.append(f"REFERENCES {ref_table}({ref_col})")

    return " ".join(column)


def create_tables_query():
    tables = []
    for tn, cols in schema.items():
        tn = tn if tn not in keywords else f'"{tn}"'
        table = [f"CREATE TABLE IF NOT EXISTS {tn} ("]
        cols_ = [f"    {get_col(cn, p)}" for cn, p in cols.items()]
        table.append(",\n".join(cols_))
        table.append(");")
        tables.append("\n".join(table))

    return "\n\n".join(tables)


def db_open():
    con = psycopg2.connect(os.environ["DATABASE_URI"])
    cur = con.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    return con, cur


def db_close(con, cur):
    con.commit()
    cur.close()
    con.close()
