from typing import List, NewType, Optional, Any
from uuid import UUID

from pydantic import BaseModel, Field
from pydantic.dataclasses import dataclass

from kamui.core.entity.source import SourceType


@dataclass
class Stream:
    stream_id: UUID
    name: str
    source_type: SourceType
    source_name: str


@dataclass
class KSQLStream:
    type: str
    name: str
    format: str


class KSQLStreamDetailed(BaseModel):
    class KSQLStreamField(BaseModel):
        class KSQLStreamFieldSchema(BaseModel):
            type: str
            fields_: Optional[Any] = Field(default=None, alias="fields")

        name: str
        schema_: KSQLStreamFieldSchema = Field(alias="schema")

    name: str
    fields_: List[KSQLStreamField] = Field(alias="fields")
    type: str
    format: str
    topic: str


StreamList = NewType("StreamList", List[Stream])
