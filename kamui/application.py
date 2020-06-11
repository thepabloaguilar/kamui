from flask import Flask
from flask_cors import CORS

from kamui.entrypoints.rest.health import health_bp
from kamui.entrypoints.rest.topic import rest_topic_bp
from kamui.entrypoints.rest.stream import rest_stream_bp
from kamui.entrypoints.rest.project import rest_project_bp


def create_app() -> Flask:
    app = Flask(__name__)

    # Rest
    app.register_blueprint(health_bp)
    app.register_blueprint(rest_topic_bp)
    app.register_blueprint(rest_stream_bp)
    app.register_blueprint(rest_project_bp)

    CORS(app, resources={r"/api/*": {"origins": "*"}})

    return app
