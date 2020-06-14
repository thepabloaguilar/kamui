from uuid import UUID
from datetime import datetime
from dataclasses import field

from pydantic.dataclasses import dataclass

from .project_status import ProjectStatus


@dataclass
class Project:
    project_id: UUID
    title: str
    created_at: datetime
    status: ProjectStatus = field(default=ProjectStatus.ACTIVE)
