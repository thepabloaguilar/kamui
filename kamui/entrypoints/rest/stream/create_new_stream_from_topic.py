from flask import request
from flask_restful import Resource
from dataclasses_json import dataclass_json

from kamui.configuration.dependency_injection import di_container
from kamui.core.usecase.stream.create_new_stream_from_topic import (
    CreateNewStreamFromTopicCommand,
    CreateNewStreamFromTopicUsecase,
)


class CreateNewStreamFromTopicResource(Resource):
    API_PATH = "/streams/"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__create_new_stream_from_topic = di_container.resolve(
            CreateNewStreamFromTopicUsecase
        )

    def post(self):
        deserializable_body_class = dataclass_json(CreateNewStreamFromTopicCommand)
        self.__create_new_stream_from_topic(
            deserializable_body_class.from_dict(request.json)
        )
        return {"status": "ok"}, 201
