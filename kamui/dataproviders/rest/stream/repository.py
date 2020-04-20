from typing import Any

from returns.result import Result

from kamui.core.usecase.failure import DataProviderFailureDetails
from kamui.dataproviders.rest import client, HttpClient
from kamui.core.usecase.stream.create_new_stream_from_topic import (
    CreateNewStreamFromTopicCommand,
    CreateStreamFromKafkaTopic,
)


class CreateStreamFromKafkaTopicRepository(CreateStreamFromKafkaTopic):
    # TODO: Make KSQL Server URL configurable
    def __init__(self) -> None:
        self.__client: HttpClient = client
        self.__KSQL_SERVER_URL: str = "http://localhost:8088/"

    def __call__(
        self, creat_new_stream_command: CreateNewStreamFromTopicCommand
    ) -> Result[Any, DataProviderFailureDetails]:
        query_fields = [
            f"{field.name} {field.type}" for field in creat_new_stream_command.fields
        ]

        response = self.__client.post(
            url=f"{self.__KSQL_SERVER_URL}ksql",
            payload={
                "ksql": f"CREATE STREAM {creat_new_stream_command.stream_name} ({', '.join(query_fields)}) WITH (kafka_topic='{creat_new_stream_command.topic_name}', value_format='AVRO');"
            },
            headers={
                "Accept": "application/vnd.ksql.v1+json",
                "Content-Type": "application/vnd.ksql.v1+json",
            },
        )

        return response
