from flask import Blueprint
from flask_restful import Api

from .get_topic_schema import GetTopicSchemaResource
from .get_topic_names import GetTopicNamesResource


rest_topic_bp = Blueprint("rest_topic", __name__)
rest_topic_api = Api(rest_topic_bp, prefix="/api")

rest_topic_api.add_resource(GetTopicSchemaResource, GetTopicSchemaResource.API_PATH)
rest_topic_api.add_resource(GetTopicNamesResource, GetTopicNamesResource.API_PATH)
