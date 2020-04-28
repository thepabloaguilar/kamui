from typing import List
from uuid import UUID

from returns.maybe import Maybe
from returns.result import Result, Success

from kamui.core.usecase.failure import FailureDetails
from kamui.core.usecase.project.get_project_details import FindProjectByProjectId
from .model import ProjectModel
from kamui.configuration.database import database_session
from kamui.core.entity.project import Project
from kamui.core.usecase.project.create_new_project import CreateNewProject
from kamui.core.usecase.project.get_projects_list import GetProjectsList


class CreateNewProjectRepository(CreateNewProject):
    def __call__(self, project_title: str) -> Project:
        project = ProjectModel(title=project_title)
        with database_session() as session:
            session.add(project)  # type: ignore
            session.commit()  # type: ignore
            return project.to_entity()


class GetProjectsListRepository(GetProjectsList):
    def __call__(self) -> List[Project]:
        return [project.to_entity() for project in ProjectModel.query.all()]


class FindProjectByProjectIdRepository(FindProjectByProjectId):
    def __call__(self, project_id: UUID) -> Result[Maybe[Project], FailureDetails]:
        project = ProjectModel.query.filter(
            ProjectModel.project_id == project_id
        ).first()
        maybe_project: Maybe[Project] = Maybe.new(project).map(
            lambda _project: _project.to_entity()  # type: ignore
        )
        return Success(maybe_project)
