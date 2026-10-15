from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config import settings

# Engine: The connection pool
engine = create_engine(settings.database_url)

# Session: The temporary workspace for transaction
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Declarative base: The parent class for our database models
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()