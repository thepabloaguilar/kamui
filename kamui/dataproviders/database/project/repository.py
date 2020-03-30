from typing import List

from .model import ProjectModel
from kamui.configuration.database import DatabaseBase, database_session
from kamui.core.entity.project import Project
from kamui.core.usecase.project.create_new_project import CreateNewProject
from kamui.core.usecase.project.get_projects_list import GetProjectsList


class CreateNewProjectRepository(CreateNewProject):
    def __call__(self, project_title: str) -> Project:
        project = ProjectModel(title=project_title)
        with database_session() as session:
            session.add(project)
            session.commit()
            return project.to_entity()


class GetProjectsListRepository(GetProjectsList):
    def __call__(self) -> List[Project]:
        return [project.to_entity() for project in ProjectModel.query.all()]
