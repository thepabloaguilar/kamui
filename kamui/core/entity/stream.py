from dataclasses import dataclass
from typing import List, NewType, Optional, Any
from uuid import UUID

from dataclasses_json import dataclass_json

from kamui.core.entity.source import SourceType


@dataclass_json
@dataclass
class Stream:
    stream_id: UUID
    name: str
    source_type: SourceType
    source_name: str


@dataclass_json
@dataclass
class KSQLStream:
    type: str
    name: str
    format: str


@dataclass_json
@dataclass
class KSQLStreamDetailed:
    @dataclass_json
    @dataclass
    class KSQLStreamField:
        @dataclass_json
        @dataclass
        class KSQLStreamFieldSchema:
            type: str
            fields: Optional[Any]

        name: str
        schema: KSQLStreamFieldSchema

    name: str
    fields: List[KSQLStreamField]
    type: str
    format: str
    topic: str


StreamList = NewType("StreamList", List[Stream])
