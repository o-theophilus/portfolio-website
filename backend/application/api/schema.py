
from werkzeug.security import generate_password_hash
from uuid import uuid4
from datetime import datetime, timedelta


def now(day=0):
    return (datetime.now() + timedelta(days=1) * day).replace(
        microsecond=0).isoformat()


def user_template(
        name: str,
        email: str,
        password: str,
        status: str = "anonymous",
        roles: list = []
):

    return {
        "type": "user",
        "key": uuid4().hex,
        "version": uuid4().hex,
        "created_at": now(),
        "updated_at": now(),

        "name": name,
        "email": email,
        "password": generate_password_hash(password, method="sha256"),

        "status": status,  # anonymous, verified, deleted
        "login": False,
        "roles": roles,
        "setting": {
                "theme": "dark"
        }
    }


def user_schema(u):
    return {
        "key": u["key"],
        "status": u["status"],

        "name": u["name"],
        "email": u["email"],

        "setting": u["setting"],

        "roles": u["roles"],
        "login": u["login"],

    }


def post_template(
        type: str,
        title: str,
        slug: str,
):
    return {
        "type": type,  # blog, project
        "key": uuid4().hex,
        "version": uuid4().hex,
        "created_at": now(),
        "updated_at": now(),

        "status": "draft",  # draft, publish, deleted
        "slug": slug,
        "title": title,
        "content": "",
        "description": "",
        "format": "markdown",  # markdown, url
        "photos": [],
        "videos": [],
        "tags": []
    }


def post_schema(p, data=[]):
    photos = []
    if "photos" in p:
        for photo in p['photos']:
            photos.append(f"photo/{photo}")

    return {
        "key": p["key"],
        "status": p["status"],
        "title": p["title"],
        "format": p["format"],
        "photos": photos,
        "videos": p["videos"] if "videos" in p else [],
        "description": p["description"],
        "content": p["content"],
        "slug": p["slug"],
        "tags": p["tags"],
        "type": p["type"],
        "created_at": p["created_at"],
    }


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
