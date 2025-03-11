"""
Pytest configuration and fixtures.

This module provides fixtures for testing the application, including
database fixtures, API client fixtures, and test data fixtures.

The database initialization process:
1. Create a file-based SQLite database for testing
2. Import all models to ensure they're registered with SQLAlchemy
3. Create all tables using Base.metadata.create_all
4. Reset the database between tests to ensure a clean state
"""

import asyncio
import os
from typing import AsyncGenerator, Dict, Generator, List

import pytest
import pytest_asyncio
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from app import __app_name__, __version__
from app.api.v1.api import api_router
from app.config import Settings, settings
from app.database import Base, get_db, init_db
# Explicitly import all models to ensure they're registered with SQLAlchemy
from app.models.order import Order, OrderItem, OrderStatus
from app.models.product import Product


# Test settings with file-based SQLite database for testing
@pytest.fixture(scope="session")
def test_settings() -> Settings:
    """
    Create test settings with file-based SQLite database for testing.
    
    Returns:
        Settings: Test settings
    """
    # Use a file-based SQLite database for testing
    # This ensures that the database persists across connections
    return Settings(
        ENV="testing",
        DEBUG=True,
        DATABASE_URL="sqlite+aiosqlite:///./test.db",
        SECRET_KEY="test_secret_key",
        PAGINATION_PAGE_SIZE=10,
    )


# Override settings for tests
@pytest.fixture(scope="session", autouse=True)
def override_settings(test_settings: Settings) -> None:
    """
    Override settings for tests.
    
    Args:
        test_settings: Test settings
    """
    # Replace the global settings with test settings
    for key, value in test_settings.model_dump().items():
        setattr(settings, key, value)


# Create async engine for tests
@pytest_asyncio.fixture(scope="session")
async def engine():
    """
    Create async engine for tests.
    
    Returns:
        AsyncEngine: SQLAlchemy async engine
    """
    # Remove test.db if it exists
    if os.path.exists("./test.db"):
        os.remove("./test.db")
    
    # Create engine with the test database URL
    engine = create_async_engine(
        settings.DATABASE_URL,
        echo=False,
        future=True,
        poolclass=NullPool,
    )
    
    # Import all models to ensure they're registered with SQLAlchemy
    from app.models.product import Product
    from app.models.order import Order, OrderItem
    
    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    yield engine
    
    # Drop tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    
    # Remove test.db
    if os.path.exists("./test.db"):
        os.remove("./test.db")
    
    await engine.dispose()


# Reset database tables between tests
@pytest_asyncio.fixture(scope="function")
async def reset_db(engine):
    """
    Reset database tables between tests.
    
    This fixture ensures that each test starts with a clean database.
    
    Args:
        engine: SQLAlchemy async engine
    """
    # Drop all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
    
    # Import all models to ensure they're registered with SQLAlchemy
    from app.models.product import Product
    from app.models.order import Order, OrderItem
    
    # Create all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# Create async session for tests
@pytest_asyncio.fixture(scope="function")
async def db_session(engine, reset_db) -> AsyncGenerator[AsyncSession, None]:
    """
    Create async session for tests.
    
    Args:
        engine: SQLAlchemy async engine
        reset_db: Reset database fixture
        
    Yields:
        AsyncSession: SQLAlchemy async session
    """
    # Create session factory
    async_session_factory = sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
        autoflush=False,
    )
    
    async with async_session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


# Override get_db dependency for tests
@pytest_asyncio.fixture(scope="function")
async def override_get_db(db_session: AsyncSession) -> AsyncGenerator:
    """
    Override get_db dependency for tests.
    
    Args:
        db_session: SQLAlchemy async session
        
    Yields:
        AsyncSession: SQLAlchemy async session
    """
    async def _get_test_db():
        try:
            yield db_session
        finally:
            pass
    
    return _get_test_db


# Create test app
@pytest_asyncio.fixture(scope="function")
async def app(override_get_db) -> FastAPI:
    """
    Create test app.
    
    Args:
        override_get_db: Override get_db dependency
        
    Returns:
        FastAPI: FastAPI application
    """
    from app.main import app as main_app
    
    # Override get_db dependency
    main_app.dependency_overrides[get_db] = override_get_db
    
    return main_app


# Create test client
@pytest_asyncio.fixture(scope="function")
async def client(app: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    """
    Create test client.
    
    Args:
        app: FastAPI application
        
    Yields:
        AsyncClient: HTTPX async client
    """
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


# Test product data
@pytest.fixture(scope="function")
def product_data() -> Dict:
    """
    Create test product data.
    
    Returns:
        Dict: Test product data
    """
    return {
        "name": "Test Product",
        "description": "This is a test product",
        "price": 19.99,
        "inventory_count": 100,
        "sku": "TEST-SKU-001",
        "category": "Test Category",
        "image_url": "https://example.com/test-product.jpg",
        "weight": 500,
        "dimensions": "10x20x30 cm",
        "is_active": True,
    }


# Test order data
@pytest.fixture(scope="function")
def order_data() -> Dict:
    """
    Create test order data.
    
    Returns:
        Dict: Test order data
    """
    return {
        "customer_name": "Test Customer",
        "customer_email": "test@example.com",
        "customer_phone": "123-456-7890",
        "shipping_address": "123 Test St, Test City, Test Country",
        "billing_address": "123 Test St, Test City, Test Country",
        "payment_method": "Credit Card",
        "payment_id": "TEST-PAYMENT-001",
        "notes": "This is a test order",
        "items": [
            {
                "product_id": 1,
                "quantity": 2,
                "unit_price": 19.99,
            }
        ],
    }


# Create test products in database
@pytest_asyncio.fixture(scope="function")
async def test_products(db_session: AsyncSession) -> List[Product]:
    """
    Create test products in database.
    
    Args:
        db_session: SQLAlchemy async session
        
    Returns:
        List[Product]: List of test products
    """
    products = [
        Product(
            name="Product 1",
            description="Description for Product 1",
            price=19.99,
            inventory_count=100,
            sku="SKU-001",
            category="Category 1",
            image_url="https://example.com/product1.jpg",
            weight=500,
            dimensions="10x20x30 cm",
            is_active=True,
        ),
        Product(
            name="Product 2",
            description="Description for Product 2",
            price=29.99,
            inventory_count=50,
            sku="SKU-002",
            category="Category 1",
            image_url="https://example.com/product2.jpg",
            weight=750,
            dimensions="15x25x35 cm",
            is_active=True,
        ),
        Product(
            name="Product 3",
            description="Description for Product 3",
            price=39.99,
            inventory_count=25,
            sku="SKU-003",
            category="Category 2",
            image_url="https://example.com/product3.jpg",
            weight=1000,
            dimensions="20x30x40 cm",
            is_active=False,
        ),
    ]
    
    for product in products:
        db_session.add(product)
    
    await db_session.commit()
    
    # Refresh products to get IDs
    for product in products:
        await db_session.refresh(product)
    
    return products


# Create test orders in database
@pytest_asyncio.fixture(scope="function")
async def test_orders(db_session: AsyncSession, test_products: List[Product]) -> List[Order]:
    """
    Create test orders in database.
    
    Args:
        db_session: SQLAlchemy async session
        test_products: List of test products
        
    Returns:
        List[Order]: List of test orders
    """
    orders = [
        Order(
            status=OrderStatus.PENDING,
            total_amount=39.98,  # 2 * 19.99
            customer_name="Customer 1",
            customer_email="customer1@example.com",
            customer_phone="123-456-7890",
            shipping_address="123 Test St, Test City, Test Country",
            billing_address="123 Test St, Test City, Test Country",
            payment_method="Credit Card",
            payment_id="PAYMENT-001",
            notes="Order 1 notes",
        ),
        Order(
            status=OrderStatus.PROCESSING,
            total_amount=59.98,  # 2 * 29.99
            customer_name="Customer 2",
            customer_email="customer2@example.com",
            customer_phone="234-567-8901",
            shipping_address="234 Test St, Test City, Test Country",
            billing_address="234 Test St, Test City, Test Country",
            payment_method="PayPal",
            payment_id="PAYMENT-002",
            notes="Order 2 notes",
        ),
    ]
    
    for order in orders:
        db_session.add(order)
    
    await db_session.commit()
    
    # Refresh orders to get IDs
    for order in orders:
        await db_session.refresh(order)
    
    # Add order items
    order_items = [
        OrderItem(
            order_id=orders[0].id,
            product_id=test_products[0].id,
            quantity=2,
            unit_price=test_products[0].price,
            subtotal=2 * test_products[0].price,
        ),
        OrderItem(
            order_id=orders[1].id,
            product_id=test_products[1].id,
            quantity=2,
            unit_price=test_products[1].price,
            subtotal=2 * test_products[1].price,
        ),
    ]
    
    for order_item in order_items:
        db_session.add(order_item)
    
    await db_session.commit()
    
    return orders
