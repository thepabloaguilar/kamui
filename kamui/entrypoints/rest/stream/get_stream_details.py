from typing import Any
from uuid import UUID

from flask import Response
from flask_restful import Resource

from kamui.configuration.dependency_injection import di_container
from kamui.core.usecase.stream import GetStreamDetailsUsecase


class GetStreamDetailsResource(Resource):
    API_PATH = "/streams/<uuid:stream_id>"

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.__get_stream_details: GetStreamDetailsUsecase = di_container.resolve(
            GetStreamDetailsUsecase
        )

    def get(self, stream_id: UUID) -> Any:
        # TODO: Threat errors
        return Response(
            response=self.__get_stream_details(stream_id).unwrap().to_json(),
            status=200,
            mimetype="application/json",
        )
