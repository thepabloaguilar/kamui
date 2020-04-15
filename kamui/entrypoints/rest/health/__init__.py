from flask import Blueprint
from flask_restful import Api

from .get_health_status import GetHealthStatus


health_bp = Blueprint("health", __name__)
health_rest_api = Api(health_bp, prefix="/api")

health_rest_api.add_resource(GetHealthStatus, GetHealthStatus.API_PATH)
