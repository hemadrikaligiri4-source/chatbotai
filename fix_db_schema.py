import sqlite3
import os

db_path = os.path.join(os.getcwd(), 'instance', 'hemadri.db')
print(f"Migrating database at: {db_path}")

if not os.path.exists(db_path):
    print("Database file does not exist!")
else:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        # Check columns
        cursor.execute("PRAGMA table_info(user)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'is_verified' not in columns:
            print("Adding is_verified column...")
            cursor.execute("ALTER TABLE user ADD COLUMN is_verified BOOLEAN DEFAULT 0")
            conn.commit()
            print("Column added successfully.")
        else:
            print("Column is_verified already exists.")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        conn.close()
