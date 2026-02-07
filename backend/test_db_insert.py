import sqlite3
import traceback
from app.auth import get_password_hash
from app.database import engine
from app.models.task_models import User
from sqlmodel import Session, select

def test_db_insert():
    try:
        print("Testing database insert...")
        
        # Create a test user
        hashed_password = get_password_hash("password123")
        test_user = User(
            email="test@example.com",
            password=hashed_password,
            name="Test User"
        )
        
        # Insert into database
        with Session(engine) as session:
            session.add(test_user)
            session.commit()
            session.refresh(test_user)
            
        print("User inserted successfully!")
        print(f"User ID: {test_user.id}")
        return True
    except Exception as e:
        print(f"Error inserting user: {e}")
        print(f"Traceback: {traceback.format_exc()}")
        return False

if __name__ == "__main__":
    test_db_insert()