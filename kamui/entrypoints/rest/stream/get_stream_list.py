import json
from typing import Any

from flask import Response
from flask_restful import Resource

from kamui.configuration.dependency_injection import di_container
from kamui.core.usecase.stream import GetStreamsUsecase


class GetStreamListResource(Resource):
    API_PATH = "/streams"

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.__get_streams: GetStreamsUsecase = di_container.resolve(GetStreamsUsecase)

    def get(self) -> Any:
        streams = self.__get_streams()
        stream_list = [
            json.loads(stream.to_json()) for stream in streams.unwrap()  # type: ignore
        ]
        return Response(
            response=json.dumps(stream_list), status=201, mimetype="application/json",
        )
