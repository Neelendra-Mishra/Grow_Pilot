import pymysql

def setup():
    try:
        connection = pymysql.connect(host='localhost', user='root', password='sqlPrem2025')
        cursor = connection.cursor()
        
        cursor.execute("CREATE DATABASE IF NOT EXISTS inventory")
        cursor.execute("USE inventory")
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Employee_Data (
            empid INT PRIMARY KEY,
            name VARCHAR(75),
            farmrole VARCHAR(100),
            gender VARCHAR(15),
            dob VARCHAR(10),
            contact varchar(20),
            employement_type VARCHAR(50),
            education varchar (40),
            work_shift VARCHAR(50),
            address VARCHAR(100),
            doj VARCHAR(30),
            salary DECIMAL(10,2),
            usertype VARCHAR(30),
            maincrop VARCHAR(100)
        )
        """)
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS User_signin_details (
            id int auto_increment primary key not null,
            email varchar(100),
            username varchar(70),
            password varchar(40)
        )
        """)
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS supplier_data (
            invoice int primary key, 
            name varchar(50), 
            contact varchar(15), 
            address varchar(100), 
            description text
        )
        """)
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS product_data (
            id int auto_increment primary key, 
            category varchar(100), 
            supplier varchar(100), 
            name varchar(100), 
            price decimal(12,2), 
            quantity int, 
            status varchar(50)
        )
        """)
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS category_data (
            id int primary key, 
            name varchar(50),
            description text
        )
        """)
        
        cursor.execute("SELECT * FROM User_signin_details")
        if not cursor.fetchall():
            cursor.execute("INSERT INTO User_signin_details (email, username, password) VALUES ('admin@growpilot.com', 'admin', 'admin')")
            
        connection.commit()
        print("Database setup complete. All tables created. Default user 'admin'/'admin' checked.")
    except Exception as e:
        print("Error during setup:", e)
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()

if __name__ == "__main__":
    setup()
