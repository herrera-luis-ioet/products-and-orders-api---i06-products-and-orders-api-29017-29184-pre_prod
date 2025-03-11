"""
API endpoints for order management.

This module provides endpoints for creating, reading, updating, and deleting orders.
"""

from typing import List, Optional, Any
import logging

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
from app.errors import OrderValidationError, ProductValidationError

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
    
    Responses:
        200: List of orders
        422: Validation error
        500: Internal server error
    """
    try:
        if status:
            orders = await order_crud.get_by_status(db, status=status, skip=skip, limit=limit)
        else:
            orders = await order_crud.get_multi(db, skip=skip, limit=limit)
        return orders
    except Exception as e:
        # Log the error and convert to OrderValidationError
        logger = logging.getLogger(__name__)
        logger.error(f"Error listing orders: {str(e)}")
        raise OrderValidationError(
            detail=f"Error listing orders: {str(e)}",
            error_type="list_error"
        )


# PUBLIC_INTERFACE
@router.get("/{order_id}", response_model=OrderResponse)
async def get_order(
    order_id: int = Path(..., gt=0, description="The ID of the order to get"),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """
    Get a specific order by ID.
    
    - **order_id**: The ID of the order to retrieve
    
    Raises:
        OrderValidationError: If order not found
    """
    try:
        # The custom exceptions will be caught by the global exception handlers in app.errors
        order = await order_crud.get_with_items(db, id=order_id)
        return order
    except OrderValidationError as e:
        # Re-raise the exception to be caught by the global exception handler
        raise
    except Exception as e:
        # Log the error and convert to OrderValidationError
        logger = logging.getLogger(__name__)
        logger.error(f"Error retrieving order {order_id}: {str(e)}")
        raise OrderValidationError(
            detail=f"Error retrieving order: {str(e)}",
            error_type="retrieval_error"
        )


# PUBLIC_INTERFACE
@router.post("/", response_model=OrderResponse, status_code=status.HTTP_201_CREATED)
async def create_order(
    order_in: OrderCreate,
    db: AsyncSession = Depends(get_db)
) -> Any:
    """
    Create a new order.
    
    - **order_in**: Order data to create, including items
    
    Raises:
        OrderValidationError: If order validation fails
        ProductValidationError: If product validation fails
    
    Returns:
        OrderResponse: The created order with all items
        
    Responses:
        201: Order created successfully
        422: Validation error (OrderValidationError or ProductValidationError)
        500: Internal server error
    """
    try:
        # The custom exceptions will be caught by the global exception handlers in app.errors
        order = await order_crud.create_with_items(db, obj_in=order_in)
        return order
    except (OrderValidationError, ProductValidationError) as e:
        # Re-raise the exception to be caught by the global exception handler
        raise
    except Exception as e:
        # Log the error and convert to OrderValidationError
        logger = logging.getLogger(__name__)
        logger.error(f"Error creating order: {str(e)}")
        raise OrderValidationError(
            detail=f"Error creating order: {str(e)}",
            error_type="creation_error"
        )


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
    
    Raises:
        OrderValidationError: If order validation fails
    
    Responses:
        200: Order updated successfully
        404: Order not found
        422: Validation error
        500: Internal server error
    """
    try:
        # The custom exceptions will be caught by the global exception handlers in app.errors
        order = await order_crud.get(db, id=order_id)
        updated_order = await order_crud.update(db, db_obj=order, obj_in=order_in)
        return updated_order
    except OrderValidationError as e:
        # Re-raise the exception to be caught by the global exception handler
        raise
    except Exception as e:
        # Log the error and convert to OrderValidationError
        logger = logging.getLogger(__name__)
        logger.error(f"Error updating order {order_id}: {str(e)}")
        raise OrderValidationError(
            detail=f"Error updating order: {str(e)}",
            error_type="update_error"
        )


# PUBLIC_INTERFACE
@router.delete("/{order_id}", response_model=OrderResponse)
async def delete_order(
    order_id: int = Path(..., gt=0, description="The ID of the order to delete"),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """
    Delete an order.
    
    - **order_id**: The ID of the order to delete
    
    Raises:
        OrderValidationError: If order validation fails
    
    Responses:
        200: Order deleted successfully
        404: Order not found
        422: Validation error
        500: Internal server error
    """
    try:
        # The custom exceptions will be caught by the global exception handlers in app.errors
        # First check if the order exists (will raise OrderValidationError if not)
        await order_crud.get(db, id=order_id)
        order = await order_crud.remove(db, id=order_id)
        return order
    except OrderValidationError as e:
        # Re-raise the exception to be caught by the global exception handler
        raise
    except Exception as e:
        # Log the error and convert to OrderValidationError
        logger = logging.getLogger(__name__)
        logger.error(f"Error deleting order {order_id}: {str(e)}")
        raise OrderValidationError(
            detail=f"Error deleting order: {str(e)}",
            error_type="deletion_error"
        )


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
    
    Raises:
        OrderValidationError: If order validation fails
    
    Responses:
        200: Order status updated successfully
        404: Order not found
        422: Validation error
        500: Internal server error
    """
    try:
        # The custom exceptions will be caught by the global exception handlers in app.errors
        updated_order = await order_crud.update_status(db, id=order_id, status=status)
        return updated_order
    except OrderValidationError as e:
        # Re-raise the exception to be caught by the global exception handler
        raise
    except Exception as e:
        # Log the error and convert to OrderValidationError
        logger = logging.getLogger(__name__)
        logger.error(f"Error updating order status for order {order_id}: {str(e)}")
        raise OrderValidationError(
            detail=f"Error updating order status: {str(e)}",
            error_type="status_update_error"
        )


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
    
    Responses:
        200: List of orders for the customer
        422: Validation error
        500: Internal server error
    """
    try:
        orders = await order_crud.get_by_customer_email(db, email=customer_email, skip=skip, limit=limit)
        return orders
    except Exception as e:
        # Log the error and convert to OrderValidationError
        logger = logging.getLogger(__name__)
        logger.error(f"Error retrieving orders for customer {customer_email}: {str(e)}")
        raise OrderValidationError(
            detail=f"Error retrieving customer orders: {str(e)}",
            error_type="customer_orders_error"
        )
