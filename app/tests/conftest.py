from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest

from app.main import app
from app.db.session import Base, get_db

from app.core.config import settings

TEST_DATABASE_URL = settings.TEST_DATABASE_URL
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="module")
def test_db():
    Base.metadata.create_all(bind=engine)
    yield TestingSessionLocal
    Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="module", autouse=True)
def override_get_db(test_db):
    def _override_get_db():
        db = test_db()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = _override_get_db

@pytest.fixture(scope="module")
def client():
    with TestClient(app) as c:
        yield c