from typing import Any

from flask_restful import Resource
from returns.result import Result

from kamui.configuration.dependency_injection import di_container
from kamui.core.entity.stream import StreamList
from kamui.core.use_case.failure import BusinessFailureDetails
from kamui.core.use_case.stream import GetStreamsUseCase
from kamui.entrypoints.rest.helpers import json_response, unwrap_result_response


class GetStreamListResource(Resource):
    API_PATH = "/streams"

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.__get_streams: GetStreamsUseCase = di_container.resolve(GetStreamsUseCase)

    @json_response
    @unwrap_result_response(success_status_code=200)
    def get(self) -> Result[StreamList, BusinessFailureDetails]:
        return self.__get_streams()
