"""
Database connection and session management.

This module provides SQLAlchemy setup with engine, session management,
and Base class for models.
"""

from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from app.config import settings


# Create async engine for SQLite
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    future=True,
)

# Create async session factory
async_session_factory = async_sessionmaker(
    engine,
    expire_on_commit=False,
    autoflush=False,
)


# Base class for all models
class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""
    pass


# PUBLIC_INTERFACE
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency for database session.
    
    Yields:
        AsyncSession: SQLAlchemy async session
    
    Example:
        ```python
        @router.get("/items/")
        async def get_items(db: AsyncSession = Depends(get_db)):
            # Use db session here
            pass
        ```
    """
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


# PUBLIC_INTERFACE
async def init_db() -> None:
    """
    Initialize database by creating all tables.
    
    This function should be called during application startup.
    """
    async with engine.begin() as conn:
        # Import all models here to ensure they are registered with Base
        from app.models.product import Product
        from app.models.order import Order, OrderItem
        
        # Create all tables
        await conn.run_sync(Base.metadata.create_all)
