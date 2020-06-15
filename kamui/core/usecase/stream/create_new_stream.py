from abc import ABC, abstractmethod
from enum import Enum
from typing import List, Union
from uuid import UUID

from pydantic.dataclasses import dataclass
from pydantic import BaseModel, Field
from returns.result import Result

from kamui.core.entity.source import SourceType
from kamui.core.entity.stream import Stream
from kamui.core.usecase.failure import BusinessFailureDetails, FailureDetails


class FilterCondition(Enum):
    EQUAL = "="
    DIFFERENT = "!="
    GREATER_THAN = ">"
    LESS_THAN = "<"
    GREATER_OR_EQUAL_THAN = ">="
    LESS_OR_EQUAL_THAN = "<="


class CreateNewStreamCommand(BaseModel):
    @dataclass
    class StreamField:
        name: str
        type: str

    @dataclass
    class FilterCondition:
        field: str
        condition: FilterCondition
        value: Union[int, float, bool, str]

        def to_statement(self) -> str:
            return f"{self.field} {self.condition.value} '{self.value}'"

    project_id: UUID
    stream_name: str
    fields_: List[StreamField] = Field(alias="fields")
    source_name: str
    source_type: SourceType
    filters: List[FilterCondition] = Field(default_factory=list)


class CreateStreamFromKafkaTopic(ABC):
    @abstractmethod
    def __call__(
        self, creat_new_stream_command: CreateNewStreamCommand
    ) -> Result[CreateNewStreamCommand, FailureDetails]:
        pass


class CreateNewStreamFromStream(ABC):
    @abstractmethod
    def __call__(
        self, create_new_stream_from_stream_command: CreateNewStreamCommand
    ) -> Result[CreateNewStreamCommand, FailureDetails]:
        pass


class SaveStream(ABC):
    @abstractmethod
    def __call__(
        self, creat_new_stream_command: CreateNewStreamCommand
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
        self, create_new_stream_command: CreateNewStreamCommand
    ) -> Result[Stream, BusinessFailureDetails]:
        create_new_stream_command.stream_name = (
            create_new_stream_command.stream_name.upper()
        )
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


class CreateNewStreamFromStreamUsecase:
    def __init__(
        self,
        create_new_stream_from_stream: CreateNewStreamFromStream,
        save_stream: SaveStream,
    ) -> None:
        self.__create_new_stream_from_stream = create_new_stream_from_stream
        self.__save_stream = save_stream

    def __call__(
        self, create_new_stream_command: CreateNewStreamCommand
    ) -> Result[Stream, BusinessFailureDetails]:
        # TODO: verify if fields in command are present in the stream
        create_new_stream_command.stream_name = (
            create_new_stream_command.stream_name.upper()
        )
        return (
            self.__create_new_stream_from_stream(create_new_stream_command)
            .bind(self.__save_stream)
            .alt(
                lambda failure: BusinessFailureDetails(
                    failure_message="Was not possible to create the Stream",
                    reason="NON_BUSINESS_RULE_CAUSE",
                    failure_due=failure,
                )
            )
        )
