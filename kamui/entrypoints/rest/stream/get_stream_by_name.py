from typing import Any

from flask_restful import Resource
from returns.result import Result

from kamui.configuration.dependency_injection import di_container
from kamui.core.entity.stream import KSQLStreamDetailed
from kamui.core.usecase.failure import BusinessFailureDetails
from kamui.core.usecase.stream import GetStreamByNameUsecase
from kamui.entrypoints.rest.helpers import json_response, unwrap_result_response


class GetStreamByNameResource(Resource):
    API_PATH = "/ksql-streams/<string:stream_name>"

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.__get_stream_by_name: GetStreamByNameUsecase = di_container.resolve(
            GetStreamByNameUsecase
        )

    @json_response
    @unwrap_result_response(success_status_code=200)
    def get(
        self, stream_name: str
    ) -> Result[KSQLStreamDetailed, BusinessFailureDetails]:
        return self.__get_stream_by_name(stream_name)
