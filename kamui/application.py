from flask import Flask
from flask_cors import CORS

from kamui.entrypoints.rest.health import health_bp
from kamui.entrypoints.web.home import web_home_bp
from kamui.entrypoints.web.core import web_core_bp
from kamui.entrypoints.web.project import web_project_bp


def create_app():
    app = Flask(__name__)

    # Rest
    app.register_blueprint(health_bp)

    # Web
    app.register_blueprint(web_home_bp)
    app.register_blueprint(web_core_bp)
    app.register_blueprint(web_project_bp)

    CORS(app, resources={r"/api/*": {"origins": "*"}})

    return app
