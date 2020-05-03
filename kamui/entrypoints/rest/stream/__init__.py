from flask import Blueprint
from flask_restful import Api

from .create_new_stream_from_topic import CreateNewStreamFromTopicResource
from .get_stream_by_name import GetStreamByNameResource

rest_stream_bp = Blueprint("rest_stream", __name__)
rest_stream_api = Api(rest_stream_bp, prefix="/api")

rest_stream_api.add_resource(
    CreateNewStreamFromTopicResource, CreateNewStreamFromTopicResource.API_PATH
)
rest_stream_api.add_resource(GetStreamByNameResource, GetStreamByNameResource.API_PATH)
