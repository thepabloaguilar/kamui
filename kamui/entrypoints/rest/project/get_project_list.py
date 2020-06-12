import json
from typing import Any

from flask import Response
from flask_restful import Resource

from kamui.configuration.dependency_injection import di_container
from kamui.core.usecase.project import GetProjectsListUsecase


class GetProjectListResource(Resource):
    API_PATH = "/projects"

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.__get_projects_list = di_container.resolve(GetProjectsListUsecase)

    def get(self) -> Any:
        projects_list = self.__get_projects_list()
        projects_list = [json.loads(project.to_json()) for project in projects_list]
        return Response(
            response=json.dumps(projects_list), status=200, mimetype="application/json",
        )
