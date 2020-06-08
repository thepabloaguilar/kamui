from flask import Blueprint
from flask_restful import Api

from .create_new_stream import CreateNewStreamResource
from .get_stream_by_name import GetStreamByNameResource
from .get_ksql_streams_list import GetKSQLStreamsListResource
from .get_stream_list import GetStreamListResource
from .get_stream_details import GetStreamDetailsResource

rest_stream_bp = Blueprint("rest_stream", __name__)
rest_stream_api = Api(rest_stream_bp, prefix="/api")

rest_stream_api.add_resource(CreateNewStreamResource, CreateNewStreamResource.API_PATH)
rest_stream_api.add_resource(GetStreamByNameResource, GetStreamByNameResource.API_PATH)
rest_stream_api.add_resource(
    GetKSQLStreamsListResource, GetKSQLStreamsListResource.API_PATH
)
rest_stream_api.add_resource(GetStreamListResource, GetStreamListResource.API_PATH)
rest_stream_api.add_resource(
    GetStreamDetailsResource, GetStreamDetailsResource.API_PATH
)
