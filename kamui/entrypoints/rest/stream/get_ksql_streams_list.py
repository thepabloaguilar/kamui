import json
from typing import Any

from flask import Response
from flask_restful import Resource

from kamui.configuration.dependency_injection import di_container
from kamui.core.usecase.stream import GetKSQLStreamsUsecase


class GetKSQLStreamsListResource(Resource):
    API_PATH = "/streams"

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.__get_ksql_streams: GetKSQLStreamsUsecase = di_container.resolve(
            GetKSQLStreamsUsecase
        )

    def get(self):
        streams = [
            json.loads(stream.to_json())
            for stream in self.__get_ksql_streams().unwrap()
        ]
        return Response(
            response=json.dumps(streams), status=200, mimetype="application/json",
        )
