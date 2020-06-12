from abc import ABC, abstractmethod
from typing import List

from returns.result import Result

from kamui.core.entity.project import Project
from kamui.core.usecase.failure import FailureDetails


class GetProjectsList(ABC):
    @abstractmethod
    def __call__(self) -> Result[List[Project], FailureDetails]:
        pass


class GetProjectsListUsecase:
    def __init__(self, get_projects_list: GetProjectsList):
        self.__get_projects_list = get_projects_list

    def __call__(self) -> Result[List[Project], FailureDetails]:
        return self.__get_projects_list()
