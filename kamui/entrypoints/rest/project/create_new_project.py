from typing import Any

from flask import request, Response
from flask_restful import Resource

from kamui.configuration.dependency_injection import di_container
from kamui.core.usecase.project import CreateNewProjectUsecase
from kamui.core.usecase.project.create_new_project import CreateNewProjectCommand


class CreateNewProjectResource(Resource):
    API_PATH = "/projects"

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.__create_new_project: CreateNewProjectUsecase = di_container.resolve(
            CreateNewProjectUsecase
        )

    def post(self) -> Any:
        command = CreateNewProjectCommand.from_dict(request.json)
        return Response(
            response=self.__create_new_project(command).to_json(),
            status=201,
            mimetype="application/json",
        )
