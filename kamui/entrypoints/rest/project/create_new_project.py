from typing import Any, Union

from flask import Response
from flask_restful import Resource
from returns.result import Result

from kamui.configuration.dependency_injection import di_container
from kamui.core.entity.project import Project
from kamui.core.use_case.failure import FailureDetails
from kamui.core.use_case.project import CreateNewProjectUseCase
from kamui.core.use_case.project.create_new_project import CreateNewProjectCommand
from kamui.entrypoints.rest.helpers import (
    parse_request_body,
    unwrap_result_response,
    json_response,
)


class CreateNewProjectResource(Resource):
    API_PATH = "/projects"

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.__create_new_project: CreateNewProjectUseCase = di_container.resolve(
            CreateNewProjectUseCase
        )

    @json_response
    @unwrap_result_response(success_status_code=201)
    @parse_request_body(CreateNewProjectCommand)
    def post(
        self, request_body: Result[CreateNewProjectCommand, Response]
    ) -> Result[Project, Union[Response, FailureDetails]]:
        return request_body.unify(self.__create_new_project)
