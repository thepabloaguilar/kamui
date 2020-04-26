from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Any
from uuid import UUID

from returns.result import Result

from kamui.core.entity.stream import Stream
from kamui.core.usecase.failure import BusinessFailureDetails, FailureDetails


@dataclass(frozen=True)
class CreateNewStreamFromTopicCommand:
    @dataclass(frozen=True)
    class StreamField:
        name: str
        type: str

    project_id: UUID
    stream_name: str
    fields: List[StreamField]
    topic_name: str


class CreateStreamFromKafkaTopic(ABC):
    @abstractmethod
    def __call__(
        self, creat_new_stream_command: CreateNewStreamFromTopicCommand
    ) -> Result[CreateNewStreamFromTopicCommand, FailureDetails]:
        pass


class SaveStream(ABC):
    @abstractmethod
    def __call__(
        self, creat_new_stream_command: CreateNewStreamFromTopicCommand
    ) -> Result[Stream, FailureDetails]:
        pass


class CreateNewStreamFromTopicUsecase:
    def __init__(
        self,
        create_stream_from_kafka_topic: CreateStreamFromKafkaTopic,
        save_stream: SaveStream,
    ) -> None:
        self.__create_stream_from_kafka_topic = create_stream_from_kafka_topic
        self.__save_stream = save_stream

    def __call__(
        self, create_new_stream_command: CreateNewStreamFromTopicCommand
    ) -> Result[Stream, BusinessFailureDetails]:
        return (
            self.__create_stream_from_kafka_topic(create_new_stream_command)
            .bind(self.__save_stream)
            .alt(
                lambda failure: BusinessFailureDetails(
                    failure_message="Was not possible to create the Stream",
                    reason="NON_BUSINESS_RULE_CAUSE",
                    failure_due=failure,
                )
            )
        )
