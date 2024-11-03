import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

@pytest.fixture
def valid_user():
    return {"username": "tanzila", "password": "tanzila"}

@pytest.fixture
def auth_header(valid_user):
    login_response = client.post("/token", data=valid_user)
    print("Login response:", login_response.json())  
    assert login_response.status_code == 200, "Failed to log in with valid credentials"
    token = login_response.json().get("access_token")
    assert token is not None, "Failed to get access token for valid user"
    return {"Authorization": f"Bearer {token}"}

def test_get_all_employees(auth_header):
    """Test retrieving all employees."""
    response = client.get("/api/employees/", headers=auth_header)
    print("Get all employees response:", response.status_code, response.json())  
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_employee(auth_header):
    """Test creating a new employee."""
    new_employee = {
        "name": "tanzila",
        "email": "ikhlaq@example.com",  
        "department": "IT",
        "role": "Developer"
    }

    response = client.post("/api/employees/", json=new_employee, headers=auth_header)

    # Assert the status code first
    assert response.status_code in [200, 400], f"Unexpected status code: {response.status_code}"

    # Handle successful response
    if response.status_code == 200:
        assert response.json() == {"message": "Employee added successfully!"}
    # Handle failure due to existing email
    elif response.status_code == 400:
        assert response.json().get("detail") == "Email already exists", \
            f"Expected 'Email already exists' but got {response.json().get('detail')}"

def test_get_employee_by_id(auth_header):
    """Test retrieving a specific employee by ID."""
    response = client.get("/api/employees/1/", headers=auth_header)
    #print("Get employee by ID response:", response.status_code, response.json())  
    if response.status_code == 200:
        data = response.json()
        assert "id" in data
        assert data["id"] == 1
    else:
        assert response.status_code == 404

def test_update_employee(auth_header):
    """Test updating an employee's information."""
    update_data = {
        "name": "John Doe Updated",
        "email": "johndoe@example.com",
        "department": "IT",
        "role": "Senior Developer"
    }
    response = client.put("/api/employees/1/", json=update_data, headers=auth_header)
    #print("Update employee response:", response.status_code, response.json()) 
    if response.status_code == 200:
        assert response.json() == {"message": "Employee updated successfully!"}
    else:
        assert response.status_code == 404

def test_delete_employee(auth_header):
    """Test deleting an employee."""
    response = client.delete("/api/employees/1/", headers=auth_header)
    #print("Delete employee response:", response.status_code, response.json())  
    if response.status_code == 204:
        assert response.json() == {"message": "Employee deleted successfully!"}
    else:
        assert response.status_code == 404
