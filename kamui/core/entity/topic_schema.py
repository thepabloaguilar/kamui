from typing import NewType, List

from pydantic import BaseModel, Field
from pydantic.dataclasses import dataclass

TopicSchemaVersions = NewType("TopicSchemaVersions", List[int])


@dataclass(frozen=True)
class TopicSchemaField:
    name: str
    type: str


class TopicSchema(BaseModel):
    type: str
    name: str
    namespace: str
    fields_: List[TopicSchemaField] = Field(alias="fields")
