"""
Tests for order API endpoints.

This module contains tests for the order API endpoints, including
tests for creating, reading, updating, and deleting orders.
"""

import json
from typing import Dict, List

import pytest
from fastapi import status
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.order import Order, OrderStatus
from app.models.product import Product


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