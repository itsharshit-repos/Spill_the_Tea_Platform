from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://ai_backend:admin123@localhost:5432/ai_system_dev"

# Engine: The connection pool
engine = create_engine(SQLALCHEMY_DATABASE_URL)

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