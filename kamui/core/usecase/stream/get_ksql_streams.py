from abc import ABC, abstractmethod
from typing import List

from returns.result import Result

from kamui.core.entity.stream import KSQLStream
from kamui.core.usecase.failure import FailureDetails, BusinessFailureDetails


class GetKSQLStreams(ABC):
    @abstractmethod
    def __call__(self) -> Result[List[KSQLStream], FailureDetails]:
        pass


class GetKSQLStreamsUsecase:
    def __init__(self, get_stream_names: GetKSQLStreams) -> None:
        self.__get_stream_names = get_stream_names

    def __call__(self) -> Result[List[KSQLStream], BusinessFailureDetails]:
        return self.__get_stream_names().alt(
            lambda failure: BusinessFailureDetails(
                reason="NON_BUSINESS_RULE_CAUSE",
                failure_message="An error occurred while getting the stream list",
                failure_due=failure,
            )
        )
