from typing import Any

from flask_restful import Resource
from returns.result import Result

from kamui.configuration.dependency_injection import di_container
from kamui.core.entity.topic_schema import TopicSchema
from kamui.core.usecase.failure import BusinessFailureDetails
from kamui.core.usecase.topic.get_topic_schema import GetTopicSchemaUsecase
from kamui.entrypoints.rest.helpers import json_response, unwrap_result_response


class GetTopicSchemaResource(Resource):
    API_PATH = "/topics/<string:topic_name>/schema"

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.get_topic_schema: GetTopicSchemaUsecase = di_container.resolve(
            GetTopicSchemaUsecase
        )

    @json_response
    @unwrap_result_response(success_status_code=200)
    def get(self, topic_name: str) -> Result[TopicSchema, BusinessFailureDetails]:
        return self.get_topic_schema(topic_name)
