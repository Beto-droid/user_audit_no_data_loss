from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_create_user():
    response = client.post(
        "/users/", json={"id": 1, "name": "User 1", "email": "user@user.com"}
    )
    assert response.status_code == 200
    assert response.json()["name"] == "User 1"
