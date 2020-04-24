from uuid import uuid4

from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from kamui.configuration.database import DatabaseBase
from kamui.core.entity.stream import Stream


class StreamModel(DatabaseBase):
    __tablename__ = "stream"

    stream_id = Column("stream_id", UUID(as_uuid=True), default=uuid4, primary_key=True)
    name = Column("name", String(50), nullable=False)
    project_id = Column(
        "project_id", UUID(as_uuid=True), ForeignKey("project.project_id")
    )

    project = relationship("ProjectModel", back_populates="streams")

    def to_entity(self) -> Stream:
        return Stream(
            stream_id=self.stream_id, name=self.name, project_id=self.project_id
        )
