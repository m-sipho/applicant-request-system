from fastapi.testclient import TestClient
from app.main import app
import os
import pytest

client = TestClient(app)

def test_create_applicant_success(client):
    payload = {
        "name": "Mthokozisi",
        "email": "mth@gmail.com",
        "password": "MthoSipho"
    }

    response = client.post("/register", json=payload)

    assert response.status_code == 201
    data = response.json()

    assert "id" in data
    assert data["email"] == payload["email"]
    assert "password" not in data


@pytest.mark.parametrize("payload, expected_status", [
    # Missing email
    ({"name": "Mtho", "password": "password"}, 422),
    # Invalid email format
    ({"name": "Mtho", "email": "not-an-email", "password": "password"}, 422),
    # Missing password
    ({"name": "Mtho", "email": "valid@test.com"}, 422)
])
def test_create_applicant_validation_errors(client, payload, expected_status):
    response = client.post("/register", json=payload)
    assert response.status_code == expected_status