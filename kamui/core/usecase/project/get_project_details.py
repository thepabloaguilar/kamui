from abc import ABC, abstractmethod
from functools import partial
from typing import Union, List
from uuid import UUID

from pydantic.dataclasses import dataclass
from returns.maybe import Maybe
from returns.result import Result, Success, Failure

from kamui.core.entity.project import Project
from kamui.core.entity.stream import Stream, StreamList
from kamui.core.usecase.failure import FailureDetails, BusinessFailureDetails


@dataclass
class ProjectDetails:
    project: Project
    streams: List[Stream]


class FindProjectByProjectId(ABC):
    @abstractmethod
    def __call__(self, project_id: UUID) -> Result[Maybe[Project], FailureDetails]:
        pass


class FindStreamsByProject(ABC):
    @abstractmethod
    def __call__(self, project: Project) -> Result[StreamList, FailureDetails]:
        pass


class GetProjectDetailsUseCase:
    def __init__(
        self,
        find_project_by_project_id: FindProjectByProjectId,
        find_streams_by_project: FindStreamsByProject,
    ):
        self.__find_project_by_project_id = find_project_by_project_id
        self.__find_streams_by_project = find_streams_by_project

    def __call__(
        self, project_id: UUID
    ) -> Result[Union[ProjectDetails, Project], FailureDetails]:
        project = self.__find_project_by_project_id(project_id).bind(
            self.__verify_if_project_exist
        )
        if isinstance(project, Result.success_type):
            project_value = project.unwrap()
            return project.bind(self.__find_streams_by_project).map(  # type: ignore
                partial(ProjectDetails, project_value)
            )
        return project

    def __verify_if_project_exist(
        self, project: Maybe[Project]
    ) -> Result[Project, BusinessFailureDetails]:
        if isinstance(project, Maybe.success_type):
            return Success(project.unwrap())
        return Failure(
            BusinessFailureDetails(
                reason="NOT_FOUND", failure_message="Project not found"
            )
        )
