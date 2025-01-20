from app.tests.conftest import client


def test_create_user_and_verify_audit_logs(client):
    response = client.post(
        "/users/", json={"name": "Audit Test User", "email": "audittestuser@example.com"}
    )
    assert response.status_code == 200
    created_user = response.json()

    audit_response = client.get(f"/audit/?user_id={created_user['id']}")
    assert audit_response.status_code == 200
    audit_logs = audit_response.json()
    assert len(audit_logs) == 1
    assert audit_logs[0]["change_type"] == "created"


def test_user_crud_and_audit(client):
    response = client.post(
        "/users/", json={"name": "Test User", "email": "testuser@example.com"}
    )
    assert response.status_code == 200
    created_user = response.json()

    audit_response = client.get(f"/audit/?user_id={created_user['id']}")
    assert audit_response.status_code == 200
    audit_response_data = audit_response.json()
    assert audit_response_data[0]["change_type"] == "created"
    assert audit_response_data[0]["user_id_record"] == created_user['id']
    assert audit_response_data[0]["user_id"] == created_user['id']
    assert audit_response_data[0]["changed_fields"] == {'new': {'email': 'testuser@example.com', 'name': 'Test User'}, 'old': {}}

    update_response = client.put(
        f"/users/{created_user['id']}?name=Updated Test User&email=updateduser@example.com"
    )
    assert update_response.status_code == 200
    audit_response_json = client.get(f"/audit/?user_id={created_user['id']}").json()[1]["changed_fields"]
    assert audit_response_json == {'old': {'name': 'Test User', 'email': 'testuser@example.com'}, 'new': {'name': 'Updated Test User', 'email': 'updateduser@example.com'}}

    delete_response = client.delete(f"/users/{created_user['id']}")
    assert delete_response.status_code == 200

    audit_response = client.get(f"/audit/?user_id={created_user['id']}")
    assert audit_response.status_code == 404

    audit_response = client.get(f"/audit/?user_id_record={created_user['id']}")
    assert audit_response.status_code == 200
    audit_response_json = audit_response.json()
    assert audit_response_json[3]["id"] == 4
    assert audit_response_json[3]["user_id"] is None
    assert audit_response_json[3]["user_id_record"] == 2
    assert audit_response_json[3]["change_type"] == "deleted"

    assert len(audit_response_json) == 4