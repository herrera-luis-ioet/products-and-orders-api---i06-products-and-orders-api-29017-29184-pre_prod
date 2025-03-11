"""
Order schemas.

This module provides Pydantic schemas for order validation and serialization.
"""

from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional, List

from pydantic import BaseModel, Field, ConfigDict, field_validator

from app.models.order import OrderStatus
from app.schemas.product import ProductSummary


# PUBLIC_INTERFACE
class OrderItemBase(BaseModel):
    """
    Base schema for order item data.
    
    This schema defines the common fields for all order item-related schemas.
    """
    product_id: int = Field(..., description="ID of the product")
    quantity: int = Field(..., description="Quantity of the product", gt=0)
    unit_price: Optional[Decimal] = Field(None, description="Unit price at time of order", ge=0)


# PUBLIC_INTERFACE
class OrderItemCreate(OrderItemBase):
    """
    Schema for creating a new order item.
    
    This schema is used for validating order item creation requests.
    """
    pass


# PUBLIC_INTERFACE
class OrderItemUpdate(BaseModel):
    """
    Schema for updating an existing order item.
    
    This schema is used for validating order item update requests.
    All fields are optional to allow partial updates.
    """
    quantity: Optional[int] = Field(None, description="Quantity of the product", gt=0)


# PUBLIC_INTERFACE
class OrderItemInDB(OrderItemBase):
    """
    Schema for order item data as stored in the database.
    
    This schema includes database-specific fields like id and timestamps.
    """
    id: int
    order_id: int
    subtotal: Decimal = Field(..., description="Subtotal for this item (quantity * unit_price)")
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# PUBLIC_INTERFACE
class OrderItemResponse(OrderItemInDB):
    """
    Schema for order item response.
    
    This schema is used for serializing order item data in API responses.
    It includes product details.
    """
    product: ProductSummary


# PUBLIC_INTERFACE
class OrderBase(BaseModel):
    """
    Base schema for order data.
    
    This schema defines the common fields for all order-related schemas.
    """
    customer_name: str = Field(..., description="Customer's full name", max_length=255)
    customer_email: str = Field(..., description="Customer's email address", max_length=255)
    customer_phone: Optional[str] = Field(None, description="Customer's phone number", max_length=20)
    shipping_address: Optional[str] = Field(None, description="Shipping address")
    billing_address: Optional[str] = Field(None, description="Billing address")
    payment_method: Optional[str] = Field(None, description="Payment method used", max_length=50)
    payment_id: Optional[str] = Field(None, description="Payment ID from payment gateway", max_length=100)
    notes: Optional[str] = Field(None, description="Additional notes for the order")


# PUBLIC_INTERFACE
class OrderCreate(OrderBase):
    """
    Schema for creating a new order.
    
    This schema is used for validating order creation requests.
    It includes a list of order items.
    """
    items: List[OrderItemCreate] = Field(..., description="List of order items", min_length=1)


# PUBLIC_INTERFACE
class OrderUpdate(BaseModel):
    """
    Schema for updating an existing order.
    
    This schema is used for validating order update requests.
    All fields are optional to allow partial updates.
    """
    status: Optional[OrderStatus] = Field(None, description="Current status of the order")
    customer_name: Optional[str] = Field(None, description="Customer's full name", max_length=255)
    customer_email: Optional[str] = Field(None, description="Customer's email address", max_length=255)
    customer_phone: Optional[str] = Field(None, description="Customer's phone number", max_length=20)
    shipping_address: Optional[str] = Field(None, description="Shipping address")
    billing_address: Optional[str] = Field(None, description="Billing address")
    payment_method: Optional[str] = Field(None, description="Payment method used", max_length=50)
    payment_id: Optional[str] = Field(None, description="Payment ID from payment gateway", max_length=100)
    notes: Optional[str] = Field(None, description="Additional notes for the order")


# PUBLIC_INTERFACE
class OrderInDB(OrderBase):
    """
    Schema for order data as stored in the database.
    
    This schema includes database-specific fields like id and timestamps.
    """
    id: int
    status: OrderStatus = Field(..., description="Current status of the order")
    total_amount: Decimal = Field(..., description="Total order amount in USD", ge=0)
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# PUBLIC_INTERFACE
class OrderResponse(OrderInDB):
    """
    Schema for order response.
    
    This schema is used for serializing order data in API responses.
    It includes a list of order items with their product details.
    """
    items: List[OrderItemResponse] = Field(..., description="List of order items")


# PUBLIC_INTERFACE
class OrderSummary(BaseModel):
    """
    Schema for a summary of order data.
    
    This schema is used for listing orders without including all details.
    """
    id: int
    status: OrderStatus
    total_amount: Decimal
    customer_name: str
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)