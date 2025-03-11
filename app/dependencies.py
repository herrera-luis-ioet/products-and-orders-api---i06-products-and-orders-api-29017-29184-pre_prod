"""
Dependency injection functions for FastAPI routes.

This module provides common dependencies used across API routes,
including database sessions, pagination parameters, and authentication.
"""

from typing import Annotated, AsyncGenerator, Optional, Tuple

from fastapi import Depends, Header, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.database import get_db


# PUBLIC_INTERFACE
def get_pagination_params(
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(
        settings.PAGINATION_PAGE_SIZE,
        ge=1,
        le=100,
        description="Number of items to return"
    ),
) -> Tuple[int, int]:
    """
    Get pagination parameters from query parameters.
    
    Args:
        skip: Number of items to skip (for pagination)
        limit: Maximum number of items to return
        
    Returns:
        Tuple[int, int]: Tuple containing skip and limit values
        
    Example:
        ```python
        @router.get("/items/")
        async def list_items(
            pagination: Tuple[int, int] = Depends(get_pagination_params),
            db: AsyncSession = Depends(get_db)
        ):
            skip, limit = pagination
            # Use skip and limit for pagination
            pass
        ```
    """
    return skip, limit


# PUBLIC_INTERFACE
def get_sort_params(
    sort_by: Optional[str] = Query(None, description="Field to sort by"),
    sort_desc: bool = Query(False, description="Sort in descending order"),
) -> Tuple[Optional[str], bool]:
    """
    Get sorting parameters from query parameters.
    
    Args:
        sort_by: Field to sort by
        sort_desc: Sort in descending order if true
        
    Returns:
        Tuple[Optional[str], bool]: Tuple containing sort_by and sort_desc values
        
    Example:
        ```python
        @router.get("/items/")
        async def list_items(
            sort_params: Tuple[Optional[str], bool] = Depends(get_sort_params),
            db: AsyncSession = Depends(get_db)
        ):
            sort_by, sort_desc = sort_params
            # Use sort_by and sort_desc for sorting
            pass
        ```
    """
    return sort_by, sort_desc


# PUBLIC_INTERFACE
def get_correlation_id(
    x_correlation_id: Optional[str] = Header(None, description="Correlation ID for request tracing")
) -> str:
    """
    Get or generate a correlation ID for request tracing.
    
    Args:
        x_correlation_id: Correlation ID from request header
        
    Returns:
        str: Correlation ID (from header or generated)
        
    Example:
        ```python
        @router.get("/items/")
        async def list_items(
            correlation_id: str = Depends(get_correlation_id),
            db: AsyncSession = Depends(get_db)
        ):
            # Use correlation_id for logging or tracing
            pass
        ```
    """
    import uuid
    
    if x_correlation_id:
        return x_correlation_id
    return str(uuid.uuid4())


# Type aliases for common dependencies
DBSession = Annotated[AsyncSession, Depends(get_db)]
PaginationParams = Annotated[Tuple[int, int], Depends(get_pagination_params)]
SortParams = Annotated[Tuple[Optional[str], bool], Depends(get_sort_params)]
CorrelationId = Annotated[str, Depends(get_correlation_id)]


# PUBLIC_INTERFACE
def validate_product_exists(product_id: int, db: DBSession) -> None:
    """
    Validate that a product exists.
    
    Args:
        product_id: ID of the product to validate
        db: Database session
        
    Raises:
        HTTPException: If the product does not exist
        
    Example:
        ```python
        @router.get("/products/{product_id}")
        async def get_product(
            product_id: int,
            db: AsyncSession = Depends(get_db)
        ):
            await validate_product_exists(product_id, db)
            # Continue with operation
            pass
        ```
    """
    from app.crud.product import product as product_crud
    
    product = await product_crud.get(db, id=product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product with ID {product_id} not found"
        )


# PUBLIC_INTERFACE
def validate_order_exists(order_id: int, db: DBSession) -> None:
    """
    Validate that an order exists.
    
    Args:
        order_id: ID of the order to validate
        db: Database session
        
    Raises:
        HTTPException: If the order does not exist
        
    Example:
        ```python
        @router.get("/orders/{order_id}")
        async def get_order(
            order_id: int,
            db: AsyncSession = Depends(get_db)
        ):
            await validate_order_exists(order_id, db)
            # Continue with operation
            pass
        ```
    """
    from app.crud.order import order as order_crud
    
    order = await order_crud.get(db, id=order_id)
    if not order:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Order with ID {order_id} not found"
        )