from flask import Flask
from flask_cors import CORS

from kamui.entrypoints.rest.health import health_bp
from kamui.entrypoints.rest.topic import rest_topic_bp
from kamui.entrypoints.rest.stream import rest_stream_bp
from kamui.entrypoints.rest.project import rest_project_bp
from kamui.entrypoints.web.home import web_home_bp
from kamui.entrypoints.web.core import web_core_bp
from kamui.entrypoints.web.project import web_project_bp
from kamui.entrypoints.web.stream import web_stream_bp


def create_app() -> Flask:
    app = Flask(__name__)

    # Rest
    app.register_blueprint(health_bp)
    app.register_blueprint(rest_topic_bp)
    app.register_blueprint(rest_stream_bp)
    app.register_blueprint(rest_project_bp)

    # Web
    app.register_blueprint(web_home_bp)
    app.register_blueprint(web_core_bp)
    app.register_blueprint(web_project_bp)
    app.register_blueprint(web_stream_bp)

    CORS(app, resources={r"/api/*": {"origins": "*"}})

    return app
