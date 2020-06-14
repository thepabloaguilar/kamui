from typing import Any

from flask_restful import Resource
from returns.result import Result

from kamui.configuration.dependency_injection import di_container
from kamui.core.entity.topic import TopicNames
from kamui.core.usecase.failure import BusinessFailureDetails
from kamui.core.usecase.topic import GetAvailableTopicNamesUsecase
from kamui.entrypoints.rest.helpers import json_response, unwrap_result_response


class GetTopicNamesResource(Resource):
    API_PATH = "/topics"

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.__get_available_topic_names: GetAvailableTopicNamesUsecase = (
            di_container.resolve(GetAvailableTopicNamesUsecase)
        )

    @json_response
    @unwrap_result_response(success_status_code=200)
    def get(self) -> Result[TopicNames, BusinessFailureDetails]:
        return self.__get_available_topic_names()
