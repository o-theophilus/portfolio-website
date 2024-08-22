from flask import Flask, jsonify
from flask_cors import CORS

from . import api
from . import user
from . import user_get
from . import post
from . import post_get
from . import comment
from . import report
from . import engagement
from . import storage
from . import account
from . import admin
from . import log


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
    app.register_blueprint(user_get.bp)
    app.register_blueprint(post.bp)
    app.register_blueprint(post_get.bp)
    app.register_blueprint(comment.bp)
    app.register_blueprint(report.bp)
    app.register_blueprint(engagement.bp)
    app.register_blueprint(storage.bp)
    app.register_blueprint(account.bp)
    app.register_blueprint(admin.bp)
    app.register_blueprint(log.bp)

    return app
