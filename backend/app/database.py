from sqlmodel import create_engine, Session
from typing import Generator
import os
from contextlib import contextmanager
import urllib.parse
from sqlalchemy import text

# Get database URL from environment variable
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todo_app.db")

# Handle special characters in DATABASE_URL for PostgreSQL
if DATABASE_URL.startswith("postgresql://"):
    # Parse the URL and handle special characters
    parsed = urllib.parse.urlparse(DATABASE_URL)
    # Reconstruct with proper quoting
    DATABASE_URL = f"postgresql://{parsed.username}:{urllib.parse.quote_plus(parsed.password)}@{parsed.hostname}:{parsed.port}{parsed.path}"
elif DATABASE_URL.startswith("psql 'postgresql://"):
    # Handle the specific format in the .env file
    DATABASE_URL = DATABASE_URL.replace("psql '", "").rstrip("'")
elif DATABASE_URL == "sqlite:///./todo_app.db":
    # Use absolute path to ensure consistent database access
    import os
    db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "todo_app.db"))
    DATABASE_URL = f"sqlite:///{db_path}"

# Create engine with connection pooling settings
# Always use the same database URL consistently
if "sqlite" in DATABASE_URL:
    # Enable foreign key constraints for SQLite
    engine = create_engine(
        DATABASE_URL,
        echo=False,           # Set to True for debugging SQL queries
        pool_pre_ping=True,   # Verify connections before use
        connect_args={
            "check_same_thread": False,
            "uri": True  # This enables PRAGMA settings for SQLite
        }
    )
    # Enable foreign keys after engine creation
    with engine.connect() as conn:
        conn.execute(text("PRAGMA foreign_keys=ON"))
else:
    engine = create_engine(
        DATABASE_URL,
        echo=False,           # Set to True for debugging SQL queries
        pool_pre_ping=True,   # Verify connections before use
        connect_args={} if "sqlite" not in DATABASE_URL else {"check_same_thread": False}
    )


def get_session() -> Generator[Session, None, None]:
    """Dependency to get DB session"""
    with Session(engine) as session:
        yield session


# Function to create tables
def create_tables():
    """Create all tables in the database"""
    from sqlmodel import SQLModel
    from .models.task_models import User, Task, Conversation, Message

    # Import all models here to register them with SQLModel
    try:
        SQLModel.metadata.create_all(bind=engine)
        print("Database tables created successfully")
    except Exception as e:
        print(f"Error creating database tables: {e}")
        # If PostgreSQL fails, try creating SQLite tables
        if "sqlite" not in str(DATABASE_URL):
            sqlite_url = "sqlite:///./todo_app.db"
            sqlite_engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})
            SQLModel.metadata.create_all(bind=sqlite_engine)
            print("Created SQLite tables as fallback")