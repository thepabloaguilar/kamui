from typing import Tuple, Dict, Any

from flask_restful import Resource

from kamui.configuration.dependency_injection import di_container
from kamui.core.entity.stream import KSQLStreamDetailed
from kamui.core.usecase.failure import (
    BusinessFailureDetails,
    DataProviderFailureDetails,
)
from kamui.core.usecase.stream import GetStreamByNameUsecase


class GetStreamByNameResource(Resource):
    API_PATH = "/streams/<string:stream_name>/"

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.__get_stream_by_name: GetStreamByNameUsecase = di_container.resolve(
            GetStreamByNameUsecase
        )

    def get(self, stream_name: str) -> Tuple[Dict[str, Any], int]:
        return (
            self.__get_stream_by_name(stream_name)
            .map(self.__process_success)
            .fix(self.__process_failure)
            .unwrap()
        )

    def __process_success(
        self, ksql_stream_detailed: KSQLStreamDetailed
    ) -> Tuple[Dict[str, Any], int]:
        return ksql_stream_detailed.to_dict(), 200  # type: ignore

    def __process_failure(
        self, failure_details: BusinessFailureDetails
    ) -> Tuple[Dict[str, Any], int]:
        if isinstance(failure_details.failure_due, DataProviderFailureDetails):
            return failure_details.to_dict(), 503  # type: ignore
        return failure_details.to_dict(), 400  # type: ignore
