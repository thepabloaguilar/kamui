from typing import Any, Union
from uuid import UUID

from flask_restful import Resource
from returns.result import Result

from kamui.configuration.dependency_injection import di_container
from kamui.core.entity.project import Project
from kamui.core.use_case.failure import FailureDetails
from kamui.core.use_case.project import GetProjectDetailsUseCase
from kamui.core.use_case.project.get_project_details import ProjectDetails
from kamui.entrypoints.rest.helpers import json_response, unwrap_result_response


class GetProjectDetailsResource(Resource):
    API_PATH = "/projects/<uuid:project_id>"

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.__get_project_details: GetProjectDetailsUseCase = di_container.resolve(
            GetProjectDetailsUseCase
        )

    @json_response
    @unwrap_result_response(success_status_code=200)
    def get(
        self, project_id: UUID
    ) -> Result[Union[ProjectDetails, Project], FailureDetails]:
        return self.__get_project_details(project_id)
