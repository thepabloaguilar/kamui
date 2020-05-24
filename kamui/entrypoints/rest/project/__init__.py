from flask import Blueprint
from flask_restful import Api

from .get_project_list import GetProjectListResource

rest_project_bp = Blueprint("rest_project", __name__)
rest_stream_api = Api(rest_project_bp, prefix="/api")

rest_stream_api.add_resource(GetProjectListResource, GetProjectListResource.API_PATH)