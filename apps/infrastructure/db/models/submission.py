from sqlalchemy import Column, DateTime, Enum, Integer, String, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from apps.domain.enums.judge_status import JudgeStatus
from apps.infrastructure.db.base import Base


class SubmissionModel(Base):
    __tablename__ = "submissions"

    id = Column(UUID(as_uuid=True), primary_key=True)
    problem_id = Column(
        Integer,
        ForeignKey("problems.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    problem = relationship(
        "ProblemModel",
        backref="submissions",
    )
    language = Column(String(32), nullable=False)
    source_code = Column(Text, nullable=False)
    status = Column(Enum(JudgeStatus), nullable=False)

    execution_time_ms = Column(Integer, nullable=True)
    output = Column(Text, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    rejudge_count = Column(Integer, nullable=False, default=0)
    judged_at = Column(DateTime(timezone=True), nullable=True)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
