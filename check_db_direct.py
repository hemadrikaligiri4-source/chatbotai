import sqlite3
import os

db_path = os.path.join(os.getcwd(), 'instance', 'hemadri.db')
print(f"Checking database at: {db_path}")

if not os.path.exists(db_path):
    print("Database file does not exist!")
else:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print(f"Tables: {tables}")
        
        if ('user',) in tables:
            cursor.execute("SELECT id, email, is_verified FROM user;")
            users = cursor.fetchall()
            print(f"{'ID':<5} | {'Email':<30} | {'Verified'}")
            print("-" * 50)
            for user in users:
                print(f"{user[0]:<5} | {user[1]:<30} | {user[2]}")
        else:
            print("User table not found!")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()
