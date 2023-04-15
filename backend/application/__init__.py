from flask import Flask
from flask_cors import CORS

from .api import bp as api
from .api.post import bp as post
from .api.post_get import bp as post_get
from .api.post_comment import bp as comment
from .api.photo import bp as photo
from .api.tag import bp as tag
from .api.user import bp as user
from .api.auth import bp as auth
from .api.auth_password_forgot import bp as auth_password_forgot


def create_app(config_file="config.py"):
    app = Flask(__name__)
    app.config.from_pyfile(config_file)
    CORS(app)

    app.register_blueprint(api)
    app.register_blueprint(post)
    app.register_blueprint(post_get)
    app.register_blueprint(comment)
    app.register_blueprint(photo)
    app.register_blueprint(user)
    app.register_blueprint(tag)
    app.register_blueprint(auth)
    app.register_blueprint(auth_password_forgot)

    return app
