from abc import ABC, abstractmethod
from functools import partial
from typing import Any

from returns.result import Result

from kamui.core.entity.topic_schema import TopicSchemaVersions, TopicSchema
from kamui.core.usecase.failure import BusinessFailureDetails


class GetTopicSchema(ABC):
    @abstractmethod
    def __call__(
        self, schema_version: int, topic_name: str
    ) -> Result[TopicSchema, Any]:
        pass


class GetTopicSchemaVersions(ABC):
    @abstractmethod
    def __call__(self, topic_name: str) -> Result[TopicSchemaVersions, Any]:
        pass


class GetTopicSchemaUsecase:
    def __init__(
        self,
        get_topic_schema: GetTopicSchema,
        get_topic_schema_versions: GetTopicSchemaVersions,
    ) -> None:
        self.__get_topic_schema = get_topic_schema
        self.__get_topic_schema_versions = get_topic_schema_versions

    def __call__(self, topic_name: str) -> Result[Any, BusinessFailureDetails]:
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

    def __get_latest_schema_version(self, topic_name: str) -> Result[int, Any]:
        return self.__get_topic_schema_versions(topic_name).map(max)
