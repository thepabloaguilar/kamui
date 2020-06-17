from typing import Any, Union

from flask import Response
from flask_restful import Resource
from returns.result import Result

from kamui.configuration.dependency_injection import di_container
from kamui.core.entity.stream import Stream
from kamui.core.use_case.failure import BusinessFailureDetails
from kamui.core.use_case.stream.create_new_stream import (
    CreateNewStreamCommand,
    CreateNewStreamFromTopicUseCase,
    SourceType,
    CreateNewStreamFromStreamUseCase,
)
from kamui.entrypoints.rest.helpers import (
    json_response,
    unwrap_result_response,
    parse_request_body,
)


class CreateNewStreamResource(Resource):
    API_PATH = "/streams"

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.__create_new_stream_from_topic: CreateNewStreamFromTopicUseCase = (
            di_container.resolve(CreateNewStreamFromTopicUseCase)
        )
        self.__create_new_stream_from_stream: CreateNewStreamFromStreamUseCase = (
            di_container.resolve(CreateNewStreamFromStreamUseCase)
        )

    @json_response
    @unwrap_result_response(success_status_code=201)
    @parse_request_body(CreateNewStreamCommand)
    def post(
        self, request_body: Result[CreateNewStreamCommand, Response]
    ) -> Result[Stream, Union[Response, BusinessFailureDetails]]:
        return request_body.unify(self.__create_new_stream)

    def __create_new_stream(
        self, command: CreateNewStreamCommand
    ) -> Result[Stream, BusinessFailureDetails]:
        if command.source_type == SourceType.TOPIC:
            return self.__create_new_stream_from_topic(command)
        return self.__create_new_stream_from_stream(command)
