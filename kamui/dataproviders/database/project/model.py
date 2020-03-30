from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime, Enum, func

from kamui.configuration.database import DatabaseBase
from kamui.core.entity.project import Project
from kamui.core.entity.project_status import ProjectStatus


class ProjectModel(DatabaseBase):
    __tablename__ = "project"

    id = Column("id", Integer, primary_key=True)
    title = Column("title", String(20))
    created_at = Column("created_at", DateTime(timezone=True), default=func.now())
    status = Column("status", Enum(ProjectStatus), default=ProjectStatus.ACTIVE)

    def to_entity(self) -> Project:
        return Project(
            id=self.id,
            title=self.title,
            created_at=self.created_at,
            status=self.status,
        )
