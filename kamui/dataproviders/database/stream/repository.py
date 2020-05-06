from returns.result import Result, Success

from kamui.configuration.database import database_session
from kamui.core.entity.project import Project
from kamui.core.entity.stream import StreamList, Stream
from kamui.core.usecase.failure import FailureDetails
from kamui.core.usecase.project.get_project_details import FindStreamsByProject
from kamui.core.usecase.stream.create_new_stream import (
    SaveStream,
    CreateNewStreamCommand,
)
from kamui.dataproviders.database.stream.model import StreamModel


class SaveStreamRepository(SaveStream):
    def __call__(
        self, creat_new_stream_command: CreateNewStreamCommand
    ) -> Result[Stream, FailureDetails]:
        stream = StreamModel(
            name=creat_new_stream_command.stream_name,
            source_type=creat_new_stream_command.source_type,
            source_name=creat_new_stream_command.source_name,
            project_id=creat_new_stream_command.project_id,
        )
        with database_session() as session:
            session.add(stream)  # type: ignore
            session.commit()  # type: ignore
            return Success(stream.to_entity())


class FindStreamsByProjectRepository(FindStreamsByProject):
    def __call__(self, project: Project) -> Result[StreamList, FailureDetails]:
        find_streams_query = StreamModel.query.filter(
            StreamModel.project_id == project.project_id
        )
        return Success(
            StreamList([stream.to_entity() for stream in find_streams_query])
        )
