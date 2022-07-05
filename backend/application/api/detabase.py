from flask import current_app
from deta import Deta


def photo_drive():
    return Deta(current_app.config["DETA_KEY"]).Drive("meji")


def db():
    db_name_name = "live_db"
    if current_app.config["ENV"] == "development":
        db_name_name = "dev_db"
    return Deta(current_app.config["DETA_KEY"]).Base(db_name_name)


def get_db():
    return db().fetch().items


def db_add(x):
    return db().put(x)


def db_add_many(x):
    return db().put_many(x)


def db_delete(key):
    return db().delete(key)


def db_get(db, ent, ppt, val):
    entity = None
    for row in db:
        if "type" in row and ppt in row:
            if row["type"] == ent and row[ppt] == val:
                entity = row
                break
    return entity
