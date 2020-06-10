from typing import Any, Tuple

from flask_restful import Resource

from kamui.configuration.dependency_injection import di_container
from kamui.core.entity.topic import TopicNames
from kamui.core.usecase.failure import FailureDetails
from kamui.core.usecase.topic import GetAvailableTopicNamesUsecase


class GetTopicNamesResource(Resource):
    API_PATH = "/topics"

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.__get_available_topic_names = di_container.resolve(
            GetAvailableTopicNamesUsecase
        )

    def dispatch_request(self) -> Any:
        available_topic_names = self.__get_available_topic_names()
        return (
            available_topic_names.map(self.__process_success_return)
            .fix(self.__process_failure_return)
            .unwrap()
        )

    def __process_success_return(
        self, available_topic_names: TopicNames
    ) -> Tuple[TopicNames, int]:
        return available_topic_names, 200

    def __process_failure_return(self, failure_details: FailureDetails) -> Any:
        return {"status": "error"}, 503
