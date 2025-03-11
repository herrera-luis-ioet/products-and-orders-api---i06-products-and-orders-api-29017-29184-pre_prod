"""
Tests for product API endpoints.

This module contains tests for the product API endpoints, including
tests for creating, reading, updating, and deleting products.
"""

import json
from typing import Dict, List

import pytest
from fastapi import status
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.product import Product


@pytest.mark.asyncio
async def test_list_products(client: AsyncClient, test_products: List[Product]):
    """
    Test listing products.
    
    Args:
        client: Test client
        test_products: List of test products
    """
    response = await client.get("/api/v1/products/")
    
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == len(test_products)
    
    # Check that all products are returned
    product_ids = [product["id"] for product in data]
    for product in test_products:
        assert product.id in product_ids


@pytest.mark.asyncio
async def test_list_products_pagination(client: AsyncClient, test_products: List[Product]):
    """
    Test listing products with pagination.
    
    Args:
        client: Test client
        test_products: List of test products
    """
    # Test with skip=1, limit=1
    response = await client.get("/api/v1/products/?skip=1&limit=1")
    
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 1
    
    # Test with skip=0, limit=2
    response = await client.get("/api/v1/products/?skip=0&limit=2")
    
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2


@pytest.mark.asyncio
async def test_get_product(client: AsyncClient, test_products: List[Product]):
    """
    Test getting a specific product.
    
    Args:
        client: Test client
        test_products: List of test products
    """
    product_id = test_products[0].id
    response = await client.get(f"/api/v1/products/{product_id}")
    
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert data["id"] == product_id
    assert data["name"] == test_products[0].name
    assert data["sku"] == test_products[0].sku
    assert float(data["price"]) == float(test_products[0].price)
    assert data["inventory_count"] == test_products[0].inventory_count


@pytest.mark.asyncio
async def test_get_product_not_found(client: AsyncClient):
    """
    Test getting a non-existent product.
    
    Args:
        client: Test client
    """
    response = await client.get("/api/v1/products/999")
    
    assert response.status_code == status.HTTP_404_NOT_FOUND
    
    data = response.json()
    assert "detail" in data
    assert "not found" in data["detail"]


@pytest.mark.asyncio
async def test_create_product(client: AsyncClient, product_data: Dict):
    """
    Test creating a product.
    
    Args:
        client: Test client
        product_data: Test product data
    """
    response = await client.post(
        "/api/v1/products/",
        json=product_data,
    )
    
    assert response.status_code == status.HTTP_201_CREATED
    
    data = response.json()
    assert data["name"] == product_data["name"]
    assert data["sku"] == product_data["sku"]
    assert float(data["price"]) == float(product_data["price"])
    assert data["inventory_count"] == product_data["inventory_count"]
    assert "id" in data
    assert data["id"] > 0


@pytest.mark.asyncio
async def test_create_product_duplicate_sku(client: AsyncClient, product_data: Dict, test_products: List[Product]):
    """
    Test creating a product with a duplicate SKU.
    
    Args:
        client: Test client
        product_data: Test product data
        test_products: List of test products
    """
    # Use an existing SKU
    product_data["sku"] = test_products[0].sku
    
    response = await client.post(
        "/api/v1/products/",
        json=product_data,
    )
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    data = response.json()
    assert "detail" in data
    assert "already exists" in data["detail"]


@pytest.mark.asyncio
async def test_update_product(client: AsyncClient, test_products: List[Product]):
    """
    Test updating a product.
    
    Args:
        client: Test client
        test_products: List of test products
    """
    product_id = test_products[0].id
    update_data = {
        "name": "Updated Product Name",
        "price": 29.99,
        "inventory_count": 50,
    }
    
    response = await client.put(
        f"/api/v1/products/{product_id}",
        json=update_data,
    )
    
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert data["id"] == product_id
    assert data["name"] == update_data["name"]
    assert float(data["price"]) == float(update_data["price"])
    assert data["inventory_count"] == update_data["inventory_count"]
    # SKU should remain unchanged
    assert data["sku"] == test_products[0].sku


@pytest.mark.asyncio
async def test_update_product_not_found(client: AsyncClient):
    """
    Test updating a non-existent product.
    
    Args:
        client: Test client
    """
    update_data = {
        "name": "Updated Product Name",
        "price": 29.99,
    }
    
    response = await client.put(
        "/api/v1/products/999",
        json=update_data,
    )
    
    assert response.status_code == status.HTTP_404_NOT_FOUND
    
    data = response.json()
    assert "detail" in data
    assert "not found" in data["detail"]


@pytest.mark.asyncio
async def test_update_product_duplicate_sku(client: AsyncClient, test_products: List[Product]):
    """
    Test updating a product with a duplicate SKU.
    
    Args:
        client: Test client
        test_products: List of test products
    """
    product_id = test_products[0].id
    update_data = {
        "sku": test_products[1].sku,  # Use SKU from another product
    }
    
    response = await client.put(
        f"/api/v1/products/{product_id}",
        json=update_data,
    )
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    data = response.json()
    assert "detail" in data
    assert "already exists" in data["detail"]


@pytest.mark.asyncio
async def test_delete_product(client: AsyncClient, test_products: List[Product]):
    """
    Test deleting a product.
    
    Args:
        client: Test client
        test_products: List of test products
    """
    product_id = test_products[0].id
    
    response = await client.delete(f"/api/v1/products/{product_id}")
    
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert data["id"] == product_id
    
    # Verify product is deleted
    response = await client.get(f"/api/v1/products/{product_id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND


@pytest.mark.asyncio
async def test_delete_product_not_found(client: AsyncClient):
    """
    Test deleting a non-existent product.
    
    Args:
        client: Test client
    """
    response = await client.delete("/api/v1/products/999")
    
    assert response.status_code == status.HTTP_404_NOT_FOUND
    
    data = response.json()
    assert "detail" in data
    assert "not found" in data["detail"]


@pytest.mark.asyncio
async def test_search_products(client: AsyncClient, test_products: List[Product]):
    """
    Test searching products.
    
    Args:
        client: Test client
        test_products: List of test products
    """
    # Search by name
    response = await client.get("/api/v1/products/search/?query=Product 1")
    
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert any(product["name"] == "Product 1" for product in data)
    
    # Search by description
    response = await client.get("/api/v1/products/search/?query=Description for Product 2")
    
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert any(product["name"] == "Product 2" for product in data)


@pytest.mark.asyncio
async def test_get_products_by_category(client: AsyncClient, test_products: List[Product]):
    """
    Test getting products by category.
    
    Args:
        client: Test client
        test_products: List of test products
    """
    response = await client.get("/api/v1/products/category/Category 1")
    
    assert response.status_code == status.HTTP_200_OK
    
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert all(product["id"] in [p.id for p in test_products if p.category == "Category 1"] for product in data)