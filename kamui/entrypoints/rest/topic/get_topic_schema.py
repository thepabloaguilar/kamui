from typing import Any

from flask_restful import Resource
from returns.result import Result

from kamui.configuration.dependency_injection import di_container
from kamui.core.entity.topic_schema import TopicSchema
from kamui.core.use_case.failure import BusinessFailureDetails
from kamui.core.use_case.topic.get_topic_schema import GetTopicSchemaUseCase
from kamui.entrypoints.rest.helpers import json_response, unwrap_result_response


class GetTopicSchemaResource(Resource):
    API_PATH = "/topics/<string:topic_name>/schema"

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.get_topic_schema: GetTopicSchemaUseCase = di_container.resolve(
            GetTopicSchemaUseCase
        )

    @json_response
    @unwrap_result_response(success_status_code=200)
    def get(self, topic_name: str) -> Result[TopicSchema, BusinessFailureDetails]:
        return self.get_topic_schema(topic_name)
