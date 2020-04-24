from dataclasses import dataclass
from typing import List, NewType
from uuid import UUID


@dataclass
class Stream:
    stream_id: UUID
    name: str
    project_id: UUID


StreamList = NewType("StreamList", List[Stream])
