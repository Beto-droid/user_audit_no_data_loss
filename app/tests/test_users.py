from app.tests.conftest import client


def test_read_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to User Profile Audit"}


def test_create_user_id_1(client):
    response = client.post(
        "/users/", json={"name": "Test Name 1", "email": "testmail1@testmail.com"}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == "Test Name 1"
    assert data["email"] == "testmail1@testmail.com"


def test_get_client_by_id(client):
    response = client.get("/users/1")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "Test Name 1"
    assert data["email"] == "testmail1@testmail.com"


def test_get_client_by_id_no_user(client):
    response = client.get("/users/2")
    assert response.status_code == 404
    assert response.json() == {
        "detail": "The user with this id does not exist in the system"
    }


def test_create_user_id_2(client):
    response = client.post(
        "/users/", json={"name": "Test Name 2", "email": "testmail2@testmail.com"}
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == "Test Name 2"
    assert data["email"] == "testmail2@testmail.com"


def test_update_user_id_2(client):
    response = client.put(
        "/users/2?name=Test Name update&email=testmailupdated@testmail.com"
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == "Test Name update"
    assert data["email"] == "testmailupdated@testmail.com"


def test_delete_user_id_2(client):
    response = client.delete("/users/2")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["deleted_user"] == {
        "id": 2,
        "name": "Test Name update",
        "email": "testmailupdated@testmail.com",
    }
