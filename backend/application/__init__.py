from flask import Flask, jsonify
from flask_cors import CORS

from . import storage
from . import log
from .log import get as log_get
from . import auth
from .auth import forgot
from . import admin
from .admin import get as admin_get
from .admin import access
from .admin import action
from .admin import block
from .admin.block import get as block_get
from .admin import file_error
from .admin import highlight
from .admin.highlight import get as highlight_get
from . import report
from .report import get as report_get
from . import user
from .user import get as user_get
from .user import email
from .user import password
from .user import photo as user_photo
from .user import notification
from . import post
from .post import file
from .post import get as post_get
from .post import photo as post_photo
from .post import engage
from .post.engage import get as post_engage_get
from .post import comment
from .post.comment import get as comment_get
from . import api
from .api import db
from . import fix


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
    app.register_blueprint(log.bp)
    app.register_blueprint(log_get.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(forgot.bp)
    app.register_blueprint(admin.bp)
    app.register_blueprint(admin_get.bp)
    app.register_blueprint(access.bp)
    app.register_blueprint(action.bp)
    app.register_blueprint(block.bp)
    app.register_blueprint(block_get.bp)
    app.register_blueprint(file_error.bp)
    app.register_blueprint(highlight.bp)
    app.register_blueprint(highlight_get.bp)
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
    app.register_blueprint(engage.bp)
    app.register_blueprint(post_engage_get.bp)
    app.register_blueprint(comment.bp)
    app.register_blueprint(comment_get.bp)
    app.register_blueprint(api.bp)
    app.register_blueprint(db.bp)
    app.register_blueprint(fix.bp)

    return app
