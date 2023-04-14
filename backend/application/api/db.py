from flask import current_app
from deta import Deta


def base():
    name = "live"
    # if current_app.config["DEBUG"]:
    #     name = "test"
    return Deta(current_app.config["DETA_KEY"]).Base(name)


def data():
    return base().fetch().items


def get(type_, ppt, val, db=None):
    if not db:
        db = data()
    item = None
    for row in db:
        if "type" in row and ppt in row:
            if row["type"] == type_ and row[ppt] == val:
                item = row
                break
    return item


def get_type(type_, db=None):
    if not db:
        db = data()
    items = []
    for row in db:
        if "type" in row and row["type"] == type_:
            items.append(row)
    return items


def add(x):
    return base().put(x)


def add_many(x):
    return base().put_many(x)


def rem(key):
    return base().delete(key)
