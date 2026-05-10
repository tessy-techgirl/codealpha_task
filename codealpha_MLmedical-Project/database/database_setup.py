import mysql.connector

def init_db():
    db = mysql.connector.connect(host="localhost", user="root", password="_T57ERESA-22F")
    cursor = db.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS medical_system")
    cursor.execute("USE medical_system")
    
    # Table for user login
    cursor.execute("CREATE TABLE IF NOT EXISTS users (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(50), password VARCHAR(50))")
    
    # Table for saving patient diagnosis history
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INT AUTO_INCREMENT PRIMARY KEY, 
            username VARCHAR(50), 
            disease VARCHAR(50), 
            result VARCHAR(50), 
            date DATETIME
        )
    """)
    db.commit()
    print("Database Ready.")

if __name__ == "__main__":
    init_db()