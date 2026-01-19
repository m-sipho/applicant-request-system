from fastapi.testclient import TestClient
from app.main import app
import os
from app.models import User
import pytest

client = TestClient(app)

# The real success state
def test_create_admin_success(client, db_session):
    # Ensure the database is empty
    db_session.query(User).delete()
    db_session.commit()

    with pytest.MonkeyPatch.context() as m:
        m.setenv("ADMIN_SECRET", "test-secret")

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