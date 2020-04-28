from dataclasses import dataclass
from typing import List, NewType
from uuid import UUID

from dataclasses_json import dataclass_json


@dataclass
class Stream:
    stream_id: UUID
    name: str
    project_id: UUID


@dataclass_json
@dataclass
class KSQLStream:
    type: str
    name: str
    format: str


StreamList = NewType("StreamList", List[Stream])
