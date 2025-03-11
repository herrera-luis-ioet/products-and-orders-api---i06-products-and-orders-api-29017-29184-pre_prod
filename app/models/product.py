"""
Product model.

This module provides the Product model for storing product information.
"""

from decimal import Decimal
from typing import List, Optional

from sqlalchemy import String, Numeric, Integer, Text, Index, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel


class Product(BaseModel):
    """
    Product model for storing product information.
    
    Attributes:
        name: The name of the product
        description: A detailed description of the product
        price: The price of the product
        inventory_count: The number of items in inventory
        sku: Stock Keeping Unit - unique identifier for the product
        category: The category of the product
        image_url: URL to the product image
        weight: Weight of the product in grams
        dimensions: Dimensions of the product (e.g., "10x20x30 cm")
        is_active: Whether the product is active and can be purchased
        order_items: Relationship to order items
    """
    __tablename__ = "products"
    
    # Required fields
    name: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    price: Mapped[Decimal] = mapped_column(
        Numeric(precision=10, scale=2),
        nullable=False,
        default=0.0,
        comment="Product price in USD"
    )
    inventory_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=0,
        comment="Number of items in inventory"
    )
    sku: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        unique=True,
        index=True,
        comment="Stock Keeping Unit - unique identifier"
    )
    
    # Optional fields
    description: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        comment="Detailed product description"
    )
    category: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
        index=True,
        comment="Product category"
    )
    image_url: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
        comment="URL to product image"
    )
    weight: Mapped[Optional[int]] = mapped_column(
        Integer,
        nullable=True,
        comment="Weight in grams"
    )
    dimensions: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
        comment="Dimensions (e.g., '10x20x30 cm')"
    )
    is_active: Mapped[bool] = mapped_column(
        default=True,
        index=True,
        comment="Whether the product is active and can be purchased"
    )
    
    # Relationships
    order_items: Mapped[List["OrderItem"]] = relationship(
        back_populates="product",
        cascade="all, delete-orphan"
    )
    
    # Constraints
    __table_args__ = (
        CheckConstraint("price >= 0", name="check_price_positive"),
        CheckConstraint("inventory_count >= 0", name="check_inventory_non_negative"),
        Index("ix_products_name_category", "name", "category"),
    )
    
    def __repr__(self) -> str:
        return f"<Product(id={self.id}, name='{self.name}', sku='{self.sku}')>"