from abc import ABC, abstractmethod

from returns.result import Result

from kamui.core.entity.stream import StreamList
from kamui.core.usecase.failure import FailureDetails, BusinessFailureDetails


class FindStreams(ABC):
    @abstractmethod
    def __call__(self) -> Result[StreamList, FailureDetails]:
        pass


class GetStreamsUsecase:
    def __init__(self, find_streams: FindStreams):
        self.__find_streams = find_streams

    def __call__(self) -> Result[StreamList, BusinessFailureDetails]:
        return self.__find_streams().alt(
            lambda failure: BusinessFailureDetails(
                failure_message="Was not possible to get streams",
                reason="NON_BUSINESS_RULE_CAUSE",
                failure_due=failure,
            )
        )
