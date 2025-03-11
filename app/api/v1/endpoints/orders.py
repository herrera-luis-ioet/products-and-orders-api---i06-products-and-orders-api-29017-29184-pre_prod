"""
API endpoints for order management.

This module provides endpoints for creating, reading, updating, and deleting orders.
"""

from typing import List, Optional, Any

from fastapi import APIRouter, Depends, HTTPException, Query, Path, status, Body
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.order import order as order_crud
from app.database import get_db
from app.schemas.order import (
    OrderCreate,
    OrderUpdate,
    OrderResponse,
    OrderSummary
)
from app.models.order import OrderStatus
from app.config import settings

# Create router for orders endpoints
router = APIRouter()


# PUBLIC_INTERFACE
@router.get("/", response_model=List[OrderSummary])
async def list_orders(
    db: AsyncSession = Depends(get_db),
    skip: int = Query(0, ge=0, description="Number of orders to skip"),
    limit: int = Query(settings.PAGINATION_PAGE_SIZE, ge=1, le=100, description="Number of orders to return"),
    sort_by: Optional[str] = Query(None, description="Field to sort by"),
    sort_desc: bool = Query(False, description="Sort in descending order"),
    status: Optional[OrderStatus] = Query(None, description="Filter by order status")
) -> Any:
    """
    List all orders with pagination, filtering, and sorting.
    
    - **skip**: Number of orders to skip (for pagination)
    - **limit**: Maximum number of orders to return
    - **sort_by**: Field to sort by (e.g., created_at, total_amount)
    - **sort_desc**: Sort in descending order if true
    - **status**: Filter by order status if provided
    """
    if status:
        orders = await order_crud.get_by_status(db, status=status, skip=skip, limit=limit)
    else:
        orders = await order_crud.get_multi(db, skip=skip, limit=limit)
    return orders


# PUBLIC_INTERFACE
@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(
    order_id: int = Path(..., gt=0, description="The ID of the order to get"),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """
    Get a specific order by ID.
    
    - **order_id**: The ID of the order to retrieve
    """
    order = await order_crud.get_with_items(db, id=order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with ID {order_id} not found"
        )
    return order


# PUBLIC_INTERFACE
@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(
    order_in: OrderCreate,
    db: AsyncSession = Depends(get_db)
) -> Any:
    """
    Create a new order.
    
    - **order_in**: Order data to create, including items
    """
    order = await order_crud.create_with_items(db, obj_in=order_in)
    return order


# PUBLIC_INTERFACE
@router.put("/{order_id}", response_model=OrderResponse)
async def update_order(
    order_in: OrderUpdate,
    order_id: int = Path(..., gt=0, description="The ID of the order to update"),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """
    Update an existing order.
    
    - **order_id**: The ID of the order to update
    - **order_in**: Updated order data
    """
    order = await order_crud.get(db, id=order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with ID {order_id} not found"
        )
    
    updated_order = await order_crud.update(db, db_obj=order, obj_in=order_in)
    return updated_order


# PUBLIC_INTERFACE
@router.delete("/{order_id}", response_model=OrderResponse)
async def delete_order(
    order_id: int = Path(..., gt=0, description="The ID of the order to delete"),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """
    Delete an order.
    
    - **order_id**: The ID of the order to delete
    """
    order = await order_crud.get(db, id=order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with ID {order_id} not found"
        )
    
    order = await order_crud.remove(db, id=order_id)
    return order


# PUBLIC_INTERFACE
@router.put("/{order_id}/status", response_model=OrderResponse)
async def update_order_status(
    status: OrderStatus = Body(..., description="New order status"),
    order_id: int = Path(..., gt=0, description="The ID of the order to update"),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """
    Update order status.
    
    - **order_id**: The ID of the order to update
    - **status**: New status for the order
    """
    order = await order_crud.get(db, id=order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with ID {order_id} not found"
        )
    
    updated_order = await order_crud.update_status(db, id=order_id, status=status)
    return updated_order


# PUBLIC_INTERFACE
@router.get("/customer/{customer_email}", response_model=List[OrderSummary])
async def get_orders_by_customer_email(
    customer_email: str = Path(..., description="Customer email address"),
    db: AsyncSession = Depends(get_db),
    skip: int = Query(0, ge=0, description="Number of orders to skip"),
    limit: int = Query(settings.PAGINATION_PAGE_SIZE, ge=1, le=100, description="Number of orders to return")
) -> Any:
    """
    Get orders by customer email.
    
    - **customer_email**: Email address of the customer
    - **skip**: Number of orders to skip (for pagination)
    - **limit**: Maximum number of orders to return
    """
    orders = await order_crud.get_by_customer_email(db, email=customer_email, skip=skip, limit=limit)
    return orders