from sqlalchemy import Column, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

from kamui.configuration.database import DatabaseBase


class StreamProjectModel(DatabaseBase):
    __tablename__ = "stream_project"

    project_id = Column(
        "project_id", ForeignKey("project.project_id"), primary_key=True
    )
    stream_id = Column("stream_id", ForeignKey("stream.stream_id"), primary_key=True)
    created_at = Column("created_at", DateTime(timezone=True), default=func.now())

    project = relationship("ProjectModel", back_populates="streams")
    stream = relationship("StreamModel", back_populates="projects")
