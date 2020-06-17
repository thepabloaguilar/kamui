from abc import ABC, abstractmethod

from returns.result import Result

from kamui.core.entity.stream import KSQLStreamDetailed
from kamui.core.usecase.failure import BusinessFailureDetails, FailureDetails


class GetStreamByName(ABC):
    @abstractmethod
    def __call__(self, stream_name: str) -> Result[KSQLStreamDetailed, FailureDetails]:
        pass


class GetStreamByNameUseCase:
    def __init__(self, get_stream_by_name: GetStreamByName) -> None:
        self.__get_stream_by_name = get_stream_by_name

    def __call__(
        self, stream_name: str
    ) -> Result[KSQLStreamDetailed, BusinessFailureDetails]:
        return self.__get_stream_by_name(stream_name).alt(
            lambda failure: BusinessFailureDetails(
                reason="NON_BUSINESS_RULE_CAUSE",
                failure_message="Was not possible to get Stream",
                failure_due=failure,
            )
        )
