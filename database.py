# Database connection
import mysql.connector
from mysql.connector import Error
import dotenv,os

dotenv.load_dotenv()

password=os.getenv("PASSWORD")

def connection():
    try:
        connection=mysql.connector.connect(
            host='localhost',
            user='root',
            password=password,
            database='emp_crm'
        )
        print("Connection to db successful!")
    except Error as e:
        print(f"Error connecting to db: {e}")

    return connection

if __name__=="__main__":
    connection()