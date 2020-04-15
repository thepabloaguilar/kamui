from abc import ABC, abstractmethod

from kamui.core.entity.topic import TopicNames


class GetTopicNames(ABC):
    @abstractmethod
    def __call__(self) -> TopicNames:
        pass


class GetAvailableTopicNamesUsecase:
    def __init__(self, get_topic_names: GetTopicNames) -> None:
        self.__get_topic_names = get_topic_names

    def __call__(self) -> TopicNames:
        return TopicNames(
            [
                topic_name
                for topic_name in self.__get_topic_names()
                if not topic_name.startswith("_")
            ]
        )
