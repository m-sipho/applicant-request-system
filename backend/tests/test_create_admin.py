from fastapi.testclient import TestClient
from app.main import app
import os

client = TestClient(app)

def test_create_admin_success(client):
    os.environ["ADMIN_SECRET"] = "test-secret"

    response = client.post(
        "/bootstrap/admin",
        params={"secret": "test-secret"},
        json={
            "name": "Admin",
            "email": "admin@example.com",
            "password": "strongpassword"
        }
    )

    assert response.status_code == 200
    assert response.json() == {"message": "Admin created"}