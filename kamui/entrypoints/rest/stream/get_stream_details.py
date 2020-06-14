from typing import Any
from uuid import UUID

from flask_restful import Resource
from returns.result import Result

from kamui.configuration.dependency_injection import di_container
from kamui.core.usecase.failure import FailureDetails
from kamui.core.usecase.stream import GetStreamDetailsUsecase
from kamui.core.usecase.stream.get_stream_details import StreamDetails
from kamui.entrypoints.rest.helpers import json_response, unwrap_result_response


class GetStreamDetailsResource(Resource):
    API_PATH = "/streams/<uuid:stream_id>"

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.__get_stream_details: GetStreamDetailsUsecase = di_container.resolve(
            GetStreamDetailsUsecase
        )

    @json_response
    @unwrap_result_response(success_status_code=200)
    def get(self, stream_id: UUID) -> Result[StreamDetails, FailureDetails]:
        return self.__get_stream_details(stream_id)
