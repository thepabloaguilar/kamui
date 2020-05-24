from abc import ABC, abstractmethod
from dataclasses import dataclass

from dataclasses_json import dataclass_json

from kamui.core.entity.project import Project


@dataclass_json
@dataclass
class CreateNewProjectCommand:
    title: str


class CreateNewProject(ABC):
    @abstractmethod
    def __call__(self, project_title: str) -> Project:
        pass


class CreateNewProjectUsecase:
    def __init__(self, create_new_project: CreateNewProject) -> None:
        self.__create_new_project = create_new_project

    def __call__(self, command: CreateNewProjectCommand) -> Project:
        return self.__create_new_project(command.title)
