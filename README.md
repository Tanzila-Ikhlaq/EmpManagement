# EmpManagement

**EmpManagement** is a FastAPI-based employee management system that provides a RESTful API for managing employee records with a focus on simplicity and efficiency. This project features user authentication using OAuth2 and JWT tokens, allowing secure access to CRUD operations for employee data.

## Key Features:
- **User Authentication**: Secure login and token generation using OAuth2.
- **CRUD Operations**: Create, read, update, and delete employee records easily.
- **Filtering and Pagination**: Retrieve employee data based on various parameters.
- **Error Handling**: Robust error management for a smooth user experience.
- **MySQL Integration**: Uses MySQL for reliable data storage.
- **Test Cases**: Includes test cases for endpoint verification to ensure the functionality and reliability of the API.

## Technologies Used

- [FastAPI](https://fastapi.tiangolo.com/) - Web framework for building APIs.
- [MySQL](https://www.mysql.com/) - Database for storing employee data.
- [Python](https://www.python.org/) - Programming language.
- [Pydantic](https://pydantic-docs.helpmanual.io/) - Data validation and settings management.
- [JWT (JSON Web Tokens)](https://jwt.io/) - For secure token generation and validation.

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Tanzila-Ikhlaq/EmpManagement.git
   cd EmpManagement
   ```

3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

4. Set up your database.

5. Run the application:
   ```bash
   uvicorn app:app --reload
   ```

   The API will be available at `http://127.0.0.1:8000`.

### API Endpoints

#### Token Endpoint

- **POST** `/token`
  - Request: 
    - `username`: User's username
    - `password`: User's password
  - Response: 
    - `access_token`: JWT token
    - `token_type`: Bearer

#### Employee Endpoints

- **GET** `/api/employees/`
  - Fetch all employees (requires authentication).
  - Query parameters:
    - `department`: Filter by department
    - `role`: Filter by role
    - `page`: Page number for pagination
    - `limit`: Number of records per page

- **POST** `/api/employees/`
  - Create a new employee (requires authentication).
  - Request body:
    ```json
    {
      "name": "tanzila",
      "email": "ikhlaq@example.com",
      "department": "IT",
      "role": "Developer"
    }
    ```

- **GET** `/api/employees/{id}/`
  - Retrieve an employee by ID (requires authentication).

- **PUT** `/api/employees/{id}/`
  - Update an existing employee (requires authentication).
  - Request body: Same as POST.

- **DELETE** `/api/employees/{id}/`
  - Delete an employee by ID (requires authentication).

### Testing

The project includes test cases to verify the functionality of the API endpoints. Tests are written using `pytest` and can be executed to ensure that all endpoints are working as expected.

You can use tools like [Postman](https://www.postman.com/) or `curl` to test the API endpoints. 
