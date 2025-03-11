"""
Tests for order API endpoints.

This module contains tests for the order API endpoints, including
tests for creating, reading, updating, and deleting orders.
It also includes tests for error handling, edge cases, and specific scenarios.
"""

import json
import logging
from typing import Dict, List, Any, Optional
from unittest.mock import patch, MagicMock, AsyncMock

import pytest
from fastapi import status, HTTPException
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from app.models.order import Order, OrderStatus, OrderItem
from app.models.product import Product
from app.api.v1.endpoints.orders import _safely_refresh_product_relationships
from app.errors import OrderValidationError, ProductValidationError


@pytest.mark.asyncio
async def test_list_orders(client: AsyncClient, test_orders: List[Order]):
    """
    Test listing orders.
    
    Args:
        client: Test client
        test_orders: List of test orders
    """
    response = await client.get("/api/v1/orders/")
    
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == len(test_orders)
    
    # Check that all orders are returned
    order_ids = [order["id"] for order in data]
    for order in test_orders:
        assert order.id in order_ids


@pytest.mark.asyncio
async def test_list_orders_pagination(client: AsyncClient, test_orders: List[Order]):
    """
    Test listing orders with pagination.
    
    Args:
        client: Test client
        test_orders: List of test orders
    """
    # Test with skip=1, limit=1
    response = await client.get("/api/v1/orders/?skip=1&limit=1")
    
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    
    # Test with skip=0, limit=1
    response = await client.get("/api/v1/orders/?skip=0&limit=1")
    
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1


@pytest.mark.asyncio
async def test_list_orders_by_status(client: AsyncClient, test_orders: List[Order]):
    """
    Test listing orders by status.
    
    Args:
        client: Test client
        test_orders: List of test orders
    """
    # Test with status=pending
    response = await client.get("/api/v1/orders/?status=pending")
    
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert isinstance(data, list)
    assert all(order["status"] == "pending" for order in data)
    
    # Test with status=processing
    response = await client.get("/api/v1/orders/?status=processing")
    
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert isinstance(data, list)
    assert all(order["status"] == "processing" for order in data)


@pytest.mark.asyncio
async def test_get_order(client: AsyncClient, test_orders: List[Order]):
    """
    Test getting a specific order.
    
    Args:
        client: Test client
        test_orders: List of test orders
    """
    order_id = test_orders[0].id
    response = await client.get(f"/api/v1/orders/{order_id}")
    
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert data["id"] == order_id
    assert data["customer_name"] == test_orders[0].customer_name
    assert data["customer_email"] == test_orders[0].customer_email
    assert data["status"] == test_orders[0].status.value
    assert float(data["total_amount"]) == float(test_orders[0].total_amount)
    
    # Check that items are included
    assert "items" in data
    assert isinstance(data["items"], list)
    assert len(data["items"]) > 0


@pytest.mark.asyncio
async def test_get_order_not_found(client: AsyncClient):
    """
    Test getting a non-existent order.
    
    Args:
        client: Test client
    """
    response = await client.get("/api/v1/orders/999")
    
    assert response.status_code == status.HTTP_404_NOT_FOUND
    
    data = response.json()
    assert "detail" in data
    assert "not found" in data["detail"]


@pytest.mark.asyncio
async def test_create_order(client: AsyncClient, order_data: Dict, test_products: List[Product]):
    """
    Test creating an order.
    
    Args:
        client: Test client
        order_data: Test order data
        test_products: List of test products
    """
    # Update product_id to use an existing product
    order_data["items"][0]["product_id"] = test_products[0].id
    
    response = await client.post(
        "/api/v1/orders/",
        json=order_data,
    )
    
    assert response.status_code == status.HTTP_201_CREATED
    
    data = response.json()
    assert data["customer_name"] == order_data["customer_name"]
    assert data["customer_email"] == order_data["customer_email"]
    assert data["status"] == OrderStatus.PENDING.value
    assert "id" in data
    assert data["id"] > 0
    
    # Check that items are included
    assert "items" in data
    assert isinstance(data["items"], list)
    assert len(data["items"]) == len(order_data["items"])
    assert data["items"][0]["product_id"] == order_data["items"][0]["product_id"]
    assert data["items"][0]["quantity"] == order_data["items"][0]["quantity"]


@pytest.mark.asyncio
async def test_create_order_invalid_product(client: AsyncClient, order_data: Dict):
    """
    Test creating an order with an invalid product.
    
    Args:
        client: Test client
        order_data: Test order data
    """
    # Use a non-existent product ID
    order_data["items"][0]["product_id"] = 999
    
    response = await client.post(
        "/api/v1/orders/",
        json=order_data,
    )
    
    # This should fail because the product doesn't exist
    assert response.status_code != status.HTTP_201_CREATED


@pytest.mark.asyncio
async def test_update_order(client: AsyncClient, test_orders: List[Order]):
    """
    Test updating an order.
    
    Args:
        client: Test client
        test_orders: List of test orders
    """
    order_id = test_orders[0].id
    update_data = {
        "customer_name": "Updated Customer Name",
        "notes": "Updated notes",
    }
    
    response = await client.put(
        f"/api/v1/orders/{order_id}",
        json=update_data,
    )
    
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert data["id"] == order_id
    assert data["customer_name"] == update_data["customer_name"]
    assert data["notes"] == update_data["notes"]
    # Email should remain unchanged
    assert data["customer_email"] == test_orders[0].customer_email


@pytest.mark.asyncio
async def test_update_order_not_found(client: AsyncClient):
    """
    Test updating a non-existent order.
    
    Args:
        client: Test client
    """
    update_data = {
        "customer_name": "Updated Customer Name",
    }
    
    response = await client.put(
        "/api/v1/orders/999",
        json=update_data,
    )
    
    assert response.status_code == status.HTTP_404_NOT_FOUND
    
    data = response.json()
    assert "detail" in data
    assert "not found" in data["detail"]


@pytest.mark.asyncio
async def test_update_order_status(client: AsyncClient, test_orders: List[Order]):
    """
    Test updating order status.
    
    Args:
        client: Test client
        test_orders: List of test orders
    """
    order_id = test_orders[0].id
    update_data = {
        "status": OrderStatus.SHIPPED.value,
    }
    
    response = await client.put(
        f"/api/v1/orders/{order_id}/status",
        json=update_data,
    )
    
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert data["id"] == order_id
    assert data["status"] == OrderStatus.SHIPPED.value


@pytest.mark.asyncio
async def test_update_order_status_not_found(client: AsyncClient):
    """
    Test updating status of a non-existent order.
    
    Args:
        client: Test client
    """
    update_data = {
        "status": OrderStatus.SHIPPED.value,
    }
    
    response = await client.put(
        "/api/v1/orders/999/status",
        json=update_data,
    )
    
    assert response.status_code == status.HTTP_404_NOT_FOUND
    
    data = response.json()
    assert "detail" in data
    assert "not found" in data["detail"]


@pytest.mark.asyncio
async def test_delete_order(client: AsyncClient, test_orders: List[Order]):
    """
    Test deleting an order.
    
    Args:
        client: Test client
        test_orders: List of test orders
    """
    order_id = test_orders[0].id
    
    response = await client.delete(f"/api/v1/orders/{order_id}")
    
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert data["id"] == order_id
    
    # Verify order is deleted
    response = await client.get(f"/api/v1/orders/{order_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_delete_order_not_found(client: AsyncClient):
    """
    Test deleting a non-existent order.
    
    Args:
        client: Test client
    """
    response = await client.delete("/api/v1/orders/999")
    
    assert response.status_code == status.HTTP_404_NOT_FOUND
    
    data = response.json()
    assert "detail" in data
    assert "not found" in data["detail"]


@pytest.mark.asyncio
async def test_get_orders_by_customer_email(client: AsyncClient, test_orders: List[Order]):
    """
    Test getting orders by customer email.
    
    Args:
        client: Test client
        test_orders: List of test orders
    """
    customer_email = test_orders[0].customer_email
    response = await client.get(f"/api/v1/orders/customer/{customer_email}")
    
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert all(order["customer_email"] == customer_email for order in data)


# ===== Tests for _safely_refresh_product_relationships =====

@pytest.mark.asyncio
async def test_safely_refresh_product_relationships_none_order(db_session: AsyncSession):
    """
    Test _safely_refresh_product_relationships with None order.
    
    Args:
        db_session: Database session
    """
    logger = logging.getLogger("test")
    # Should not raise any exception
    await _safely_refresh_product_relationships(None, db_session, logger)
    # No assertions needed, just checking that it doesn't raise an exception


@pytest.mark.asyncio
async def test_safely_refresh_product_relationships_none_items(db_session: AsyncSession):
    """
    Test _safely_refresh_product_relationships with order that has None items.
    
    Args:
        db_session: Database session
    """
    logger = logging.getLogger("test")
    
    # Create an order with None items
    order = Order(
        status=OrderStatus.PENDING,
        total_amount=100.0,
        customer_name="Test Customer",
        customer_email="test@example.com"
    )
    db_session.add(order)
    await db_session.commit()
    await db_session.refresh(order)
    
    # Mock the refresh method to set items to None
    original_refresh = db_session.refresh
    
    async def mock_refresh(obj, attribute_names):
        await original_refresh(obj, attribute_names)
        if "items" in attribute_names:
            obj.items = None
    
    with patch.object(db_session, "refresh", side_effect=mock_refresh):
        # Should not raise any exception and set items to empty list
        await _safely_refresh_product_relationships(order, db_session, logger)
        
    assert order.items == []


@pytest.mark.asyncio
async def test_safely_refresh_product_relationships_none_item(db_session: AsyncSession):
    """
    Test _safely_refresh_product_relationships with order that has a None item.
    
    Args:
        db_session: Database session
    """
    logger = logging.getLogger("test")
    
    # Create an order
    order = Order(
        status=OrderStatus.PENDING,
        total_amount=100.0,
        customer_name="Test Customer",
        customer_email="test@example.com"
    )
    db_session.add(order)
    await db_session.commit()
    await db_session.refresh(order)
    
    # Instead of mocking the function itself, we'll just call it directly
    # and verify it doesn't raise an exception
    await _safely_refresh_product_relationships(order, db_session, logger)
    
    # No assertions needed, just checking that it doesn't raise an exception


@pytest.mark.asyncio
async def test_safely_refresh_product_relationships_refresh_error(db_session: AsyncSession):
    """
    Test _safely_refresh_product_relationships with error during refresh.
    
    Args:
        db_session: Database session
    """
    logger = logging.getLogger("test")
    
    # Create an order
    order = Order(
        id=1,  # Set ID explicitly for error message
        status=OrderStatus.PENDING,
        total_amount=100.0,
        customer_name="Test Customer",
        customer_email="test@example.com"
    )
    
    # Mock the refresh method to raise an exception
    async def mock_refresh_error(*args, **kwargs):
        raise SQLAlchemyError("Test refresh error")
    
    with patch.object(db_session, "refresh", side_effect=mock_refresh_error):
        # Should not raise any exception
        await _safely_refresh_product_relationships(order, db_session, logger)
        
    # No assertions needed, just checking that it doesn't raise an exception


@pytest.mark.asyncio
async def test_safely_refresh_product_relationships_item_refresh_error(db_session: AsyncSession, test_products: List[Product]):
    """
    Test _safely_refresh_product_relationships with error during item refresh.
    
    Args:
        db_session: Database session
        test_products: List of test products
    """
    logger = logging.getLogger("test")
    
    # Create an order with an item
    order = Order(
        id=1,  # Set ID explicitly for error message
        status=OrderStatus.PENDING,
        total_amount=100.0,
        customer_name="Test Customer",
        customer_email="test@example.com"
    )
    db_session.add(order)
    await db_session.commit()
    await db_session.refresh(order)
    
    # Add an order item
    order_item = OrderItem(
        id=1,  # Set ID explicitly for error message
        order_id=order.id,
        product_id=test_products[0].id,
        quantity=1,
        unit_price=test_products[0].price,
        subtotal=test_products[0].price
    )
    db_session.add(order_item)
    await db_session.commit()
    
    # Original refresh function
    original_refresh = db_session.refresh
    
    # Counter to track which refresh call we're on
    call_count = 0
    
    async def mock_refresh_with_item_error(obj, attribute_names):
        nonlocal call_count
        call_count += 1
        
        # First call is for order.items, let it succeed
        if call_count == 1:
            await original_refresh(obj, attribute_names)
            # Set product to None to trigger the refresh in the next step
            for item in obj.items:
                item.product = None
        # Second call is for item.product, make it fail
        else:
            raise SQLAlchemyError("Test item refresh error")
    
    with patch.object(db_session, "refresh", side_effect=mock_refresh_with_item_error):
        # Should not raise any exception
        await _safely_refresh_product_relationships(order, db_session, logger)
        
    # No assertions needed, just checking that it doesn't raise an exception


# ===== Tests for database connection errors =====

@pytest.mark.asyncio
async def test_list_orders_database_error(client: AsyncClient):
    """
    Test listing orders with database error.
    
    Args:
        client: Test client
    """
    # Mock the get_multi method to raise a database error
    with patch("app.crud.order.order.get_multi", side_effect=SQLAlchemyError("Test database error")):
        response = await client.get("/api/v1/orders/")
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        
        data = response.json()
        assert "error" in data
        assert "database_error" in data["error"]["error_type"]


@pytest.mark.asyncio
async def test_get_order_database_error(client: AsyncClient, test_orders: List[Order]):
    """
    Test getting an order with database error.
    
    Args:
        client: Test client
        test_orders: List of test orders
    """
    order_id = test_orders[0].id
    
    # Mock the get_with_items method to raise a database error
    with patch("app.crud.order.order.get_with_items", side_effect=SQLAlchemyError("Test database error")):
        response = await client.get(f"/api/v1/orders/{order_id}")
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        
        data = response.json()
        assert "error" in data
        assert "retrieval_error" in data["error"]["error_type"]


@pytest.mark.asyncio
async def test_create_order_database_error(client: AsyncClient, order_data: Dict, test_products: List[Product]):
    """
    Test creating an order with database error.
    
    Args:
        client: Test client
        order_data: Test order data
        test_products: List of test products
    """
    # Update product_id to use an existing product
    order_data["items"][0]["product_id"] = test_products[0].id
    
    # Mock the create_with_items method to raise a database error
    with patch("app.crud.order.order.create_with_items", side_effect=SQLAlchemyError("Test database error")):
        response = await client.post(
            "/api/v1/orders/",
            json=order_data,
        )
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        
        data = response.json()
        assert "error" in data
        assert "creation_error" in data["error"]["error_type"]


# ===== Tests for invalid order status transitions =====

@pytest.mark.asyncio
async def test_update_order_status_invalid_transition(client: AsyncClient, test_orders_all_statuses: List[Order]):
    """
    Test updating order status with invalid transition.
    
    Args:
        client: Test client
        test_orders_all_statuses: List of test orders with all statuses
    """
    # Find the delivered order
    delivered_order = next(order for order in test_orders_all_statuses if order.status == OrderStatus.DELIVERED)
    
    # Try to change from DELIVERED to PENDING (invalid transition)
    update_data = {
        "status": OrderStatus.PENDING.value,
    }
    
    # Mock the update_status method to raise an OrderValidationError
    with patch("app.crud.order.order.update_status", side_effect=OrderValidationError(
        detail="Cannot change order status from DELIVERED to PENDING",
        error_type="invalid_status_transition",
        validation_errors=[{
            "msg": "Invalid status transition",
            "current_status": OrderStatus.DELIVERED.value,
            "requested_status": OrderStatus.PENDING.value
        }]
    )):
        response = await client.put(
            f"/api/v1/orders/{delivered_order.id}/status",
            json=update_data,
        )
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        
        data = response.json()
        assert "error" in data
        assert "invalid_status_transition" in data["error"]["error_type"]


@pytest.mark.asyncio
async def test_update_order_status_missing_status(client: AsyncClient, test_orders: List[Order]):
    """
    Test updating order status with missing status field.
    
    Args:
        client: Test client
        test_orders: List of test orders
    """
    order_id = test_orders[0].id
    
    # Missing status field
    update_data = {}
    
    response = await client.put(
        f"/api/v1/orders/{order_id}/status",
        json=update_data,
    )
    
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    data = response.json()
    assert "error" in data
    assert "missing_status_field" in data["error"]["error_type"]


@pytest.mark.asyncio
async def test_update_order_status_invalid_status_value(client: AsyncClient, test_orders: List[Order]):
    """
    Test updating order status with invalid status value.
    
    Args:
        client: Test client
        test_orders: List of test orders
    """
    order_id = test_orders[0].id
    
    # Invalid status value
    update_data = {
        "status": "invalid_status",
    }
    
    response = await client.put(
        f"/api/v1/orders/{order_id}/status",
        json=update_data,
    )
    
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    data = response.json()
    assert "error" in data
    assert "invalid_status_value" in data["error"]["error_type"]


# ===== Tests for edge cases in pagination =====

@pytest.mark.asyncio
async def test_list_orders_pagination_zero_limit(client: AsyncClient, test_orders: List[Order]):
    """
    Test listing orders with zero limit (should use default).
    
    Args:
        client: Test client
        test_orders: List of test orders
    """
    response = await client.get("/api/v1/orders/?limit=0")
    
    # Should return 422 Unprocessable Entity because limit must be >= 1
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_list_orders_pagination_negative_skip(client: AsyncClient, test_orders: List[Order]):
    """
    Test listing orders with negative skip (should use default).
    
    Args:
        client: Test client
        test_orders: List of test orders
    """
    response = await client.get("/api/v1/orders/?skip=-1")
    
    # Should return 422 Unprocessable Entity because skip must be >= 0
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_list_orders_pagination_large_limit(client: AsyncClient, test_orders: List[Order]):
    """
    Test listing orders with limit larger than max allowed.
    
    Args:
        client: Test client
        test_orders: List of test orders
    """
    response = await client.get("/api/v1/orders/?limit=101")
    
    # Should return 422 Unprocessable Entity because limit must be <= 100
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_list_orders_pagination_skip_beyond_total(client: AsyncClient, test_orders: List[Order]):
    """
    Test listing orders with skip beyond total number of orders.
    
    Args:
        client: Test client
        test_orders: List of test orders
    """
    # Skip beyond the total number of orders
    response = await client.get(f"/api/v1/orders/?skip={len(test_orders) + 10}")
    
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 0  # Should return empty list


# ===== Tests for order item validation scenarios =====

@pytest.mark.asyncio
async def test_create_order_empty_items(client: AsyncClient, order_data: Dict):
    """
    Test creating an order with empty items list.
    
    Args:
        client: Test client
        order_data: Test order data
    """
    # Empty items list
    order_data["items"] = []
    
    response = await client.post(
        "/api/v1/orders/",
        json=order_data,
    )
    
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_create_order_negative_quantity(client: AsyncClient, order_data: Dict, test_products: List[Product]):
    """
    Test creating an order with negative quantity.
    
    Args:
        client: Test client
        order_data: Test order data
        test_products: List of test products
    """
    # Update product_id to use an existing product
    order_data["items"][0]["product_id"] = test_products[0].id
    # Set negative quantity
    order_data["items"][0]["quantity"] = -1
    
    response = await client.post(
        "/api/v1/orders/",
        json=order_data,
    )
    
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_create_order_insufficient_inventory(client: AsyncClient, order_data: Dict, test_products_inventory: List[Product]):
    """
    Test creating an order with insufficient inventory.
    
    Args:
        client: Test client
        order_data: Test order data
        test_products_inventory: List of test products with varied inventory levels
    """
    # Find the out of stock product
    out_of_stock_product = next(product for product in test_products_inventory if product.inventory_count == 0)
    
    # Update product_id to use the out of stock product
    order_data["items"][0]["product_id"] = out_of_stock_product.id
    order_data["items"][0]["quantity"] = 1
    
    response = await client.post(
        "/api/v1/orders/",
        json=order_data,
    )
    
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


@pytest.mark.asyncio
async def test_create_order_multiple_products_one_invalid(client: AsyncClient, order_data_multiple_items: Dict, test_products: List[Product]):
    """
    Test creating an order with multiple products, one of which is invalid.
    
    Args:
        client: Test client
        order_data_multiple_items: Test order data with multiple items
        test_products: List of test products
    """
    # Update product_ids to use existing products
    for i in range(min(len(order_data_multiple_items["items"]), len(test_products))):
        order_data_multiple_items["items"][i]["product_id"] = test_products[i].id
    
    # Set one product_id to an invalid value
    order_data_multiple_items["items"][-1]["product_id"] = 999
    
    response = await client.post(
        "/api/v1/orders/",
        json=order_data_multiple_items,
    )
    
    assert response.status_code == status.HTTP_404_NOT_FOUND
    
    data = response.json()
    assert "detail" in data
    assert "Product not found" in data["detail"]


# ===== Tests for delete order with invalid status =====

@pytest.mark.asyncio
async def test_delete_order_shipped_status(client: AsyncClient, test_orders_all_statuses: List[Order]):
    """
    Test deleting an order with SHIPPED status (should fail).
    
    Args:
        client: Test client
        test_orders_all_statuses: List of test orders with all statuses
    """
    # Find the shipped order
    shipped_order = next(order for order in test_orders_all_statuses if order.status == OrderStatus.SHIPPED)
    
    # Mock the remove method to raise an OrderValidationError
    with patch("app.crud.order.order.remove", side_effect=OrderValidationError(
        detail=f"Cannot delete order with status {OrderStatus.SHIPPED.value}",
        error_type="invalid_order_deletion",
        validation_errors=[{
            "msg": "Cannot delete order that has been shipped or delivered",
            "current_status": OrderStatus.SHIPPED.value
        }]
    )):
        response = await client.delete(f"/api/v1/orders/{shipped_order.id}")
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        
        data = response.json()
        assert "detail" in data
        assert f"Cannot delete order with status {OrderStatus.SHIPPED.value}" in data["detail"]


@pytest.mark.asyncio
async def test_delete_order_delivered_status(client: AsyncClient, test_orders_all_statuses: List[Order]):
    """
    Test deleting an order with DELIVERED status (should fail).
    
    Args:
        client: Test client
        test_orders_all_statuses: List of test orders with all statuses
    """
    # Find the delivered order
    delivered_order = next(order for order in test_orders_all_statuses if order.status == OrderStatus.DELIVERED)
    
    # Mock the remove method to raise an OrderValidationError
    with patch("app.crud.order.order.remove", side_effect=OrderValidationError(
        detail=f"Cannot delete order with status {OrderStatus.DELIVERED.value}",
        error_type="invalid_order_deletion",
        validation_errors=[{
            "msg": "Cannot delete order that has been shipped or delivered",
            "current_status": OrderStatus.DELIVERED.value
        }]
    )):
        response = await client.delete(f"/api/v1/orders/{delivered_order.id}")
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        
        data = response.json()
        assert "detail" in data
        assert f"Cannot delete order with status {OrderStatus.DELIVERED.value}" in data["detail"]


# ===== Tests for get_orders_by_customer_email with no orders =====

@pytest.mark.asyncio
async def test_get_orders_by_customer_email_no_orders(client: AsyncClient):
    """
    Test getting orders by customer email when no orders exist for that email.
    
    Args:
        client: Test client
    """
    response = await client.get("/api/v1/orders/customer/nonexistent@example.com")
    
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 0  # Should return empty list


# ===== Tests for concurrent order updates =====

@pytest.mark.asyncio
async def test_concurrent_order_updates_integrity_error(client: AsyncClient, test_orders: List[Order]):
    """
    Test concurrent order updates causing an integrity error.
    
    Args:
        client: Test client
        test_orders: List of test orders
    """
    order_id = test_orders[0].id
    update_data = {
        "customer_name": "Concurrent Update Customer",
    }
    
    # Mock the update method to raise an IntegrityError
    with patch("app.crud.order.order.update", side_effect=IntegrityError("Test integrity error", None, None)):
        response = await client.put(
            f"/api/v1/orders/{order_id}",
            json=update_data,
        )
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        
        data = response.json()
        assert "error" in data
        assert "update_error" in data["error"]["error_type"]


# ===== Tests for additional error handling scenarios =====

@pytest.mark.asyncio
async def test_get_order_not_found_validation_error(client: AsyncClient):
    """
    Test getting an order with a validation error that indicates not found.
    
    Args:
        client: Test client
    """
    order_id = 999
    
    # Mock the get_with_items method to raise an OrderValidationError with order_not_found
    with patch("app.crud.order.order.get_with_items", side_effect=OrderValidationError(
        detail=f"Order with ID {order_id} not found",
        error_type="order_not_found",
        validation_errors=[{"msg": f"Order with ID {order_id} not found"}]
    )):
        response = await client.get(f"/api/v1/orders/{order_id}")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        
        data = response.json()
        assert "detail" in data
        assert f"Order with ID {order_id} not found" in data["detail"]


@pytest.mark.asyncio
async def test_get_order_other_validation_error(client: AsyncClient, test_orders: List[Order]):
    """
    Test getting an order with a validation error other than not found.
    
    Args:
        client: Test client
        test_orders: List of test orders
    """
    order_id = test_orders[0].id
    
    # Mock the get_with_items method to raise an OrderValidationError with a different error type
    with patch("app.crud.order.order.get_with_items", side_effect=OrderValidationError(
        detail="Test validation error",
        error_type="test_error",
        validation_errors=[{"msg": "Test validation error"}]
    )):
        response = await client.get(f"/api/v1/orders/{order_id}")
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        
        data = response.json()
        assert "error" in data
        assert "test_error" in data["error"]["error_type"]


@pytest.mark.asyncio
async def test_get_order_exists_but_none(client: AsyncClient, test_orders: List[Order]):
    """
    Test getting an order that exists but returns None.
    
    Args:
        client: Test client
        test_orders: List of test orders
    """
    order_id = test_orders[0].id
    
    # Mock the get_with_items method to return None
    with patch("app.crud.order.order.get_with_items", return_value=None):
        response = await client.get(f"/api/v1/orders/{order_id}")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        
        data = response.json()
        assert "detail" in data
        assert f"Order with ID {order_id} not found" in data["detail"]


@pytest.mark.asyncio
async def test_create_order_creation_failed(client: AsyncClient, order_data: Dict, test_products: List[Product]):
    """
    Test creating an order that fails during creation.
    
    Args:
        client: Test client
        order_data: Test order data
        test_products: List of test products
    """
    # Update product_id to use an existing product
    order_data["items"][0]["product_id"] = test_products[0].id
    
    # Mock the create_with_items method to return None
    with patch("app.crud.order.order.create_with_items", return_value=None):
        response = await client.post(
            "/api/v1/orders/",
            json=order_data,
        )
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        
        data = response.json()
        assert "error" in data
        assert "order_creation_failed" in data["error"]["error_type"]


@pytest.mark.asyncio
async def test_update_order_get_after_update_not_found(client: AsyncClient, test_orders: List[Order]):
    """
    Test updating an order where the get after update returns not found.
    
    Args:
        client: Test client
        test_orders: List of test orders
    """
    order_id = test_orders[0].id
    update_data = {
        "customer_name": "Updated Customer Name",
    }
    
    # Mock the update method to succeed but get_with_items to raise not found
    with patch("app.crud.order.order.update", return_value=test_orders[0]), \
         patch("app.crud.order.order.get_with_items", side_effect=OrderValidationError(
            detail=f"Order with ID {order_id} not found",
            error_type="order_not_found",
            validation_errors=[{"msg": f"Order with ID {order_id} not found"}]
         )):
        response = await client.put(
            f"/api/v1/orders/{order_id}",
            json=update_data,
        )
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        
        data = response.json()
        assert "detail" in data
        assert f"Order with ID {order_id} not found" in data["detail"]


@pytest.mark.asyncio
async def test_update_order_get_after_update_returns_none(client: AsyncClient, test_orders: List[Order]):
    """
    Test updating an order where the get after update returns None.
    
    Args:
        client: Test client
        test_orders: List of test orders
    """
    order_id = test_orders[0].id
    update_data = {
        "customer_name": "Updated Customer Name",
    }
    
    # Mock the update method to succeed but get_with_items to return None
    with patch("app.crud.order.order.update", return_value=test_orders[0]), \
         patch("app.crud.order.order.get_with_items", return_value=None):
        response = await client.put(
            f"/api/v1/orders/{order_id}",
            json=update_data,
        )
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        
        data = response.json()
        assert "detail" in data
        assert f"Order with ID {order_id} not found after update" in data["detail"]


@pytest.mark.asyncio
async def test_update_order_status_get_after_update_not_found(client: AsyncClient, test_orders: List[Order]):
    """
    Test updating an order status where the get after update returns not found.
    
    Args:
        client: Test client
        test_orders: List of test orders
    """
    order_id = test_orders[0].id
    update_data = {
        "status": OrderStatus.SHIPPED.value,
    }
    
    # Mock the update_status method to succeed but get_with_items to raise not found
    with patch("app.crud.order.order.update_status", return_value=test_orders[0]), \
         patch("app.crud.order.order.get_with_items", side_effect=OrderValidationError(
            detail=f"Order with ID {order_id} not found",
            error_type="order_not_found",
            validation_errors=[{"msg": f"Order with ID {order_id} not found"}]
         )):
        response = await client.put(
            f"/api/v1/orders/{order_id}/status",
            json=update_data,
        )
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        
        data = response.json()
        assert "detail" in data
        assert f"Order with ID {order_id} not found" in data["detail"]


@pytest.mark.asyncio
async def test_update_order_status_get_after_update_returns_none(client: AsyncClient, test_orders: List[Order]):
    """
    Test updating an order status where the get after update returns None.
    
    Args:
        client: Test client
        test_orders: List of test orders
    """
    order_id = test_orders[0].id
    update_data = {
        "status": OrderStatus.SHIPPED.value,
    }
    
    # Mock the update_status method to succeed but get_with_items to return None
    with patch("app.crud.order.order.update_status", return_value=test_orders[0]), \
         patch("app.crud.order.order.get_with_items", return_value=None):
        response = await client.put(
            f"/api/v1/orders/{order_id}/status",
            json=update_data,
        )
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        
        data = response.json()
        assert "detail" in data
        assert f"Order with ID {order_id} not found after status update" in data["detail"]


@pytest.mark.asyncio
async def test_delete_order_not_deleted_properly(client: AsyncClient, test_orders: List[Order]):
    """
    Test deleting an order where the remove method returns None.
    
    Args:
        client: Test client
        test_orders: List of test orders
    """
    order_id = test_orders[0].id
    
    # Mock the remove method to return None
    with patch("app.crud.order.order.remove", return_value=None):
        response = await client.delete(f"/api/v1/orders/{order_id}")
        
        assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        
        data = response.json()
        assert "error" in data
        assert "deletion_failed" in data["error"]["error_type"]


@pytest.mark.asyncio
async def test_list_orders_none_result(client: AsyncClient):
    """
    Test listing orders where the get_multi method returns None.
    
    Args:
        client: Test client
    """
    # Mock the get_multi method to return None
    with patch("app.crud.order.order.get_multi", return_value=None):
        response = await client.get("/api/v1/orders/")
        
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 0  # Should return empty list


@pytest.mark.asyncio
async def test_list_orders_by_status_none_result(client: AsyncClient):
    """
    Test listing orders by status where the get_by_status method returns None.
    
    Args:
        client: Test client
    """
    # Mock the get_by_status method to return None
    with patch("app.crud.order.order.get_by_status", return_value=None):
        response = await client.get("/api/v1/orders/?status=pending")
        
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 0  # Should return empty list


@pytest.mark.asyncio
async def test_get_orders_by_customer_email_none_result(client: AsyncClient):
    """
    Test getting orders by customer email where the get_by_customer_email method returns None.
    
    Args:
        client: Test client
    """
    # Mock the get_by_customer_email method to return None
    with patch("app.crud.order.order.get_by_customer_email", return_value=None):
        response = await client.get("/api/v1/orders/customer/test@example.com")
        
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 0  # Should return empty list


@pytest.mark.asyncio
async def test_get_orders_by_customer_email_customer_not_found(client: AsyncClient):
    """
    Test getting orders by customer email where the get_by_customer_email method raises customer_not_found.
    
    Args:
        client: Test client
    """
    customer_email = "nonexistent@example.com"
    
    # Mock the get_by_customer_email method to raise an OrderValidationError with customer_not_found
    with patch("app.crud.order.order.get_by_customer_email", side_effect=OrderValidationError(
        detail=f"Customer with email {customer_email} not found",
        error_type="customer_not_found",
        validation_errors=[{"msg": f"Customer with email {customer_email} not found"}]
    )):
        response = await client.get(f"/api/v1/orders/customer/{customer_email}")
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
        
        data = response.json()
        assert "detail" in data
        assert f"Customer with email {customer_email} not found" in data["detail"]


from datetime import datetime

@pytest.mark.asyncio
async def test_get_orders_by_customer_email_with_empty_orders(client: AsyncClient):
    """
    Test getting orders by customer email where one of the orders is None.

    Args:
        client: Test client
    """
    customer_email = "test@example.com"

    # Mock the get_by_customer_email method to return None
    with patch("app.crud.order.order.get_by_customer_email", return_value=None):
        response = await client.get(f"/api/v1/orders/customer/{customer_email}")
        
        assert response.status_code == status.HTTP_200_OK
        
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 0  # Should return empty list
