from abc import ABC, abstractmethod

from kamui.core.entity.project import Project


class CreateNewProject(ABC):
    @abstractmethod
    def __call__(self, project_title: str) -> Project:
        pass


class CreateNewProjectUsecase:
    def __init__(self, create_new_project: CreateNewProject) -> None:
        self.__create_new_project = create_new_project

    def __call__(self, project_title: str) -> Project:
        return self.__create_new_project(project_title)
