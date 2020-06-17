from abc import ABC, abstractmethod
from functools import partial

from returns.result import Result

from kamui.core.entity.topic_schema import TopicSchemaVersions, TopicSchema
from kamui.core.use_case.failure import BusinessFailureDetails, FailureDetails


class GetTopicSchema(ABC):
    @abstractmethod
    def __call__(
        self, schema_version: int, topic_name: str
    ) -> Result[TopicSchema, FailureDetails]:
        pass


class GetTopicSchemaVersions(ABC):
    @abstractmethod
    def __call__(self, topic_name: str) -> Result[TopicSchemaVersions, FailureDetails]:
        pass


class GetTopicSchemaUseCase:
    def __init__(
        self,
        get_topic_schema: GetTopicSchema,
        get_topic_schema_versions: GetTopicSchemaVersions,
    ) -> None:
        self.__get_topic_schema = get_topic_schema
        self.__get_topic_schema_versions = get_topic_schema_versions

    def __call__(self, topic_name: str) -> Result[TopicSchema, BusinessFailureDetails]:
        return (
            self.__get_latest_schema_version(topic_name)
            .bind(partial(self.__get_topic_schema, topic_name=topic_name))
            .alt(
                lambda failure: BusinessFailureDetails(
                    failure_message="Was not possible to get Topic Schema",
                    reason="NON_BUSINESS_RULE_CAUSE",
                    failure_due=failure,
                )
            )
        )

    def __get_latest_schema_version(
        self, topic_name: str
    ) -> Result[int, FailureDetails]:
        return self.__get_topic_schema_versions(topic_name).map(max)
