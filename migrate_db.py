import sqlite3
import os

db_path = 'c:/Users/Suneel Reddy/Downloads/aichatbot/hemadri.db'

if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    try:
        # Check if column exists
        cursor.execute("PRAGMA table_info(user)")
        columns = [column[1] for column in cursor.fetchall()]
        if 'is_verified' not in columns:
            print("Adding is_verified column to user table...")
            cursor.execute("ALTER TABLE user ADD COLUMN is_verified BOOLEAN DEFAULT 0")
            conn.commit()
            print("Migration successful.")
        else:
            print("Column is_verified already exists.")
    except Exception as e:
        print(f"Migration failed: {e}")
    finally:
        conn.close()
else:
    print("Database file not found. create_all() will handle it.")
