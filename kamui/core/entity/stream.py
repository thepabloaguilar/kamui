from dataclasses import dataclass
from uuid import UUID


@dataclass
class Stream:
    stream_id: UUID
    name: str
    project_id: UUID
