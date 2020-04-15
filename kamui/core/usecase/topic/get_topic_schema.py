from abc import ABC, abstractmethod

from kamui.core.entity.topic import TopicNames, TopicSchemaVersions


class GetTopicSchema(ABC):
    @abstractmethod
    def __call__(self, topic_name: str, schema_version: int) -> TopicNames:
        pass


class GetTopicSchemaVersions(ABC):
    @abstractmethod
    def __call__(self, topic_name: str) -> TopicSchemaVersions:
        pass


class GetTopicSchemaUsecase:
    def __init__(
        self,
        get_topic_schema: GetTopicSchema,
        get_topic_schema_versions: GetTopicSchemaVersions,
    ) -> None:
        self.__get_topic_schema = get_topic_schema
        self.__get_topic_schema_versions = get_topic_schema_versions

    def __call__(self, topic_name: str):
        latest_schema_version = max(self.__get_topic_schema_versions(topic_name))
        return self.__get_topic_schema(topic_name, latest_schema_version)
