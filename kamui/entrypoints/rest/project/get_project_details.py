from typing import Any
from uuid import UUID

from flask import Response
from flask_restful import Resource

from kamui.configuration.dependency_injection import di_container
from kamui.core.usecase.project import GetProjectDetailsUsecase


class GetProjectDetailsResource(Resource):
    API_PATH = "/projects/<uuid:project_id>"

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.__get_project_details: GetProjectDetailsUsecase = di_container.resolve(
            GetProjectDetailsUsecase
        )

    def get(self, project_id: UUID) -> Any:
        # TODO: Threat errors
        return Response(
            response=self.__get_project_details(project_id).unwrap().to_json(),
            status=200,
            mimetype="application/json",
        )
