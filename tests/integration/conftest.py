import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers
from src.core.database import Base

@pytest.fixture(scope="session")
def engine():
    # Use in-memory SQLite for fast, isolated tests
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)
    clear_mappers()

@pytest.fixture(scope="function")
def db_session(engine):
    """Provides a SQLAlchemy session bound to the test engine."""
    connection = engine.connect()
    transaction = connection.begin()
    Session = sessionmaker(bind=connection)
    session = Session()
    yield session
    session.close()
    transaction.rollback()
    connection.close() 