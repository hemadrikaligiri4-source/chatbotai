import sqlite3
import os

db_path = os.path.join(os.getcwd(), 'instance', 'hemadri.db')
print(f"Verifying users in database at: {db_path}")

if not os.path.exists(db_path):
    print("Database file does not exist!")
else:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE user SET is_verified = 1")
        conn.commit()
        print(f"Successfully verified {cursor.rowcount} users.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()
