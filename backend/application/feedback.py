from flask import Blueprint, jsonify, request
from . import db
from .tools import token_to_user
from uuid import uuid4
from datetime import datetime, timedelta


bp = Blueprint("comment", __name__)


def now(day=0):
    return (datetime.now() + timedelta(days=1) * day).replace(
        microsecond=0).isoformat()


def comment_template(
        comment: str,
        user_key: str,
        path: list = []
):
    return {
        "type": "comment",
        "key": uuid4().hex,
        "version": uuid4().hex,
        "created_at": now(),
        "updated_at": now(),

        "comment": comment,
        "user_key": user_key,
        "path": path,

        "status": "active",  # active, deleted
        "upvote": [],
        "downvote": []
    }


def comment_schema(c, data=[]):
    for row in data:
        if row["type"] == "user" and c["user_key"] == row["key"]:
            c["user_name"] = row["name"]
            break

    return {
        "key": c["key"],
        "comment": c["comment"],
        "user_key": c["user_key"],
        "user_name": c["user_name"],
        "path": c["path"],
        "upvote": c["upvote"],
        "downvote": c["downvote"],

        "created_at": c["created_at"],
    }


def rating_template(
        rating: str,
        user_key: str,
        post_key: str,
):
    return {
        "type": "rating",
        "key": uuid4().hex,
        "version": uuid4().hex,
        "created_at": now(),
        "updated_at": now(),

        "rating": rating,
        "user_key": user_key,
        "post_key": post_key,
    }


def rating_schema(rating):
    return {
        "rating": rating["rating"],
        "user_key": rating["user_key"]
    }


def report_template(
        user_key: str,
        entity_key: str,
        comment: str,
):
    return {
        "type": "report",
        "key": uuid4().hex,
        "version": uuid4().hex,
        "created_at": now(),
        "updated_at": now(),

        "user_key": user_key,
        "entity_key": entity_key,
        "comment": comment,
    }


@bp.get("/comment/<key>")
def get_comments(key, data=None, user=None):
    data = data if data else db.data()
    user = user if user else token_to_user(data)
    if not user:
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    setting = user["setting"]

    comments = []
    for row in data:
        if (
            row["type"] == "comment"
            and row["status"] != "deleted"
            and row["path"][0] == key
        ):
            if setting["sort_comment_by"] == "vote":
                row["vote"] = len(row["upvote"]) - len(row["downvote"])
            comments.append(row)

    if setting["sort_comment_by"] == "date":
        setting["sort_comment_by"] = "created_at"
    comments = sorted(
        comments,
        key=lambda d: d[setting["sort_comment_by"]],
        reverse=setting["sort_comment_reverse"])

    return jsonify({
        "status": 200,
        "comments": [comment_schema(c, data) for c in comments]
    })


@bp.post("/comment/<key>")
def add(key):
    if "comment" not in request.json or not request.json["comment"]:
        return jsonify({
            "status": 400,
            "comment": "cannot be empty"
        })

    data = db.data()

    owner = db.get_key(key)
    user = token_to_user(data)
    if (
        not user or not owner
        or owner["type"] not in ["post", "comment"]
    ):
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    if user["status"] != "verified" or not user["login"]:
        return jsonify({
            "status": 400,
            "error": "unauthorised access"
        })

    path = [owner["key"]]
    if owner["type"] == "comment":
        path = [*owner["path"], owner["key"]]

    comment = db.add(comment_template(
        request.json["comment"],
        user["key"],
        path,
    ))

    data.append(comment)
    return get_comments(comment["path"][0], data, user)


@bp.post("/comment/vote/<key>")
def vote(key):
    data = db.data()

    user = token_to_user(data)
    comment = db.get("comment", "key", key, data)
    if (
        not user or not comment
        or comment["status"] == "deleted"
        or "vote" not in request.json
        or not request.json["vote"]
        or request.json["vote"] not in ["up", "down"]
    ):
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    if user["status"] != "verified" or not user["login"]:
        return jsonify({
            "status": 400,
            "error": "unauthorised access"
        })

    if user["key"] in comment["upvote"]:
        comment["upvote"].remove(user["key"])
    elif user["key"] in comment["downvote"]:
        comment["downvote"].remove(user["key"])

    comment[f"{request.json['vote']}vote"].append(user["key"])
    db.add(comment)

    for row in data:
        if row["key"] == comment["key"]:
            row = comment

    return get_comments(comment["path"][0], data, user)


@bp.delete("/comment/<key>")
def delete(key):
    data = db.data()

    user = token_to_user(data)

    comment = None
    to_delete = []

    for row in data:
        if (
            row["key"] == key
            and row["type"] == "comment"
        ):
            comment = row
        elif (
            row["type"] == "comment"
            and key in row["path"]
        ):
            to_delete.append(row)

    if (
        not user or not comment
        or comment["status"] == "deleted"
        or comment["user_key"] != user["key"]
    ):
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    to_delete.append(comment)
    for row in to_delete:
        row["status"] = "deleted"

    while len(to_delete) > 0:
        db.add_many(to_delete[:25])
        to_delete = to_delete[25:]

    for row in data:
        for rox in to_delete:
            if row["key"] == rox["key"]:
                row = rox

    return get_comments(comment["path"][0], data, user)


@bp.post("/rating/<key>")
def add_rating(key):

    data = db.data()

    user = token_to_user(data)
    post = db.get_key(key, data)
    if (
        not user or not post
        or post["type"] != "post"
    ):
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    if user["status"] != "verified" or not user["login"]:
        return jsonify({
            "status": 400,
            "error": "unauthorised access"
        })

    rating_value = 0
    if (
        "rating" in request.json
        and type(request.json["rating"]) is int
        and -5 <= request.json["rating"] <= 5
    ):
        rating_value = request.json["rating"]

    rating = None
    ratings = []
    for row in data:
        if (
            row["type"] == "rating"
            and row["post_key"] == post["key"]
        ):
            ratings.append(row)
            if row["user_key"] == user["key"]:
                row["rating"] = rating_value
                rating = row

    if not rating:
        rating = rating_template(
            rating_value,
            user["key"],
            post["key"]
        )
        data.append(rating)

    db.add(rating)

    ratings = [rating_schema(c) for c in ratings]

    return jsonify({
        "status": 200,
        "ratings": ratings
    })


@bp.post("/report/<key>")
def report(key):

    if "comment" not in request.json or not request.json["comment"]:
        return jsonify({
            "status": 400,
            "comment": "cannot be empty"
        })

    data = db.data()

    user = token_to_user(data)
    entity = db.get_key(key, data)
    if (
        not user or not entity
        or user["status"] != "verified"
        or not user["login"]
        or entity["type"] not in ["user", "comment"]
        or entity["type"] == "comment" and entity["user_key"] == user["key"]
        or entity["type"] == "user" and entity["key"] == user["key"]
        or entity["status"] == "deleted"
    ):
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    db.add(report_template(
        user["key"],
        entity["key"],
        request.json["comment"]
    ))

    return jsonify({
        "status": 200,
    })
