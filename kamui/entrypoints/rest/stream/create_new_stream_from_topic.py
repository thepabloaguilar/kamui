from dataclasses import dataclass
from typing import Any, Dict, Tuple, Union

from flask import request
from flask_restful import Resource
from dataclasses_json import dataclass_json
from returns.result import Result

from kamui.configuration.dependency_injection import di_container
from kamui.core.entity.stream import Stream
from kamui.core.usecase.failure import (
    DataProviderFailureDetails,
    BusinessFailureDetails,
)
from kamui.core.usecase.stream.create_new_stream_from_topic import (
    CreateNewStreamCommand,
    CreateNewStreamFromTopicUsecase,
)


@dataclass_json
@dataclass(frozen=True)
class CreateNewStreamCommandVO:
    stream_origin: str
    create_new_stream_command: CreateNewStreamCommand


class CreateNewStreamFromTopicResource(Resource):
    API_PATH = "/streams/"

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.__create_new_stream_from_topic: CreateNewStreamFromTopicUsecase = (
            di_container.resolve(CreateNewStreamFromTopicUsecase)
        )

    def post(self) -> Union[Tuple[Any, int], Tuple[Dict[str, Any], int]]:
        body_request = CreateNewStreamCommandVO.from_dict(request.json)  # type: ignore
        return (
            self.__create_new_stream(body_request)
            .map(self.__process_success)
            .fix(self.__process_failure)
            .unwrap()
        )

    def __create_new_stream(
        self, command: CreateNewStreamCommandVO
    ) -> Result[Stream, BusinessFailureDetails]:
        # TODO: Verify all cases of `command.stream_origin`
        return self.__create_new_stream_from_topic(command.create_new_stream_command)

    def __process_success(self, something: Any) -> Tuple[Any, int]:
        return something, 201

    def __process_failure(
        self, failure_details: BusinessFailureDetails
    ) -> Tuple[Dict[str, Any], int]:
        if isinstance(failure_details.failure_due, DataProviderFailureDetails):
            return failure_details.to_dict(), 503  # type: ignore
        return failure_details.to_dict(), 400  # type: ignore
