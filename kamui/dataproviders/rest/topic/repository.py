from typing import Any

from returns.result import Result, Success, Failure

from kamui.core.entity.topic import TopicNames
from kamui.core.entity.topic_schema import TopicSchemaVersions, TopicSchema
from kamui.core.usecase.failure import DataProviderFailureDetails, FailureDetails
from kamui.dataproviders.rest import client, HttpClient, JsonResponse
from kamui.core.usecase.topic.get_available_topic_names import GetTopicNames
from kamui.core.usecase.topic.get_topic_schema import (
    GetTopicSchema,
    GetTopicSchemaVersions,
)


class GetTopicNamesRepository(GetTopicNames):
    # TODO: Make Kafka URL configurable
    def __init__(self) -> None:
        self.__client: HttpClient = client
        self.__KAFKA_REST_PROXY_URL: str = "http://localhost:8082/"

    def __call__(self) -> Result[TopicNames, DataProviderFailureDetails]:
        topic_names = self.__client.get(
            url=f"{self.__KAFKA_REST_PROXY_URL}topics",
            headers={"Accept": "application/vnd.kafka.v2+json"},
        )
        return topic_names.map(lambda names: TopicNames(names))  # type: ignore


class GetTopicSchemaRepository(GetTopicSchema):
    # TODO: Make Schema Registry URL configurable
    def __init__(self) -> None:
        self.__client: HttpClient = client
        self.__SCHEMA_REGISTRY_URL: str = "http://localhost:8081/"

    def __call__(
        self, schema_version: int, topic_name: str
    ) -> Result[TopicSchema, FailureDetails]:
        response = self.__client.get(
            url=f"{self.__SCHEMA_REGISTRY_URL}subjects/{topic_name}-value/versions/{schema_version}",
            headers={"Content-Type": "application/vnd.schemaregistry.v1+json"},
        )
        return response.bind(self.__verify_response)

    def __verify_response(self, response: JsonResponse) -> Result[TopicSchema, Any]:
        if (
            isinstance(response, dict)
            and not response.get("message") == "Subject not found."
        ):
            return Success(TopicSchema.from_json(response["schema"]))  # type: ignore
        return Failure(response)


class GetTopicSchemaVersionsRepository(GetTopicSchemaVersions):
    # TODO: Make Schema Registry URL configurable
    def __init__(self) -> None:
        self.__client: HttpClient = client
        self.__SCHEMA_REGISTRY_URL: str = "http://localhost:8081/"

    def __call__(self, topic_name: str) -> Result[TopicSchemaVersions, FailureDetails]:
        response = self.__client.get(
            url=f"{self.__SCHEMA_REGISTRY_URL}subjects/{topic_name}-value/versions",
            headers={"Content-Type": "application/vnd.schemaregistry.v1+json"},
        )
        return response.bind(self.__verify_response)

    def __verify_response(
        self, response: JsonResponse
    ) -> Result[TopicSchemaVersions, Any]:
        if isinstance(response, list):
            return Success(TopicSchemaVersions(response))
        return Failure(response)
