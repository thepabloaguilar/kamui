from uuid import uuid4

from sqlalchemy import Column, String, DateTime, Enum, func
from sqlalchemy.dialects.postgresql import UUID

from kamui.configuration.database import DatabaseBase
from kamui.core.entity.project import Project
from kamui.core.entity.project_status import ProjectStatus


class ProjectModel(DatabaseBase):
    __tablename__ = "project"

    project_id = Column(
        "project_id", UUID(as_uuid=True), default=uuid4, primary_key=True
    )
    title = Column("title", String(20))
    created_at = Column("created_at", DateTime(timezone=True), default=func.now())
    status = Column("status", Enum(ProjectStatus), default=ProjectStatus.ACTIVE)

    def to_entity(self) -> Project:
        return Project(
            project_id=self.project_id,
            title=self.title,
            created_at=self.created_at,
            status=self.status,
        )
