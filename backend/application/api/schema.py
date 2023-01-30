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


def schema(p):
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
        "created_at": p["created_at"],
    }


def user_schema(user):
    return {
        "status": user["status"],

        "name": user["name"],
        "email": user["email"],

        "setting": user["setting"],

        "roles": user["roles"],
        "login": user["login"],

    }
