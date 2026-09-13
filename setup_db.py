import psycopg
from db import DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME

def setup():
    try:
        # Step 1: Connect to maintenance db to create target database if needed
        conn_init = psycopg.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            dbname='postgres',
            autocommit=True
        )
        cur_init = conn_init.cursor()
        cur_init.execute("SELECT 1 FROM pg_database WHERE datname = %s", (DB_NAME,))
        if not cur_init.fetchone():
            cur_init.execute(f'CREATE DATABASE "{DB_NAME}"')
            print(f"Created PostgreSQL database '{DB_NAME}'.")
        else:
            print(f"PostgreSQL database '{DB_NAME}' already exists.")
        cur_init.close()
        conn_init.close()

        # Step 2: Connect to the inventory database and create tables
        connection = psycopg.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            dbname=DB_NAME,
            autocommit=False
        )
        cursor = connection.cursor()

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS employee_data (
            empid INT PRIMARY KEY,
            name VARCHAR(75),
            farmrole VARCHAR(100),
            gender VARCHAR(15),
            dob VARCHAR(10),
            contact VARCHAR(20),
            employement_type VARCHAR(50),
            education VARCHAR(40),
            work_shift VARCHAR(50),
            address VARCHAR(100),
            doj VARCHAR(30),
            salary NUMERIC(10,2),
            usertype VARCHAR(30),
            maincrop VARCHAR(100)
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_signin_details (
            id SERIAL PRIMARY KEY,
            email VARCHAR(100),
            username VARCHAR(70),
            password VARCHAR(40)
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS supplier_data (
            invoice INT PRIMARY KEY, 
            name VARCHAR(50), 
            contact VARCHAR(15), 
            address VARCHAR(100), 
            description TEXT
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS product_data (
            id SERIAL PRIMARY KEY, 
            category VARCHAR(100), 
            supplier VARCHAR(100), 
            name VARCHAR(100), 
            price NUMERIC(12,2), 
            quantity INT, 
            status VARCHAR(50)
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS category_data (
            id INT PRIMARY KEY, 
            name VARCHAR(50), 
            description TEXT
        )
        """)

        cursor.execute("SELECT 1 FROM user_signin_details WHERE username = 'admin'")
        if not cursor.fetchone():
            cursor.execute("INSERT INTO user_signin_details (email, username, password) VALUES ('admin@growpilot.com', 'admin', 'admin')")
            print("Default admin user created ('admin' / 'admin').")

        connection.commit()
        print("Database setup complete. All PostgreSQL tables verified successfully.")
    except Exception as e:
        print("Error during setup:", e)
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()

if __name__ == "__main__":
    setup()
