import pytest
from sqlmodel import SQLModel
from main import engine

@pytest.fixture(scope="function", autouse=True)
def clean_db():
    """Resets database before each test"""
    SQLModel.metadata.drop_all(engine)
    SQLModel.metadata.create_all(engine)
