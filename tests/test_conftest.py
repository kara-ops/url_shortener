from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest
from unittest.mock import patch,MagicMock
from app.database.postgres import Base,get_db
from app.main import app
from fastapi.testclient import TestClient
from app.models.user_model import User
from app.core.security import create_access_token



TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(TEST_DATABASE_URL)
Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(bind=engine)

@pytest.fixture
def test_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def client(test_db):
    app.dependency_overrides[get_db] = lambda: test_db
    yield TestClient(app)
    app.dependency_overrides.clear()

@pytest.fixture
def auth_headers(test_db):
    user = User(
        email="testemail",
        name="testname",
        google_id="fakeidtest"
    )
    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)

    token = create_access_token(user.id)

    return {"Authorization": f"Bearer {token}"}
