import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

@pytest.fixture
def valid_user():
    return {"username": "tanzila", "password": "tanzila"}

@pytest.fixture
def invalid_user():
    return {"username": "unknown", "password": "wrongpassword"}

def test_login_valid_user(valid_user):
    response = client.post("/token", data=valid_user)
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_invalid_user(invalid_user):
    response = client.post("/token", data=invalid_user)
    assert response.status_code == 401
    assert response.json() == {"detail": "Incorrect username or password"}

def test_access_protected_endpoint(valid_user):
    # Login to get access token
    login_response = client.post("/token", data=valid_user)
    token = login_response.json()["access_token"]

    # Use token to access a protected endpoint
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/api/employees/", headers=headers)
    assert response.status_code == 200
