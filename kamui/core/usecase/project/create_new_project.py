from abc import ABC, abstractmethod
from dataclasses import dataclass

from dataclasses_json import dataclass_json
from returns.result import Result

from kamui.core.entity.project import Project
from kamui.core.usecase.failure import FailureDetails


@dataclass_json
@dataclass
class CreateNewProjectCommand:
    title: str


class CreateNewProject(ABC):
    @abstractmethod
    def __call__(self, project_title: str) -> Result[Project, FailureDetails]:
        pass


class CreateNewProjectUsecase:
    def __init__(self, create_new_project: CreateNewProject) -> None:
        self.__create_new_project = create_new_project

    def __call__(
        self, command: CreateNewProjectCommand
    ) -> Result[Project, FailureDetails]:
        return self.__create_new_project(command.title)
