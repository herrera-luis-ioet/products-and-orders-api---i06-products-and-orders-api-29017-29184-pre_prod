"""
API endpoints for product management.

This module provides endpoints for creating, reading, updating, and deleting products.
"""

from typing import List, Optional, Any

from fastapi import APIRouter, Depends, HTTPException, Query, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.product import product as product_crud
from app.database import get_db
from app.schemas.product import (
    ProductCreate,
    ProductUpdate,
    ProductResponse,
    ProductSummary
)
from app.config import settings

# Create router for products endpoints
router = APIRouter()


# PUBLIC_INTERFACE
@router.get("/", response_model=List[ProductSummary])
async def list_products(
    db: AsyncSession = Depends(get_db),
    skip: int = Query(0, ge=0, description="Number of products to skip"),
    limit: int = Query(settings.PAGINATION_PAGE_SIZE, ge=1, le=100, description="Number of products to return"),
    sort_by: Optional[str] = Query(None, description="Field to sort by"),
    sort_desc: bool = Query(False, description="Sort in descending order"),
    is_active: Optional[bool] = Query(None, description="Filter by active status")
) -> Any:
    """
    List all products with pagination, filtering, and sorting.
    
    - **skip**: Number of products to skip (for pagination)
    - **limit**: Maximum number of products to return
    - **sort_by**: Field to sort by (e.g., name, price)
    - **sort_desc**: Sort in descending order if true
    - **is_active**: Filter by active status if provided
    """
    if is_active is not None:
        products = await product_crud.get_active(db, skip=skip, limit=limit)
    else:
        products = await product_crud.get_multi(db, skip=skip, limit=limit)
    return products


# PUBLIC_INTERFACE
@router.get("/{product_id}", response_model=ProductResponse)
async def get_product(
    product_id: int = Path(..., gt=0, description="The ID of the product to get"),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """
    Get a specific product by ID.
    
    - **product_id**: The ID of the product to retrieve
    """
    product = await product_crud.get(db, id=product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {product_id} not found"
        )
    return product


# PUBLIC_INTERFACE
@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
async def create_product(
    product_in: ProductCreate,
    db: AsyncSession = Depends(get_db)
) -> Any:
    """
    Create a new product.
    
    - **product_in**: Product data to create
    """
    # Check if product with same SKU already exists
    existing_product = await product_crud.get_by_sku(db, sku=product_in.sku)
    if existing_product:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Product with SKU {product_in.sku} already exists"
        )
    
    product = await product_crud.create(db, obj_in=product_in)
    return product


# PUBLIC_INTERFACE
@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_in: ProductUpdate,
    product_id: int = Path(..., gt=0, description="The ID of the product to update"),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """
    Update an existing product.
    
    - **product_id**: The ID of the product to update
    - **product_in**: Updated product data
    """
    product = await product_crud.get(db, id=product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {product_id} not found"
        )
    
    # If SKU is being updated, check if it conflicts with another product
    if product_in.sku and product_in.sku != product.sku:
        existing_product = await product_crud.get_by_sku(db, sku=product_in.sku)
        if existing_product and existing_product.id != product_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Product with SKU {product_in.sku} already exists"
            )
    
    updated_product = await product_crud.update(db, db_obj=product, obj_in=product_in)
    return updated_product


# PUBLIC_INTERFACE
@router.delete("/{product_id}", response_model=ProductResponse)
async def delete_product(
    product_id: int = Path(..., gt=0, description="The ID of the product to delete"),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """
    Delete a product.
    
    - **product_id**: The ID of the product to delete
    """
    product = await product_crud.get(db, id=product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {product_id} not found"
        )
    
    product = await product_crud.remove(db, id=product_id)
    return product


# PUBLIC_INTERFACE
@router.get("/search/", response_model=List[ProductSummary])
async def search_products(
    query: str = Query(..., min_length=1, description="Search query string"),
    db: AsyncSession = Depends(get_db),
    skip: int = Query(0, ge=0, description="Number of products to skip"),
    limit: int = Query(settings.PAGINATION_PAGE_SIZE, ge=1, le=100, description="Number of products to return")
) -> Any:
    """
    Search products by name or description.
    
    - **query**: Search term to look for in product name or description
    - **skip**: Number of products to skip (for pagination)
    - **limit**: Maximum number of products to return
    """
    products = await product_crud.search_products(db, query=query, skip=skip, limit=limit)
    return products


# PUBLIC_INTERFACE
@router.get("/category/{category}", response_model=List[ProductSummary])
async def get_products_by_category(
    category: str = Path(..., description="Category name"),
    db: AsyncSession = Depends(get_db),
    skip: int = Query(0, ge=0, description="Number of products to skip"),
    limit: int = Query(settings.PAGINATION_PAGE_SIZE, ge=1, le=100, description="Number of products to return")
) -> Any:
    """
    Get products by category.
    
    - **category**: Category name to filter by
    - **skip**: Number of products to skip (for pagination)
    - **limit**: Maximum number of products to return
    """
    products = await product_crud.get_by_category(db, category=category, skip=skip, limit=limit)
    return products