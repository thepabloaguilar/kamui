from abc import ABC, abstractmethod
from typing import List

from kamui.core.entity.project import Project


class GetProjectsList(ABC):
    @abstractmethod
    def __call__(self) -> List[Project]:
        pass


class GetProjectsListUsecase:
    def __init__(self, get_projects_list: GetProjectsList):
        self.__get_projects_list = get_projects_list

    def __call__(self) -> List[Project]:
        return self.__get_projects_list()
