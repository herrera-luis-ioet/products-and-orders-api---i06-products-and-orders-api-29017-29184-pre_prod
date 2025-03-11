"""
API endpoints for order management.

This module provides endpoints for creating, reading, updating, and deleting orders.
"""

from typing import List, Optional, Any, Union
import logging

from fastapi import APIRouter, Depends, HTTPException, Query, Path, status, Body, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.order import order as order_crud
from app.database import get_db
from app.schemas.order import (
    OrderCreate,
    OrderUpdate,
    OrderResponse,
    OrderSummary,
    OrderStatusResponse
)
from app.models.order import OrderStatus, Order, OrderItem
from app.config import settings
from app.errors import OrderValidationError, ProductValidationError

# Create router for orders endpoints
router = APIRouter()


async def _safely_refresh_product_relationships(
    order: Union[Order, None],
    db: AsyncSession,
    logger: logging.Logger
) -> None:
    """
    Safely refresh product relationships for order items.
    
    This helper function ensures that product relationships are properly loaded
    for all order items, handling the async context correctly to avoid
    'greenlet_spawn has not been called' errors.
    
    Args:
        order: The order object to refresh relationships for
        db: SQLAlchemy async session
        logger: Logger instance for error reporting
        
    Returns:
        None
    """
    # Skip if order is None
    if not order:
        return
    
    try:
        # First refresh the order with its items
        await db.refresh(order, ["items"])
        
        # Ensure items is not None to prevent ResponseValidationError
        if order.items is None:
            order.items = []
            logger.warning(f"Order {order.id} has None items, defaulting to empty list")
            return
        
        # For each order item, ensure the product relationship is loaded
        for item in order.items:
            if item is None:
                continue
                
            try:
                # Only refresh if the product attribute exists and is None
                if hasattr(item, "product") and item.product is None:
                    await db.refresh(item, ["product"])
            except Exception as item_refresh_error:
                # Log the error but continue processing other items
                logger.error(f"Error refreshing product for item {item.id} in order {order.id}: {str(item_refresh_error)}")
    except Exception as refresh_error:
        # Log the error but continue with the order as is
        logger.error(f"Error refreshing order {order.id}: {str(refresh_error)}")
        # We can still return the order even if refresh failed


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
    logger = logging.getLogger(__name__)
    
    try:
        try:
            if status:
                orders = await order_crud.get_by_status(db, status=status, skip=skip, limit=limit)
            else:
                orders = await order_crud.get_multi(db, skip=skip, limit=limit)
        except Exception as db_error:
            logger.error(f"Database error while listing orders: {str(db_error)}")
            raise OrderValidationError(
                detail=f"Error retrieving orders: {str(db_error)}",
                error_type="database_error",
                validation_errors=[{"msg": str(db_error)}]
            )
            
        # Initialize empty list if orders is None to prevent ResponseValidationError
        if orders is None:
            logger.warning("No orders found, returning empty list")
            return []
            
        # For OrderSummary response model, we don't need to refresh relationships
        # as it only includes basic order fields, not items
        
        return orders
    except OrderValidationError as e:
        # Re-raise the exception to be caught by the global exception handler
        raise
    except Exception as e:
        # Log the error and convert to OrderValidationError
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
    
    Responses:
        200: Order details
        404: Order not found
        422: Validation error
        500: Internal server error
    """
    logger = logging.getLogger(__name__)
    
    try:
        # First check if the order exists
        try:
            order = await order_crud.get_with_items(db, id=order_id)
        except OrderValidationError as e:
            # If order not found, return 404
            if e.error_type == "order_not_found":
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=e.detail
                )
            # Re-raise other validation errors
            raise
            
        # Double check if order exists before proceeding
        if not order:
            logger.error(f"Order with ID {order_id} not found but no exception was raised")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Order with ID {order_id} not found"
            )
        
        # Use the helper function to safely refresh product relationships
        await _safely_refresh_product_relationships(order, db, logger)
                
        return order
    except OrderValidationError as e:
        # Check if this is a "not found" error and return 404
        if e.error_type == "order_not_found":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=e.detail
            )
        # Re-raise other validation errors to be caught by the global exception handler
        raise
    except HTTPException:
        # Re-raise HTTP exceptions (like 404)
        raise
    except Exception as e:
        # Log the error and convert to OrderValidationError
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
    
    Returns:
        OrderResponse: The created order with all items
        
    Responses:
        201: Order created successfully
        404: Product not found
        422: Validation error (OrderValidationError or ProductValidationError)
        500: Internal server error
    """
    logger = logging.getLogger(__name__)
    
    try:
        # The custom exceptions will be caught by the global exception handlers in app.errors
        order = await order_crud.create_with_items(db, obj_in=order_in)
        
        # Check if order was created successfully
        if not order:
            raise OrderValidationError(
                detail="Failed to create order",
                error_type="order_creation_failed",
                validation_errors=[{"msg": "Failed to create order"}]
            )
        
        # Use the helper function to safely refresh product relationships
        await _safely_refresh_product_relationships(order, db, logger)
                
        return order
    except ProductValidationError as e:
        # Check if this is a "product not found" error and return 404
        if e.error_type == "product_not_found":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product not found: {e.detail}"
            )
        # Re-raise other validation errors to be caught by the global exception handler
        raise
    except OrderValidationError as e:
        # Re-raise the exception to be caught by the global exception handler
        raise
    except Exception as e:
        # Log the error and convert to OrderValidationError
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
    
    Responses:
        200: Order updated successfully
        404: Order not found
        422: Validation error
        500: Internal server error
    """
    logger = logging.getLogger(__name__)
    
    try:
        # First check if the order exists
        try:
            order = await order_crud.get(db, id=order_id)
        except OrderValidationError as e:
            # If order not found, return 404
            if e.error_type == "order_not_found":
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=e.detail
                )
            # Re-raise other validation errors
            raise
            
        # Update the order
        updated_order = await order_crud.update(db, db_obj=order, obj_in=order_in)
        
        # Get the order with items to return in the response
        try:
            order = await order_crud.get_with_items(db, id=order_id)
            
            # Double check if order exists before proceeding
            if not order:
                logger.error(f"Order with ID {order_id} not found after update but no exception was raised")
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Order with ID {order_id} not found after update"
                )
            
            # Use the helper function to safely refresh product relationships
            await _safely_refresh_product_relationships(order, db, logger)
        except OrderValidationError as e:
            # If order not found, return 404
            if e.error_type == "order_not_found":
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=e.detail
                )
            # Re-raise other validation errors
            raise
                
        return order
    except OrderValidationError as e:
        # Check if this is a "not found" error and return 404
        if e.error_type == "order_not_found":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=e.detail
            )
        # Re-raise other validation errors to be caught by the global exception handler
        raise
    except HTTPException:
        # Re-raise HTTP exceptions (like 404)
        raise
    except Exception as e:
        # Log the error and convert to OrderValidationError
        logger.error(f"Error updating order {order_id}: {str(e)}")
        raise OrderValidationError(
            detail=f"Error updating order: {str(e)}",
            error_type="update_error"
        )


# PUBLIC_INTERFACE
@router.delete("/{order_id}", response_model=OrderStatusResponse)
async def delete_order(
    order_id: int = Path(..., gt=0, description="The ID of the order to delete"),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """
    Delete an order.
    
    - **order_id**: The ID of the order to delete
    
    Responses:
        200: Order deleted successfully
        404: Order not found
        422: Validation error
        500: Internal server error
    """
    logger = logging.getLogger(__name__)
    
    try:
        # First check if the order exists
        try:
            # This will raise OrderValidationError if not found
            await order_crud.get(db, id=order_id)
        except OrderValidationError as e:
            # If order not found, return 404
            if e.error_type == "order_not_found":
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=e.detail
                )
            # Re-raise other validation errors
            raise
            
        # Delete the order
        try:
            order = await order_crud.remove(db, id=order_id)
            
            # Check if order was actually deleted
            if not order:
                logger.error(f"Order with ID {order_id} not deleted properly but no exception was raised")
                raise OrderValidationError(
                    detail=f"Failed to delete order with ID {order_id}",
                    error_type="deletion_failed",
                    validation_errors=[{"msg": f"Failed to delete order with ID {order_id}"}]
                )
                
            return order
        except OrderValidationError as e:
            # If this is a specific error type that should be handled differently
            if e.error_type == "invalid_order_deletion":
                # For example, can't delete shipped/delivered orders
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail=e.detail
                )
            # Re-raise other validation errors
            raise
    except OrderValidationError as e:
        # Check if this is a "not found" error and return 404
        if e.error_type == "order_not_found":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=e.detail
            )
        # Re-raise other validation errors to be caught by the global exception handler
        raise
    except HTTPException:
        # Re-raise HTTP exceptions (like 404)
        raise
    except Exception as e:
        # Log the error and convert to OrderValidationError
        logger.error(f"Error deleting order {order_id}: {str(e)}")
        raise OrderValidationError(
            detail=f"Error deleting order: {str(e)}",
            error_type="deletion_error"
        )


# PUBLIC_INTERFACE
@router.put("/{order_id}/status", response_model=OrderStatusResponse)
async def update_order_status(
    status_update: dict = Body(..., description="New order status", example={"status": "shipped"}),
    order_id: int = Path(..., gt=0, description="The ID of the order to update"),
    db: AsyncSession = Depends(get_db)
) -> Any:
    """
    Update order status.
    
    - **order_id**: The ID of the order to update
    - **status**: New status for the order
    
    Responses:
        200: Order status updated successfully
        404: Order not found
        422: Validation error
        500: Internal server error
    """
    logger = logging.getLogger(__name__)
    
    try:
        # Extract status from the request body
        if "status" not in status_update:
            raise OrderValidationError(
                detail="Status field is required",
                error_type="missing_status_field",
                validation_errors=[{"msg": "Status field is required"}]
            )
        
        # Convert string status to enum
        try:
            status_enum = OrderStatus(status_update["status"])
        except ValueError:
            valid_statuses = [s.value for s in OrderStatus]
            raise OrderValidationError(
                detail=f"Invalid status value. Must be one of: {', '.join(valid_statuses)}",
                error_type="invalid_status_value",
                validation_errors=[{"msg": f"Invalid status value. Must be one of: {', '.join(valid_statuses)}"}]
            )
        
        # First check if the order exists
        try:
            # Update the order status
            updated_order = await order_crud.update_status(db, id=order_id, status=status_enum)
            
            # Get the order with items to return in the response
            order = await order_crud.get_with_items(db, id=order_id)
            
            # Double check if order exists before proceeding
            if not order:
                logger.error(f"Order with ID {order_id} not found after status update but no exception was raised")
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Order with ID {order_id} not found after status update"
                )
            
            # Use the helper function to safely refresh product relationships
            await _safely_refresh_product_relationships(order, db, logger)
        except OrderValidationError as e:
            # If order not found, return 404
            if e.error_type == "order_not_found":
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=e.detail
                )
            # Re-raise other validation errors
            raise
                
        return order
    except OrderValidationError as e:
        # Check if this is a "not found" error and return 404
        if e.error_type == "order_not_found":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=e.detail
            )
        # Re-raise other validation errors to be caught by the global exception handler
        raise
    except HTTPException:
        # Re-raise HTTP exceptions (like 404)
        raise
    except Exception as e:
        # Log the error and convert to OrderValidationError
        logger.error(f"Error updating order status for order {order_id}: {str(e)}")
        raise OrderValidationError(
            detail=f"Error updating order status: {str(e)}",
            error_type="status_update_error"
        )


# PUBLIC_INTERFACE
@router.get("/customer/{customer_email}", response_model=List[OrderResponse])
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
    logger = logging.getLogger(__name__)
    
    try:
        orders = await order_crud.get_by_customer_email(db, email=customer_email, skip=skip, limit=limit)
        
        # Initialize empty list if orders is None to prevent ResponseValidationError
        if orders is None:
            logger.warning(f"No orders found for customer {customer_email}, returning empty list")
            return []
        
        # Ensure all orders and their items are properly attached to the session
        for order in orders:
            # Skip empty orders (should not happen, but just to be safe)
            if not order:
                continue
                
            # Use the helper function to safely refresh product relationships
            await _safely_refresh_product_relationships(order, db, logger)
        
        return orders
    except OrderValidationError as e:
        # Check if this is a specific error type that should be handled differently
        if e.error_type == "customer_not_found":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=e.detail
            )
        # Re-raise other validation errors to be caught by the global exception handler
        raise
    except Exception as e:
        # Log the error and convert to OrderValidationError
        logger.error(f"Error retrieving orders for customer {customer_email}: {str(e)}")
        raise OrderValidationError(
            detail=f"Error retrieving customer orders: {str(e)}",
            error_type="customer_orders_error"
        )
