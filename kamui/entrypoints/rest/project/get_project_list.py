from typing import Any, List

from flask_restful import Resource
from returns.result import Result

from kamui.configuration.dependency_injection import di_container
from kamui.core.entity.project import Project
from kamui.core.usecase.failure import FailureDetails
from kamui.core.usecase.project import GetProjectsListUsecase
from kamui.entrypoints.rest.helpers import json_response, unwrap_result_response


class GetProjectListResource(Resource):
    API_PATH = "/projects"

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.__get_projects_list: GetProjectsListUsecase = di_container.resolve(
            GetProjectsListUsecase
        )

    @json_response
    @unwrap_result_response(success_status_code=200)
    def get(self) -> Result[List[Project], FailureDetails]:
        return self.__get_projects_list()
