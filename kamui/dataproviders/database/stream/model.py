from uuid import uuid4

from sqlalchemy import Column, String, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from kamui.configuration.database import DatabaseBase
from kamui.core.entity.source import SourceType
from kamui.core.entity.stream import Stream


class StreamModel(DatabaseBase):
    __tablename__ = "stream"

    stream_id = Column("stream_id", UUID(as_uuid=True), default=uuid4, primary_key=True)
    name = Column("name", String(50), nullable=False)
    source_type = Column("source_type", Enum(SourceType))
    source_name = Column("source_name", String(50))
    project_id = Column(
        "project_id", UUID(as_uuid=True), ForeignKey("project.project_id")
    )

    project = relationship("ProjectModel", back_populates="streams")

    def to_entity(self) -> Stream:
        return Stream(
            stream_id=self.stream_id,
            name=self.name,
            source_type=self.source_type,
            source_name=self.source_name,
            project_id=self.project_id,
        )
