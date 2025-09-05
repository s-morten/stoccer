import os
import oracledb
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# --- Oracle Client Initialization ---
# This is the correct place to specify the config directory for tnsnames.ora, etc.
# --- Database Configuration ---
DB_USER = os.environ.get("DB_USER", "ADMIN")
DB_PASSWORD = os.environ.get("DB_PASSWORD", "your_password")
DB_DSN = os.environ.get("DB_DSN", "most") # e.g., "localhost:1521/orcl"

# SQLAlchemy connection string for Oracle
DATABASE_URL = f"oracle+oracledb://{DB_USER}:{DB_PASSWORD}@{DB_DSN}"

# --- SQLAlchemy Engine and Session ---
try:
    # The config_dir argument is removed from here
    print(DB_USER)
    print(DB_PASSWORD)
    connection = oracledb.connect(user=DB_USER, password=DB_PASSWORD,
                            dsn=DB_DSN, config_dir="/etc/")

    engine = create_engine('oracle+oracledb://', creator=lambda: connection)
        
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
except Exception as e:
    print(f"Error creating SQLAlchemy engine: {e}")
    engine = None
    SessionLocal = None

Base = declarative_base()

def get_db():
    """Dependency to get a DB session."""
    if SessionLocal is None:
        print("Database session is not configured.")
        return
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
