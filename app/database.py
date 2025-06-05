# app/database.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.settings import settings

# 1) Create the SQLAlchemy engine using the DATABASE_URL from .env
engine = create_engine(
    settings.DATABASE_URL,
    echo=False,         # Set True if you want to see all SQL statements
    pool_pre_ping=True, # Checks connections before using them
    pool_size=5,
    max_overflow=10,
)

# 2) Create a configured "SessionLocal" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 3) Base class for our ORM models
Base = declarative_base()

# 4) Dependency for FastAPI endpoints to get a DB session
def get_db():
    """
    Yield a database session, and close it after the request.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
