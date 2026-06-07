from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from app.config.settings import settings

# PostgreSQL DATABASE URL
DATABASE_URL = settings.DATABASE_URL

# Create Engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)

# Session
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base Model
Base = declarative_base()
