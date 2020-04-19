from typing import NewType, List
from dataclasses import dataclass
from dataclasses_json import dataclass_json


TopicSchemaVersions = NewType("TopicSchemaVersions", List[int])


@dataclass_json
@dataclass(frozen=True)
class TopicSchemaField:
    name: str
    type: str


@dataclass_json
@dataclass(frozen=True)
class TopicSchema:
    type: str
    name: str
    namespace: str
    fields: List[TopicSchemaField]
