from abc import ABC, abstractmethod
from dataclasses import dataclass
from functools import partial
from typing import List, Optional, Union
from uuid import UUID

from returns.maybe import Maybe
from returns.result import Result, Success, Failure

from kamui.core.entity.project import Project
from kamui.core.entity.stream import Stream
from kamui.core.usecase.failure import FailureDetails, BusinessFailureDetails


@dataclass
class StreamDetails:
    stream: Stream
    projects: Optional[List[Project]]


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
    ):
        self.__find_stream_by_stream_id = find_stream_by_stream_id
        self.__find_projects_by_stream = find_projects_by_stream

    def __call__(
        self, stream_id: UUID
    ) -> Result[Union[StreamDetails, Stream], FailureDetails]:
        stream = self.__find_stream_by_stream_id(stream_id).bind(
            self.__verify_if_stream_exist
        )
        if isinstance(stream, Result.success_type):
            stream_value = stream.unwrap()
            return stream.bind(self.__find_projects_by_stream).map(  # type: ignore
                partial(StreamDetails, stream_value)
            )
        return stream

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
