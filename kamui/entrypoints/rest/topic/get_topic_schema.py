from typing import Tuple, Any, Dict

from flask_restful import Resource

from kamui.configuration.dependency_injection import di_container
from kamui.core.entity.topic_schema import TopicSchema
from kamui.core.usecase.failure import FailureDetails
from kamui.core.usecase.topic.get_topic_schema import GetTopicSchemaUsecase


class GetTopicSchemaResource(Resource):
    API_PATH = "/topics/<string:topic_name>/schema"

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.get_topic_schema = di_container.resolve(GetTopicSchemaUsecase)

    def get(self, topic_name: str) -> Tuple[Dict[str, Any], int]:
        return (  # type: ignore
            self.get_topic_schema(topic_name)
            .map(self.__process_success)
            .fix(self.__process_failure)
            .unwrap()
        )

    def __process_success(
        self, topic_schema: TopicSchema
    ) -> Tuple[Dict[str, Any], int]:
        return topic_schema.to_dict(), 200  # type: ignore

    def __process_failure(
        self, failure_details: FailureDetails
    ) -> Tuple[Dict[str, Any], int]:
        return failure_details.to_dict(), 503  # type: ignore
