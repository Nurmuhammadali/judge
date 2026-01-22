import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from apps.infrastructure.db.base import Base
from apps.infrastructure.db.models.submission import SubmissionModel
from apps.infrastructure.db.models.testcase import TestCaseModel


DATABASE_URL = "postgresql+psycopg2://judge:judge@localhost:5433/judge_test"


@pytest.fixture(scope="session")
def engine():
    engine = create_engine(DATABASE_URL)
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def db(engine):
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()
    yield session
    session.rollback()
    session.close()
