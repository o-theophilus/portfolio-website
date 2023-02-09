from . import now

user = {
    "key": "",
    "version": "",
    "status": "anon",
    "type": "user",

    "password": "",

    "created_at": now(),
    "updated_at": now(),

    "name": "",
    "email": "",

    "setting": {
        "item_view": "grid",
        "theme": "light"
    },

    "roles": [],
    "login": False,
}


def user_schema(u):
    return {
        "status": u["status"],

        "name": u["name"],
        "email": u["email"],

        "setting": u["setting"],

        "roles": u["roles"],
        "login": u["login"],

    }


post = {
    "key": "",
    "version": "",
    "status": "draft",
    "created_at": now(),
    "updated_at": now(),
    "type": "",
    "title": "",
    "format": "markdown",
    "photos": [],
    "videos": [],
    "description": "",
    "content": "",
    "slug": "",
    "tags": []
}


def post_schema(p):
    photos = []
    if "photos" in p:
        for photo in p['photos']:
            photos.append(f"/photo/{photo}")

    return {
        "status": p["status"],
        "title": p["title"],
        "format": p["format"],
        "photos": photos,
        "videos": p["videos"] if "videos" in p else [],
        "description": p["description"],
        "content": p["content"],
        "slug": p["slug"],
        "tags": p["tags"],
        "comments": p['comments'] if "comments" in p else [],
        "type": p["type"],
        "created_at": p["created_at"],
    }


comment = {
    "key": "",
    "version": "",
    "status": "active",
    "created_at": now(),
    "updated_at": now(),
    "type": "comment",

    "post_key": "",

    "comment_key": "",

    "name": "",
    "email": "",
    "comment": ""
}


def comment_schema(c):
    return {
        "key": c["key"],

        "name": c["name"],
        "email": c["email"],
        "comment": c["comment"],
        "comment_key": c["comment_key"],

        "created_at": c["created_at"],

    }
