from app.database import get_session, engine
from app.models.task_models import User
from sqlmodel import select
from app.auth import get_password_hash
import uuid
from datetime import datetime, timezone

def test_database():
    print("Testing database connection...")
    
    # Generate a unique email
    unique_email = f"test_{uuid.uuid4()}@example.com"
    
    # Get a session
    session_gen = get_session()
    session = next(session_gen)
    
    try:
        # Try to create a test user directly
        print("Creating test user...")
        test_user = User(
            id=str(uuid.uuid4()),
            email=unique_email,  # Use unique email
            password=get_password_hash("password123"),
            name="Test User",
            created_at=datetime.now(timezone.utc)
        )
        
        session.add(test_user)
        session.commit()
        session.refresh(test_user)
        
        print(f"User created successfully with ID: {test_user.id}")
        
        # Query the user back
        retrieved_user = session.exec(select(User).where(User.email == unique_email)).first()
        if retrieved_user:
            print(f"User retrieved successfully: {retrieved_user.name}")
        else:
            print("Failed to retrieve user")
            
        # Clean up - delete the test user
        session.delete(retrieved_user)
        session.commit()
        print("Test user deleted")
        
    except Exception as e:
        print(f"Database test failed: {e}")
        import traceback
        traceback.print_exc()
    finally:
        session.close()

if __name__ == "__main__":
    test_database()