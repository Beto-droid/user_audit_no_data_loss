from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from ..main import app
from app.db.session import Base, get_db
from app.models.user import User as UserModel
from app.schemas.user import User as UserSchema
from app.schemas.user_data_status import Status

from app.core.config import settings

TEST_DATABASE_URL = settings.TEST_DATABASE_URL

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to User Profile Audit"}
