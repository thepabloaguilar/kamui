from abc import ABC, abstractmethod
from dataclasses import dataclass
from functools import partial
from typing import List, Optional, Any
from uuid import UUID

from returns.maybe import Maybe
from returns.result import Result, Success, Failure

from kamui.core.entity.project import Project
from kamui.core.entity.stream import Stream, KSQLStreamDetailed
from kamui.core.usecase.failure import FailureDetails, BusinessFailureDetails
from kamui.core.usecase.stream import GetStreamByNameUsecase


@dataclass
class StreamDetails:
    stream: Optional[Stream] = None
    projects: Optional[List[Project]] = None
    ksql_stream_detailed: Optional[KSQLStreamDetailed] = None


class FindStreamByStreamId(ABC):
    @abstractmethod
    def __call__(self, stream_id: UUID) -> Result[Maybe[Stream], FailureDetails]:
        pass


class FindProjectsByStream(ABC):
    @abstractmethod
    def __call__(self, stream: Stream) -> Result[List[Project], FailureDetails]:
        pass


class GetStreamDetailsUsecase:
    def __init__(
        self,
        find_stream_by_stream_id: FindStreamByStreamId,
        find_projects_by_stream: FindProjectsByStream,
        get_stream_by_name: GetStreamByNameUsecase,
    ):
        self.__find_stream_by_stream_id = find_stream_by_stream_id
        self.__find_projects_by_stream = find_projects_by_stream
        self.__get_stream_by_name = get_stream_by_name

    def __call__(self, stream_id: UUID) -> Result[StreamDetails, FailureDetails]:
        stream_details = StreamDetails()
        return (
            self.__find_stream_by_stream_id(stream_id)
            .bind(self.__verify_if_stream_exist)
            .map(partial(self.__set_attr, stream_details, "stream"))
            .bind(self.__find_projects_by_stream)
            .map(partial(self.__set_attr, stream_details, "projects"))
            .bind(lambda _: self.__get_stream_by_name(stream_details.stream.name))  # type: ignore # noqa: E501
            .map(partial(self.__set_attr, stream_details, "ksql_stream_detailed"))
            .map(lambda _: stream_details)
        )

    def __set_attr(self, obj: Any, attr: str, value: Any) -> Any:
        setattr(obj, attr, value)
        return value

    def __verify_if_stream_exist(
        self, stream: Maybe[Stream]
    ) -> Result[Stream, BusinessFailureDetails]:
        if isinstance(stream, Maybe.success_type):
            return Success(stream.unwrap())
        return Failure(
            BusinessFailureDetails(
                reason="NOT_FOUND", failure_message="Stream not found"
            )
        )
