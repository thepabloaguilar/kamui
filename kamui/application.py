from flask import Flask

from kamui.entrypoints.rest.health import health_bp
from kamui.entrypoints.web.home import web_home_bp


def create_app():
    app = Flask(__name__)

    app.register_blueprint(health_bp)
    app.register_blueprint(web_home_bp)

    return app
