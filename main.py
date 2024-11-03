from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from auth import authenticate_user, create_access_token,get_current_active_user,ACCESS_TOKEN_EXPIRE_MINUTES,fake_data
from datetime import timedelta
from crud import read_employees, post_details, get_user_by_id, update_action, delete_action
from models import Employee, EmployeeQueryParams,Token,User

app = FastAPI()

# Token endpoint
@app.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_data, form_data.username, form_data.password)
    if not user:
        print(f"Failed login attempt for user: {form_data.username}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    print(f"User {user['username']} authenticated successfully.")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user["username"]}, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}

# CRUD endpoints for Employee model
@app.get("/api/employees/", dependencies=[Depends(get_current_active_user)])
def get_all_employees(params: EmployeeQueryParams = Depends()):
    employees = read_employees(params)
    if employees is None:
        raise HTTPException(status_code=500, detail="Error retrieving employees")
    return employees

@app.post("/api/employees/",dependencies=[Depends(get_current_active_user)])
def create_employee(employee: Employee):
    response = post_details(employee)
    return response

@app.get("/api/employees/{id}/",dependencies=[Depends(get_current_active_user)])
def read_employee_by_id(id: int):
    employee = get_user_by_id(id)
    return employee

@app.put("/api/employees/{id}/",dependencies=[Depends(get_current_active_user)])
def modify_employee(id: int, employee: Employee):
    response = update_action(id, employee)
    return response

@app.delete("/api/employees/{id}/",dependencies=[Depends(get_current_active_user)])
def remove_employee(id: int):
    response = delete_action(id)
    return response
