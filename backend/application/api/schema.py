from . import now

user = {
    "key": "",
    "version": "",
    "status": "anon",
    "type": "user",

    "password": "",

    "date_c": now(),
    "date_u": now(),

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
    "description": "",
    "content": "",
    "slug": "",
    "tags": ""
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
        "description": p["description"],
        "content": p["content"],
        "slug": p["slug"],
        "tags": p["tags"],
        "updated_at": p["updated_at"],
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
