from typing import List
from uuid import UUID

from returns.maybe import Maybe
from returns.result import Result, Success

from kamui.core.entity.stream import Stream
from kamui.core.use_case.failure import FailureDetails
from kamui.core.use_case.project.get_project_details import FindProjectByProjectId
from kamui.core.use_case.stream.get_stream_details import FindProjectsByStream
from .model import ProjectModel
from kamui.configuration.database import database_session
from kamui.core.entity.project import Project
from kamui.core.use_case.project.create_new_project import CreateNewProject
from kamui.core.use_case.project.get_projects_list import GetProjectsList
from ..stream.model import StreamModel


class CreateNewProjectRepository(CreateNewProject):
    def __call__(self, project_title: str) -> Result[Project, FailureDetails]:
        project = ProjectModel(title=project_title)
        with database_session() as session:
            session.add(project)
            session.commit()
            return Success(project.to_entity())


class GetProjectsListRepository(GetProjectsList):
    def __call__(self) -> Result[List[Project], FailureDetails]:
        return Success([project.to_entity() for project in ProjectModel.query.all()])


class FindProjectByProjectIdRepository(FindProjectByProjectId):
    def __call__(self, project_id: UUID) -> Result[Maybe[Project], FailureDetails]:
        project = ProjectModel.query.filter(
            ProjectModel.project_id == project_id
        ).first()
        maybe_project: Maybe[Project] = Maybe.from_value(project).map(
            lambda _project: _project.to_entity()  # type: ignore
        )
        return Success(maybe_project)


class FindProjectsByStreamRepository(FindProjectsByStream):
    def __call__(self, stream: Stream) -> Result[List[Project], FailureDetails]:
        projects = ProjectModel.query.filter(
            ProjectModel.streams.any(StreamModel.stream_id == stream.stream_id)
        )
        return Success([project.to_entity() for project in projects])
