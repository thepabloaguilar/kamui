from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Any


@dataclass(frozen=True)
class CreateNewStreamFromTopicCommand:
    @dataclass(frozen=True)
    class StreamField:
        name: str
        type: str

    stream_name: str
    fields: List[StreamField]
    topic_name: str


class CreateStreamFromKafkaTopic(ABC):
    @abstractmethod
    def __call__(self, creat_new_stream_command: CreateNewStreamFromTopicCommand):
        pass


class CreateNewStreamFromTopicUsecase:
    def __init__(
        self, create_stream_from_kafka_topic: CreateStreamFromKafkaTopic
    ) -> None:
        self.__create_stream_from_kafka_topic = create_stream_from_kafka_topic

    def __call__(
        self, create_new_stream_command: CreateNewStreamFromTopicCommand
    ) -> Any:
        return self.__create_stream_from_kafka_topic(create_new_stream_command)
