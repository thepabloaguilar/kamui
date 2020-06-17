from typing import Any, List

from flask_restful import Resource
from returns.result import Result

from kamui.configuration.dependency_injection import di_container
from kamui.core.entity.stream import KSQLStream
from kamui.core.use_case.failure import BusinessFailureDetails
from kamui.core.use_case.stream import GetKSQLStreamsUseCase
from kamui.entrypoints.rest.helpers import json_response, unwrap_result_response


class GetKSQLStreamsListResource(Resource):
    API_PATH = "/ksql-streams"

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.__get_ksql_streams: GetKSQLStreamsUseCase = di_container.resolve(
            GetKSQLStreamsUseCase
        )

    @json_response
    @unwrap_result_response(success_status_code=200)
    def get(self) -> Result[List[KSQLStream], BusinessFailureDetails]:
        return self.__get_ksql_streams()
