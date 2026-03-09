from flask import Flask, jsonify
from flask_cors import CORS

from . import api, auth, fix, log, post, postgres, report, storage, user
from .api import file_error
from .auth import forgot
from .log import get as log_get
from .post import comment, file
from .post import get as post_get
from .post import photo as post_photo
from .report import get as report_get
from .user import email
from .user import get as user_get
from .user import notification, password
from .user import photo as user_photo


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
            "message": "Welcome to Theophilus Portfolio Website"
        })

    app.register_blueprint(storage.bp)
    app.register_blueprint(postgres.bp)
    app.register_blueprint(log.bp)
    app.register_blueprint(log_get.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(forgot.bp)
    app.register_blueprint(file_error.bp)
    app.register_blueprint(report.bp)
    app.register_blueprint(report_get.bp)
    app.register_blueprint(user.bp)
    app.register_blueprint(user_get.bp)
    app.register_blueprint(email.bp)
    app.register_blueprint(password.bp)
    app.register_blueprint(user_photo.bp)
    app.register_blueprint(notification.bp)
    app.register_blueprint(post.bp)
    app.register_blueprint(post_get.bp)
    app.register_blueprint(file.bp)
    app.register_blueprint(post_photo.bp)
    app.register_blueprint(comment.bp)
    app.register_blueprint(api.bp)
    app.register_blueprint(fix.bp)

    return app
