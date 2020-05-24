from typing import Any, Dict, Tuple, Union

from flask import request
from flask_restful import Resource
from returns.result import Result

from kamui.configuration.dependency_injection import di_container
from kamui.core.entity.stream import Stream
from kamui.core.usecase.failure import (
    DataProviderFailureDetails,
    BusinessFailureDetails,
)
from kamui.core.usecase.stream.create_new_stream import (
    CreateNewStreamCommand,
    CreateNewStreamFromTopicUsecase,
    SourceType,
    CreateNewStreamFromStreamUsecase,
)


class CreateNewStreamResource(Resource):
    API_PATH = "/streams"

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.__create_new_stream_from_topic: CreateNewStreamFromTopicUsecase = (
            di_container.resolve(CreateNewStreamFromTopicUsecase)
        )
        self.__create_new_stream_from_stream: CreateNewStreamFromStreamUsecase = (
            di_container.resolve(CreateNewStreamFromStreamUsecase)
        )

    def post(self) -> Union[Tuple[Any, int], Tuple[Dict[str, Any], int]]:
        body_request = CreateNewStreamCommand.from_dict(request.json)  # type: ignore
        return (
            self.__create_new_stream(body_request)
            .map(self.__process_success)
            .fix(self.__process_failure)
            .unwrap()
        )

    def __create_new_stream(
        self, command: CreateNewStreamCommand
    ) -> Result[Stream, BusinessFailureDetails]:
        if command.source_type == SourceType.TOPIC:
            return self.__create_new_stream_from_topic(command)
        return self.__create_new_stream_from_stream(command)

    def __process_success(self, something: Any) -> Tuple[Any, int]:
        return something, 201

    def __process_failure(
        self, failure_details: BusinessFailureDetails
    ) -> Tuple[Dict[str, Any], int]:
        if isinstance(failure_details.failure_due, DataProviderFailureDetails):
            return failure_details.to_dict(), 503  # type: ignore
        return failure_details.to_dict(), 400  # type: ignore
