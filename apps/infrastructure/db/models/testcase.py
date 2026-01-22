from sqlalchemy import Boolean, Column, ForeignKey, Integer, Text
from sqlalchemy.orm import relationship

from apps.infrastructure.db.base import Base


class TestCaseModel(Base):
    __tablename__ = "test_cases"

    id = Column(Integer, primary_key=True)
    problem_id = Column(
        Integer,
        ForeignKey("problems.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    problem = relationship(
        "ProblemModel",
        backref="testcases",
    )

    input_data = Column(Text, nullable=False)
    expected_output = Column(Text, nullable=False)

    is_sample = Column(Boolean, default=False)
