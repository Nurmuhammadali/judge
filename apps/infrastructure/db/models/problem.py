from sqlalchemy import Column, DateTime, Integer, String, Text
from sqlalchemy.sql import func

from apps.infrastructure.db.base import Base


class ProblemModel(Base):
    __tablename__ = "problems"

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=False)

    input_description = Column(Text, nullable=False)
    output_description = Column(Text, nullable=False)

    constraints = Column(Text, nullable=True)

    time_limit_sec = Column(Integer, nullable=False, default=2)
    memory_limit_mb = Column(Integer, nullable=False, default=256)

    created_at = Column(DateTime, server_default=func.now())
