from uuid import UUID
from datetime import datetime
from dataclasses import dataclass, field

from .project_status import ProjectStatus


@dataclass
class Project:
    project_id: UUID
    title: str
    created_at: datetime
    status: ProjectStatus = field(default=ProjectStatus.ACTIVE)
