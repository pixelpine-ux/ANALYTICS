from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from .config import settings
import os

# Performance-optimized engine configuration
engine_kwargs = {
    "echo": os.getenv("DEBUG") == "true",  # Log SQL queries in debug mode
}

# SQLite-specific optimizations
if "sqlite" in settings.database_url:
    engine_kwargs.update({
        "connect_args": {
            "check_same_thread": False,
            "timeout": 20,  # Prevent database locks
        },
        "poolclass": StaticPool,
        "pool_pre_ping": True,  # Verify connections before use
    })
else:
    # PostgreSQL optimizations
    engine_kwargs.update({
        "pool_size": 10,  # Connection pool size
        "max_overflow": 20,  # Additional connections when needed
        "pool_pre_ping": True,
        "pool_recycle": 3600,  # Recycle connections every hour
    })

engine = create_engine(settings.database_url, **engine_kwargs)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()