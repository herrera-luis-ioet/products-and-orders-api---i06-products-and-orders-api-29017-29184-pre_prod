"""
Product schemas.

This module provides Pydantic schemas for product validation and serialization.
"""

from datetime import datetime
from decimal import Decimal
from typing import Optional, List

from pydantic import BaseModel, Field, ConfigDict, field_validator


# PUBLIC_INTERFACE
class ProductBase(BaseModel):
    """
    Base schema for product data.
    
    This schema defines the common fields for all product-related schemas.
    """
    name: str = Field(..., description="Product name", max_length=255)
    price: Decimal = Field(..., description="Product price in USD", ge=0)
    inventory_count: int = Field(..., description="Number of items in inventory", ge=0)
    sku: str = Field(..., description="Stock Keeping Unit - unique identifier", max_length=50)
    description: Optional[str] = Field(None, description="Detailed product description")
    category: Optional[str] = Field(None, description="Product category", max_length=100)
    image_url: Optional[str] = Field(None, description="URL to product image", max_length=255)
    weight: Optional[int] = Field(None, description="Weight in grams", ge=0)
    dimensions: Optional[str] = Field(None, description="Dimensions (e.g., '10x20x30 cm')", max_length=50)
    is_active: bool = Field(True, description="Whether the product is active and can be purchased")


# PUBLIC_INTERFACE
class ProductCreate(ProductBase):
    """
    Schema for creating a new product.
    
    This schema is used for validating product creation requests.
    """
    pass


# PUBLIC_INTERFACE
class ProductUpdate(BaseModel):
    """
    Schema for updating an existing product.
    
    This schema is used for validating product update requests.
    All fields are optional to allow partial updates.
    """
    name: Optional[str] = Field(None, description="Product name", max_length=255)
    price: Optional[Decimal] = Field(None, description="Product price in USD", ge=0)
    inventory_count: Optional[int] = Field(None, description="Number of items in inventory", ge=0)
    sku: Optional[str] = Field(None, description="Stock Keeping Unit - unique identifier", max_length=50)
    description: Optional[str] = Field(None, description="Detailed product description")
    category: Optional[str] = Field(None, description="Product category", max_length=100)
    image_url: Optional[str] = Field(None, description="URL to product image", max_length=255)
    weight: Optional[int] = Field(None, description="Weight in grams", ge=0)
    dimensions: Optional[str] = Field(None, description="Dimensions (e.g., '10x20x30 cm')", max_length=50)
    is_active: Optional[bool] = Field(None, description="Whether the product is active and can be purchased")


# PUBLIC_INTERFACE
class ProductInDB(ProductBase):
    """
    Schema for product data as stored in the database.
    
    This schema includes database-specific fields like id and timestamps.
    """
    id: int
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# PUBLIC_INTERFACE
class ProductResponse(ProductInDB):
    """
    Schema for product response.
    
    This schema is used for serializing product data in API responses.
    """
    pass


# PUBLIC_INTERFACE
class ProductSummary(BaseModel):
    """
    Schema for a summary of product data.
    
    This schema is used for including product data in other responses,
    like order responses, without including all product details.
    """
    id: int
    name: str
    sku: str
    price: Decimal
    
    model_config = ConfigDict(from_attributes=True)