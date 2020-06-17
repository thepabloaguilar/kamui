from uuid import UUID

from returns.maybe import Maybe
from returns.result import Result, Success

from kamui.configuration.database import database_session
from kamui.core.entity.project import Project
from kamui.core.entity.stream import StreamList, Stream
from kamui.core.use_case.failure import FailureDetails
from kamui.core.use_case.project.get_project_details import FindStreamsByProject
from kamui.core.use_case.stream.create_new_stream import (
    SaveStream,
    CreateNewStreamCommand,
)
from kamui.core.use_case.stream.get_stream_details import FindStreamByStreamId
from kamui.core.use_case.stream.get_streams import FindStreams
from kamui.dataproviders.database.stream_project.model import StreamProjectModel
from kamui.dataproviders.database.stream.model import StreamModel


class SaveStreamRepository(SaveStream):
    def __call__(
        self, creat_new_stream_command: CreateNewStreamCommand
    ) -> Result[Stream, FailureDetails]:
        stream = StreamModel(
            name=creat_new_stream_command.stream_name,
            source_type=creat_new_stream_command.source_type,
            source_name=creat_new_stream_command.source_name,
        )
        stream_project = StreamProjectModel(
            stream=stream, project_id=creat_new_stream_command.project_id
        )
        with database_session() as session:
            session.add(stream_project)
            session.commit()
            return Success(stream.to_entity())


class FindStreamsRepository(FindStreams):
    def __call__(self) -> Result[StreamList, FailureDetails]:
        find_streams_query = StreamModel.query.all()
        return Success(
            StreamList([stream.to_entity() for stream in find_streams_query])
        )


class FindStreamByStreamIdRepository(FindStreamByStreamId):
    def __call__(self, stream_id: UUID) -> Result[Maybe[Stream], FailureDetails]:
        stream = StreamModel.query.filter(StreamModel.stream_id == stream_id).first()
        maybe_stream: Maybe[Stream] = Maybe.from_value(stream).map(
            lambda _stream: _stream.to_entity()  # type: ignore
        )
        return Success(maybe_stream)


class FindStreamsByProjectRepository(FindStreamsByProject):
    def __call__(self, project: Project) -> Result[StreamList, FailureDetails]:
        find_streams_query = StreamModel.query.filter(
            StreamModel.projects.any(project_id=project.project_id)
        )
        return Success(
            StreamList([stream.to_entity() for stream in find_streams_query])
        )
