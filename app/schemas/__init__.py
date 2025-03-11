"""
Pydantic schemas for request/response validation.

This package contains Pydantic schemas for validating requests and responses.
"""

from app.schemas.product import (
    ProductBase,
    ProductCreate,
    ProductUpdate,
    ProductInDB,
    ProductResponse,
    ProductSummary,
)

from app.schemas.order import (
    OrderStatus,
    OrderItemBase,
    OrderItemCreate,
    OrderItemUpdate,
    OrderItemInDB,
    OrderItemResponse,
    OrderBase,
    OrderCreate,
    OrderUpdate,
    OrderInDB,
    OrderResponse,
    OrderSummary,
)

__all__ = [
    # Product schemas
    "ProductBase",
    "ProductCreate",
    "ProductUpdate",
    "ProductInDB",
    "ProductResponse",
    "ProductSummary",
    
    # Order schemas
    "OrderStatus",
    "OrderItemBase",
    "OrderItemCreate",
    "OrderItemUpdate",
    "OrderItemInDB",
    "OrderItemResponse",
    "OrderBase",
    "OrderCreate",
    "OrderUpdate",
    "OrderInDB",
    "OrderResponse",
    "OrderSummary",
]
