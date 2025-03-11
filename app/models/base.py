"""
Base model class with common fields.

This module provides a base model class with common fields like id, created_at, and updated_at
that can be inherited by other models.
"""

from datetime import datetime
from typing import Optional

from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from app.database import Base


class BaseModel(AsyncAttrs, Base):
    """
    Base model class with common fields.
    
    All models should inherit from this class to have common fields like id, created_at, and updated_at.
    """
    __abstract__ = True
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    created_at: Mapped[datetime] = mapped_column(default=func.now(), index=True)
    updated_at: Mapped[datetime] = mapped_column(
        default=func.now(),
        onupdate=func.now(),
        index=True
    )