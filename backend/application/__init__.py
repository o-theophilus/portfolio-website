from flask import Flask, jsonify
from flask_cors import CORS

from . import api
from . import user
from . import post
from . import post_get
from . import feedback
from . import storage
from . import auth
from . import admin


def create_app(conf=None):
    app = Flask(__name__)
    app.config.from_prefixed_env()
    if conf:
        app.config.from_pyfile(conf)
    CORS(app)

    @app.route("/")
    def index():

        return jsonify({
            "status": 200,
            "message": "Welcome to Loup"
        })

    app.register_blueprint(api.bp)
    app.register_blueprint(user.bp)
    app.register_blueprint(post.bp)
    app.register_blueprint(post_get.bp)
    app.register_blueprint(feedback.bp)
    app.register_blueprint(storage.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(admin.bp)

    return app
