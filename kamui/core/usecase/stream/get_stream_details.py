from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List
from uuid import UUID

from dataclasses_json import dataclass_json
from returns.converters import maybe_to_result
from returns.pointfree import bind
from returns.curry import curry, partial
from returns.maybe import Maybe
from returns.pipeline import flow
from returns.result import Result, Success

from kamui.core.entity.project import Project
from kamui.core.entity.stream import Stream, KSQLStreamDetailed
from kamui.core.usecase.failure import FailureDetails, BusinessFailureDetails
from kamui.core.usecase.stream import GetStreamByNameUsecase


@dataclass_json
@dataclass
class StreamDetails:
    stream: Stream
    projects: List[Project]
    ksql_stream_detailed: KSQLStreamDetailed

    @classmethod
    @curry
    def build(
        cls,
        stream: Stream,
        projects: List[Project],
        ksql_stream_detailed: KSQLStreamDetailed,
    ) -> "StreamDetails":
        return cls(stream, projects, ksql_stream_detailed)


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
        stream = self.__find_stream_by_stream_id(stream_id).bind(
            self.__verify_if_stream_exist
        )
        partial_projects = partial(stream.bind, self.__find_projects_by_stream)
        partial_ksql = partial(
            stream.bind, lambda stream_: self.__get_stream_by_name(stream_.name)
        )

        return flow(
            Result.from_value(StreamDetails.build),
            stream.apply,
            bind(lambda to_apply: partial_projects().apply(Success(to_apply))),
            bind(lambda to_apply: partial_ksql().apply(Success(to_apply))),
        )

    def __verify_if_stream_exist(
        self, stream: Maybe[Stream]
    ) -> Result[Stream, BusinessFailureDetails]:
        return maybe_to_result(stream).alt(
            lambda __: BusinessFailureDetails(
                reason="NOT_FOUND", failure_message="Stream not found"
            )
        )
