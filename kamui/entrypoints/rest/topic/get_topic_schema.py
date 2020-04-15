from flask_restful import Resource

from kamui.configuration.dependency_injection import di_container
from kamui.core.usecase.topic.get_topic_schema import GetTopicSchemaUsecase


class GetTopicSchemaResource(Resource):
    API_PATH = "/topics/<string:topic_name>/schema"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.get_topic_schema = di_container.resolve(GetTopicSchemaUsecase)

    def get(self, topic_name: str):
        return self.get_topic_schema(topic_name)
