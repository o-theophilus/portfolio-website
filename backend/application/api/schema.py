from . import now


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
