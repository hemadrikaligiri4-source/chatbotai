from app import app, db, User
import os

with app.app_context():
    print(f"Database URI: {app.config['SQLALCHEMY_DATABASE_URI']}")
    print(f"Instance path: {app.instance_path}")
    
    users = User.query.all()
    if not users:
        print("No users found in the database.")
    else:
        print(f"{'ID':<5} | {'Email':<30} | {'Verified':<10} | {'Created At'}")
        print("-" * 70)
        for user in users:
            print(f"{user.id:<5} | {user.email:<30} | {str(user.is_verified):<10} | {user.created_at}")
