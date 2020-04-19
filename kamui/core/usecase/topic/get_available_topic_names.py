from abc import ABC, abstractmethod

from returns.result import Result

from kamui.core.entity.topic import TopicNames
from kamui.core.usecase.failure import FailureDetails, failure_details


class GetTopicNames(ABC):
    @abstractmethod
    def __call__(self) -> Result[TopicNames, str]:
        pass


class GetAvailableTopicNamesUsecase:
    def __init__(self, get_topic_names: GetTopicNames) -> None:
        self.__get_topic_names = get_topic_names

    def __call__(self) -> Result[TopicNames, FailureDetails]:
        return (
            self.__get_topic_names()
            .map(self.__filter_topic_names)
            .alt(failure_details("Was not possible to get Topic Names"))
        )

    def __filter_topic_names(self, topic_names: TopicNames) -> TopicNames:
        return TopicNames(
            [topic_name for topic_name in topic_names if not topic_name.startswith("_")]
        )
