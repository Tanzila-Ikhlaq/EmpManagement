from mysql.connector import Error
from database import connection
from models import Employee,EmployeeQueryParams
from fastapi import HTTPException, status
from typing import List, Dict, Any

def read_employees(params: EmployeeQueryParams) -> List[Dict[str, Any]]:
    try:
        mydb = connection()
        mycursor = mydb.cursor()

        # Base query
        query = "SELECT * FROM employee"
        conditions = []
        values = []

        # filtering conditions
        if params.department:
            conditions.append("department = %s")
            values.append(params.department)
        if params.role:
            conditions.append("role = %s")
            values.append(params.role)

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        # Pagination
        offset = (params.page - 1) * params.limit
        query += " LIMIT %s OFFSET %s"
        values.append(params.limit)
        values.append(offset)

        # query execution
        mycursor.execute(query, tuple(values))
        myresult = mycursor.fetchall()

        column_names = [i[0] for i in mycursor.description]
        result_list = [dict(zip(column_names, row)) for row in myresult]

        return result_list
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    
    finally:
        if mydb:
            mydb.close()

def post_details(employee: Employee):
    try:
        mydb = connection()
        mycursor = mydb.cursor()

        # Check if email already exists
        mycursor.execute("SELECT * FROM employee WHERE email = %s", (employee.email,))
        existing_employee = mycursor.fetchone()
        if existing_employee:
            raise HTTPException(status_code=400, detail="Email already exists")

        query = "INSERT INTO employee (name, email, department, role) VALUES (%s, %s, %s, %s)"
        val = (employee.name, employee.email, employee.department, employee.role)
        mycursor.execute(query, val)
        mydb.commit()

        return {"message": "Employee added successfully!"}, status.HTTP_201_CREATED
    
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Error: {e}")
    
    finally:
        mydb.close()

def get_user_by_id(id: int):
    try:
        mydb = connection()
        mycursor = mydb.cursor()
        query = "SELECT * FROM employee WHERE id = %s"
        val = (id,)
        mycursor.execute(query, val)
        myresult = mycursor.fetchone()

        if not myresult:
            raise HTTPException(status_code=404, detail="Employee not found")
        
        return myresult  
    
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Error: {e}")
    
    finally:
        mydb.close()

def update_action(id: int, employee: Employee):
    try:
        mydb = connection()
        mycursor = mydb.cursor()
        query = """
            UPDATE employee
            SET name = %s, email = %s, department = %s, role = %s
            WHERE id = %s
        """
        val = (employee.name, employee.email, employee.department, employee.role, id)
        mycursor.execute(query, val)
        mydb.commit()

        if mycursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Employee not found")
        
        return {"message": "Employee updated successfully!"}
    
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Error: {e}")
    
    finally:
        mydb.close()

def delete_action(id: int):
    try:
        mydb = connection()
        mycursor = mydb.cursor()
        query = "DELETE FROM employee WHERE id = %s"
        val = (id,)
        mycursor.execute(query, val)
        mydb.commit()

        if mycursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Employee not found")
        
        return {"message": "Employee deleted successfully!"}, status.HTTP_204_NO_CONTENT
    
    except Error as e:
        raise HTTPException(status_code=500, detail=f"Error: {e}")
    
    finally:
        mydb.close()
