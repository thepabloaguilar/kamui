from typing import List

from returns.result import Result, Failure, Success

from kamui.core.entity.stream import KSQLStream, KSQLStreamDetailed
from kamui.core.use_case.failure import DataProviderFailureDetails, FailureDetails
from kamui.core.use_case.stream.get_ksql_streams import GetKSQLStreams
from kamui.core.use_case.stream.get_stream_by_name import GetStreamByName
from kamui.dataproviders.rest import client, HttpClient, JsonResponse
from kamui.core.use_case.stream.create_new_stream import (
    CreateNewStreamCommand,
    CreateStreamFromKafkaTopic,
    CreateNewStreamFromStream,
)


class CreateStreamFromKafkaTopicRepository(CreateStreamFromKafkaTopic):
    # TODO: Make KSQL Server URL configurable
    def __init__(self) -> None:
        self.__client: HttpClient = client
        self.__KSQL_SERVER_URL: str = "http://localhost:8088/"

    def __call__(
        self, creat_new_stream_command: CreateNewStreamCommand
    ) -> Result[CreateNewStreamCommand, DataProviderFailureDetails]:
        query_fields = ", ".join(
            [f"{field.name} {field.type}" for field in creat_new_stream_command.fields_]
        )

        response = self.__client.post(
            url=f"{self.__KSQL_SERVER_URL}ksql",
            payload={
                "ksql": f"""
                            CREATE STREAM
                                {creat_new_stream_command.stream_name} ({query_fields})
                            WITH
                                (
                                    kafka_topic='{creat_new_stream_command.source_name}',
                                    value_format='AVRO'
                                );
                        """
            },
            headers={
                "Accept": "application/vnd.ksql.v1+json",
                "Content-Type": "application/vnd.ksql.v1+json",
            },
        ).map(lambda result: creat_new_stream_command)

        return response


class GetKSQLStreamsRepository(GetKSQLStreams):
    # TODO: Make KSQL Server URL configurable
    def __init__(self) -> None:
        self.__client: HttpClient = client
        self.__KSQL_SERVER_URL: str = "http://localhost:8088/"

    def __call__(self) -> Result[List[KSQLStream], FailureDetails]:
        response = self.__client.post(
            url=f"{self.__KSQL_SERVER_URL}ksql",
            payload={
                "ksql": "SHOW STREAMS;",
                "streamsProperties": {"auto.offset.reset": "latest"},
            },
            headers={
                "Accept": "application/vnd.ksql.v1+json",
                "Content-Type": "application/vnd.ksql.v1+json",
            },
        )

        return response.bind(self.__verify_response)

    def __verify_response(
        self, response: JsonResponse
    ) -> Result[List[KSQLStream], DataProviderFailureDetails]:
        _response = response[0]
        if _response.get("@type") == "statement_error":
            return Failure(
                DataProviderFailureDetails(
                    reason="STATEMENT_ERROR",
                    dataprovider_type="REST",
                    attributes={
                        "message": _response["message"],
                        "statementText": _response["statementText"],
                    },
                )
            )
        return Success([KSQLStream(**stream) for stream in _response["streams"]])


class GetStreamByNameRepository(GetStreamByName):
    # TODO: Make KSQL Server URL configurable
    def __init__(self) -> None:
        self.__client: HttpClient = client
        self.__KSQL_SERVER_URL: str = "http://localhost:8088/"

    def __call__(self, stream_name: str) -> Result[KSQLStreamDetailed, FailureDetails]:
        response = self.__client.post(
            url=f"{self.__KSQL_SERVER_URL}ksql",
            payload={
                "ksql": f"DESCRIBE {stream_name};",
                "streamsProperties": {"auto.offset.reset": "latest"},
            },
            headers={
                "Accept": "application/vnd.ksql.v1+json",
                "Content-Type": "application/vnd.ksql.v1+json",
            },
        )

        return response.bind(self.__verify_response)

    def __verify_response(
        self, response: JsonResponse
    ) -> Result[KSQLStreamDetailed, DataProviderFailureDetails]:
        _response = response[0]
        if _response.get("@type") == "statement_error":
            return Failure(
                DataProviderFailureDetails(
                    reason="STATEMENT_ERROR",
                    dataprovider_type="REST",
                    attributes={
                        "message": _response["message"],
                        "statementText": _response["statementText"],
                    },
                )
            )
        stream = KSQLStreamDetailed(**_response["sourceDescription"])
        return Success(stream)


class CreateNewStreamFromStreamRepository(CreateNewStreamFromStream):
    # TODO: Make KSQL Server URL configurable
    def __init__(self) -> None:
        self.__client: HttpClient = client
        self.__KSQL_SERVER_URL: str = "http://localhost:8088/"

    def __call__(
        self, create_new_stream_command: CreateNewStreamCommand
    ) -> Result[CreateNewStreamCommand, FailureDetails]:
        desired_stream_fields = ",".join(
            [field.name for field in create_new_stream_command.fields_]
        )
        filters = " AND ".join(
            filter_.to_statement() for filter_ in create_new_stream_command.filters
        )

        response = self.__client.post(
            url=f"{self.__KSQL_SERVER_URL}ksql",
            payload={
                "ksql": f"""
                            CREATE STREAM {create_new_stream_command.stream_name} AS
                            SELECT {desired_stream_fields}
                            FROM {create_new_stream_command.source_name}
                            {f'WHERE {filters}' if filters else ''}
                            EMIT CHANGES;
                        """
            },
            headers={
                "Accept": "application/vnd.ksql.v1+json",
                "Content-Type": "application/vnd.ksql.v1+json",
            },
        ).map(lambda result: create_new_stream_command)

        return response
