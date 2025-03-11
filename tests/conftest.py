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
import random
from decimal import Decimal
from typing import AsyncGenerator, Dict, Generator, List, Optional

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


# ===== Product Test Data Fixtures =====

# Test product data with all fields
@pytest.fixture(scope="function")
def product_data() -> Dict:
    """
    Create test product data with all fields.
    
    Returns:
        Dict: Test product data with all fields
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


# Test product data with only required fields
@pytest.fixture(scope="function")
def product_data_required_only() -> Dict:
    """
    Create test product data with only required fields.
    
    Returns:
        Dict: Test product data with only required fields
    """
    return {
        "name": "Minimal Product",
        "price": 9.99,
        "inventory_count": 50,
        "sku": "MIN-SKU-001",
    }


# Test product data with invalid fields
@pytest.fixture(scope="function")
def product_data_invalid() -> Dict:
    """
    Create invalid test product data.
    
    Returns:
        Dict: Invalid test product data
    """
    return {
        "name": "Invalid Product",
        "description": "This is an invalid product",
        "price": -10.0,  # Invalid: negative price
        "inventory_count": -5,  # Invalid: negative inventory
        "sku": "",  # Invalid: empty SKU
    }


# Test product data generator
@pytest.fixture(scope="function")
def product_data_generator():
    """
    Generate test product data with customizable fields.
    
    Returns:
        Function: A function that generates product data
    """
    def _generate_product_data(
        name: Optional[str] = None,
        price: Optional[float] = None,
        inventory_count: Optional[int] = None,
        sku: Optional[str] = None,
        category: Optional[str] = None,
        is_active: Optional[bool] = None
    ) -> Dict:
        """
        Generate product data with customizable fields.
        
        Args:
            name: Product name
            price: Product price
            inventory_count: Product inventory count
            sku: Product SKU
            category: Product category
            is_active: Whether the product is active
            
        Returns:
            Dict: Generated product data
        """
        # Generate random values for fields not provided
        random_id = random.randint(1000, 9999)
        
        return {
            "name": name or f"Generated Product {random_id}",
            "description": f"Description for generated product {random_id}",
            "price": price if price is not None else round(random.uniform(5.0, 100.0), 2),
            "inventory_count": inventory_count if inventory_count is not None else random.randint(1, 1000),
            "sku": sku or f"GEN-SKU-{random_id}",
            "category": category or random.choice(["Electronics", "Clothing", "Books", "Home", "Food"]),
            "image_url": f"https://example.com/product{random_id}.jpg",
            "weight": random.randint(100, 5000),
            "dimensions": f"{random.randint(5, 50)}x{random.randint(5, 50)}x{random.randint(5, 50)} cm",
            "is_active": is_active if is_active is not None else True,
        }
    
    return _generate_product_data


# Batch of test product data
@pytest.fixture(scope="function")
def product_data_batch() -> List[Dict]:
    """
    Create a batch of test product data.
    
    Returns:
        List[Dict]: A list of test product data
    """
    return [
        {
            "name": f"Batch Product {i}",
            "description": f"Description for batch product {i}",
            "price": round(random.uniform(5.0, 100.0), 2),
            "inventory_count": random.randint(1, 1000),
            "sku": f"BATCH-SKU-{i:03d}",
            "category": random.choice(["Electronics", "Clothing", "Books", "Home", "Food"]),
            "image_url": f"https://example.com/batch-product{i}.jpg",
            "weight": random.randint(100, 5000),
            "dimensions": f"{random.randint(5, 50)}x{random.randint(5, 50)}x{random.randint(5, 50)} cm",
            "is_active": random.choice([True, False]),
        }
        for i in range(1, 6)  # Create 5 products
    ]


# ===== Order Test Data Fixtures =====

# Test order data with all fields
@pytest.fixture(scope="function")
def order_data() -> Dict:
    """
    Create test order data with all fields.
    
    Returns:
        Dict: Test order data with all fields
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


# Test order data with only required fields
@pytest.fixture(scope="function")
def order_data_required_only() -> Dict:
    """
    Create test order data with only required fields.
    
    Returns:
        Dict: Test order data with only required fields
    """
    return {
        "customer_name": "Minimal Customer",
        "customer_email": "minimal@example.com",
        "items": [
            {
                "product_id": 1,
                "quantity": 1,
            }
        ],
    }


# Test order data with invalid fields
@pytest.fixture(scope="function")
def order_data_invalid() -> Dict:
    """
    Create invalid test order data.
    
    Returns:
        Dict: Invalid test order data
    """
    return {
        "customer_name": "",  # Invalid: empty name
        "customer_email": "invalid-email",  # Invalid: malformed email
        "items": [
            {
                "product_id": 1,
                "quantity": 0,  # Invalid: quantity must be > 0
            }
        ],
    }


# Test order data generator
@pytest.fixture(scope="function")
def order_data_generator():
    """
    Generate test order data with customizable fields.
    
    Returns:
        Function: A function that generates order data
    """
    def _generate_order_data(
        customer_name: Optional[str] = None,
        customer_email: Optional[str] = None,
        items: Optional[List[Dict]] = None,
        status: Optional[OrderStatus] = None,
    ) -> Dict:
        """
        Generate order data with customizable fields.
        
        Args:
            customer_name: Customer name
            customer_email: Customer email
            items: Order items
            status: Order status
            
        Returns:
            Dict: Generated order data
        """
        # Generate random values for fields not provided
        random_id = random.randint(1000, 9999)
        
        # Default items if not provided
        if items is None:
            items = [
                {
                    "product_id": 1,
                    "quantity": random.randint(1, 5),
                    "unit_price": round(random.uniform(5.0, 100.0), 2),
                }
            ]
        
        return {
            "customer_name": customer_name or f"Generated Customer {random_id}",
            "customer_email": customer_email or f"customer{random_id}@example.com",
            "customer_phone": f"{random.randint(100, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}",
            "shipping_address": f"{random.randint(100, 999)} Generated St, City {random_id}, Country",
            "billing_address": f"{random.randint(100, 999)} Generated St, City {random_id}, Country",
            "payment_method": random.choice(["Credit Card", "PayPal", "Bank Transfer", "Cash on Delivery"]),
            "payment_id": f"GEN-PAYMENT-{random_id}",
            "notes": f"Generated order {random_id} notes",
            "items": items,
        }
    
    return _generate_order_data


# Test order with multiple items
@pytest.fixture(scope="function")
def order_data_multiple_items() -> Dict:
    """
    Create test order data with multiple items.
    
    Returns:
        Dict: Test order data with multiple items
    """
    return {
        "customer_name": "Multi-Item Customer",
        "customer_email": "multi@example.com",
        "customer_phone": "987-654-3210",
        "shipping_address": "456 Multi St, Multi City, Multi Country",
        "billing_address": "456 Multi St, Multi City, Multi Country",
        "payment_method": "PayPal",
        "payment_id": "MULTI-PAYMENT-001",
        "notes": "This is a multi-item test order",
        "items": [
            {
                "product_id": 1,
                "quantity": 2,
                "unit_price": 19.99,
            },
            {
                "product_id": 2,
                "quantity": 1,
                "unit_price": 29.99,
            },
            {
                "product_id": 3,
                "quantity": 3,
                "unit_price": 39.99,
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


# Create test products in database with varied inventory levels
@pytest_asyncio.fixture(scope="function")
async def test_products_inventory(db_session: AsyncSession) -> List[Product]:
    """
    Create test products with varied inventory levels.
    
    This fixture creates products with different inventory levels:
    - In stock (high inventory)
    - Low stock (inventory < 10)
    - Out of stock (inventory = 0)
    
    Args:
        db_session: SQLAlchemy async session
        
    Returns:
        List[Product]: List of test products with varied inventory levels
    """
    products = [
        # High inventory product
        Product(
            name="High Inventory Product",
            description="This product has high inventory",
            price=19.99,
            inventory_count=100,
            sku="INV-HIGH-001",
            category="Inventory Test",
            is_active=True,
        ),
        # Low inventory product
        Product(
            name="Low Inventory Product",
            description="This product has low inventory",
            price=29.99,
            inventory_count=5,
            sku="INV-LOW-001",
            category="Inventory Test",
            is_active=True,
        ),
        # Out of stock product
        Product(
            name="Out of Stock Product",
            description="This product is out of stock",
            price=39.99,
            inventory_count=0,
            sku="INV-OUT-001",
            category="Inventory Test",
            is_active=True,
        ),
    ]
    
    for product in products:
        db_session.add(product)
    
    await db_session.commit()
    
    # Refresh products to get IDs
    for product in products:
        await db_session.refresh(product)
    
    return products


# Create test products in database with varied price points
@pytest_asyncio.fixture(scope="function")
async def test_products_price_points(db_session: AsyncSession) -> List[Product]:
    """
    Create test products with varied price points.
    
    This fixture creates products with different price points:
    - Low price
    - Medium price
    - High price
    - Very high price
    
    Args:
        db_session: SQLAlchemy async session
        
    Returns:
        List[Product]: List of test products with varied price points
    """
    products = [
        # Low price product
        Product(
            name="Budget Product",
            description="This is a budget-friendly product",
            price=9.99,
            inventory_count=100,
            sku="PRICE-LOW-001",
            category="Price Test",
            is_active=True,
        ),
        # Medium price product
        Product(
            name="Standard Product",
            description="This is a standard-priced product",
            price=49.99,
            inventory_count=50,
            sku="PRICE-MED-001",
            category="Price Test",
            is_active=True,
        ),
        # High price product
        Product(
            name="Premium Product",
            description="This is a premium-priced product",
            price=199.99,
            inventory_count=25,
            sku="PRICE-HIGH-001",
            category="Price Test",
            is_active=True,
        ),
        # Very high price product
        Product(
            name="Luxury Product",
            description="This is a luxury-priced product",
            price=999.99,
            inventory_count=5,
            sku="PRICE-VHI-001",
            category="Price Test",
            is_active=True,
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


# Create test orders with all different statuses
@pytest_asyncio.fixture(scope="function")
async def test_orders_all_statuses(db_session: AsyncSession, test_products: List[Product]) -> List[Order]:
    """
    Create test orders with all different statuses.
    
    This fixture creates orders with all possible OrderStatus values.
    
    Args:
        db_session: SQLAlchemy async session
        test_products: List of test products
        
    Returns:
        List[Order]: List of test orders with different statuses
    """
    # Create one order for each status
    orders = []
    
    for i, status in enumerate(OrderStatus):
        order = Order(
            status=status,
            total_amount=19.99 * (i + 1),
            customer_name=f"Status Customer {i + 1}",
            customer_email=f"status{i + 1}@example.com",
            customer_phone=f"{i + 1}23-456-7890",
            shipping_address=f"{i + 1}23 Status St, Status City, Status Country",
            billing_address=f"{i + 1}23 Status St, Status City, Status Country",
            payment_method="Credit Card" if i % 2 == 0 else "PayPal",
            payment_id=f"STATUS-PAYMENT-{i + 1:03d}",
            notes=f"Order with status {status.value}",
        )
        orders.append(order)
    
    for order in orders:
        db_session.add(order)
    
    await db_session.commit()
    
    # Refresh orders to get IDs
    for order in orders:
        await db_session.refresh(order)
    
    # Add order items (one item per order)
    order_items = []
    
    for i, order in enumerate(orders):
        # Use modulo to cycle through available products
        product_index = i % len(test_products)
        
        order_item = OrderItem(
            order_id=order.id,
            product_id=test_products[product_index].id,
            quantity=i + 1,
            unit_price=test_products[product_index].price,
            subtotal=(i + 1) * test_products[product_index].price,
        )
        order_items.append(order_item)
    
    for order_item in order_items:
        db_session.add(order_item)
    
    await db_session.commit()
    
    return orders


# Create test order with multiple items
@pytest_asyncio.fixture(scope="function")
async def test_order_multiple_items(db_session: AsyncSession, test_products: List[Product]) -> Order:
    """
    Create a test order with multiple items.
    
    This fixture creates an order with multiple items from different products.
    
    Args:
        db_session: SQLAlchemy async session
        test_products: List of test products
        
    Returns:
        Order: Test order with multiple items
    """
    # Calculate total amount based on items
    total_amount = sum(
        test_products[i].price * qty
        for i, qty in enumerate([2, 1, 3])
        if i < len(test_products)
    )
    
    # Create order
    order = Order(
        status=OrderStatus.PENDING,
        total_amount=total_amount,
        customer_name="Multi-Item Customer",
        customer_email="multi@example.com",
        customer_phone="987-654-3210",
        shipping_address="456 Multi St, Multi City, Multi Country",
        billing_address="456 Multi St, Multi City, Multi Country",
        payment_method="PayPal",
        payment_id="MULTI-PAYMENT-001",
        notes="This is a multi-item test order",
    )
    
    db_session.add(order)
    await db_session.commit()
    await db_session.refresh(order)
    
    # Add order items (multiple items)
    quantities = [2, 1, 3]
    order_items = []
    
    for i, product in enumerate(test_products):
        if i >= len(quantities):
            break
            
        order_item = OrderItem(
            order_id=order.id,
            product_id=product.id,
            quantity=quantities[i],
            unit_price=product.price,
            subtotal=quantities[i] * product.price,
        )
        order_items.append(order_item)
    
    for order_item in order_items:
        db_session.add(order_item)
    
    await db_session.commit()
    
    return order


# ===== Utility Fixtures =====

# Fixture to create a product and return its ID
@pytest_asyncio.fixture(scope="function")
async def create_product(db_session: AsyncSession):
    """
    Create a product and return its ID.
    
    This fixture provides a function to create a product with the given data
    and return its ID.
    
    Args:
        db_session: SQLAlchemy async session
        
    Returns:
        Function: A function that creates a product and returns its ID
    """
    async def _create_product(product_data: Dict) -> int:
        """
        Create a product with the given data and return its ID.
        
        Args:
            product_data: Product data
            
        Returns:
            int: ID of the created product
        """
        product = Product(**product_data)
        db_session.add(product)
        await db_session.commit()
        await db_session.refresh(product)
        return product.id
    
    return _create_product


# Fixture to create an order and return its ID
@pytest_asyncio.fixture(scope="function")
async def create_order(db_session: AsyncSession):
    """
    Create an order and return its ID.
    
    This fixture provides a function to create an order with the given data
    and return its ID.
    
    Args:
        db_session: SQLAlchemy async session
        
    Returns:
        Function: A function that creates an order and returns its ID
    """
    async def _create_order(order_data: Dict, items_data: List[Dict] = None) -> int:
        """
        Create an order with the given data and return its ID.
        
        Args:
            order_data: Order data
            items_data: Order items data
            
        Returns:
            int: ID of the created order
        """
        # Create order
        order = Order(**order_data)
        db_session.add(order)
        await db_session.commit()
        await db_session.refresh(order)
        
        # Create order items if provided
        if items_data:
            for item_data in items_data:
                item_data["order_id"] = order.id
                order_item = OrderItem(**item_data)
                db_session.add(order_item)
            
            await db_session.commit()
        
        return order.id
    
    return _create_order


# Fixture to generate validation error test cases for products
@pytest.fixture(scope="function")
def product_validation_error_cases() -> List[Dict]:
    """
    Generate validation error test cases for products.
    
    This fixture provides a list of product data dictionaries that should
    cause validation errors.
    
    Returns:
        List[Dict]: List of product data dictionaries that should cause validation errors
    """
    return [
        # Missing required fields
        {
            "description": "Missing name field",
            "data": {
                "price": 19.99,
                "inventory_count": 100,
                "sku": "ERR-SKU-001",
            },
            "expected_error": "name"
        },
        {
            "description": "Missing price field",
            "data": {
                "name": "Error Product",
                "inventory_count": 100,
                "sku": "ERR-SKU-002",
            },
            "expected_error": "price"
        },
        {
            "description": "Missing inventory_count field",
            "data": {
                "name": "Error Product",
                "price": 19.99,
                "sku": "ERR-SKU-003",
            },
            "expected_error": "inventory_count"
        },
        {
            "description": "Missing sku field",
            "data": {
                "name": "Error Product",
                "price": 19.99,
                "inventory_count": 100,
            },
            "expected_error": "sku"
        },
        
        # Invalid field values
        {
            "description": "Negative price",
            "data": {
                "name": "Error Product",
                "price": -19.99,
                "inventory_count": 100,
                "sku": "ERR-SKU-004",
            },
            "expected_error": "price"
        },
        {
            "description": "Negative inventory count",
            "data": {
                "name": "Error Product",
                "price": 19.99,
                "inventory_count": -100,
                "sku": "ERR-SKU-005",
            },
            "expected_error": "inventory_count"
        },
        {
            "description": "Empty name",
            "data": {
                "name": "",
                "price": 19.99,
                "inventory_count": 100,
                "sku": "ERR-SKU-006",
            },
            "expected_error": "name"
        },
        {
            "description": "Empty SKU",
            "data": {
                "name": "Error Product",
                "price": 19.99,
                "inventory_count": 100,
                "sku": "",
            },
            "expected_error": "sku"
        },
    ]


# Fixture to generate validation error test cases for orders
@pytest.fixture(scope="function")
def order_validation_error_cases() -> List[Dict]:
    """
    Generate validation error test cases for orders.
    
    This fixture provides a list of order data dictionaries that should
    cause validation errors.
    
    Returns:
        List[Dict]: List of order data dictionaries that should cause validation errors
    """
    return [
        # Missing required fields
        {
            "description": "Missing customer_name field",
            "data": {
                "customer_email": "error@example.com",
                "items": [
                    {
                        "product_id": 1,
                        "quantity": 1,
                    }
                ],
            },
            "expected_error": "customer_name"
        },
        {
            "description": "Missing customer_email field",
            "data": {
                "customer_name": "Error Customer",
                "items": [
                    {
                        "product_id": 1,
                        "quantity": 1,
                    }
                ],
            },
            "expected_error": "customer_email"
        },
        {
            "description": "Missing items field",
            "data": {
                "customer_name": "Error Customer",
                "customer_email": "error@example.com",
            },
            "expected_error": "items"
        },
        {
            "description": "Empty items list",
            "data": {
                "customer_name": "Error Customer",
                "customer_email": "error@example.com",
                "items": [],
            },
            "expected_error": "items"
        },
        
        # Invalid field values
        {
            "description": "Invalid email format",
            "data": {
                "customer_name": "Error Customer",
                "customer_email": "invalid-email",
                "items": [
                    {
                        "product_id": 1,
                        "quantity": 1,
                    }
                ],
            },
            "expected_error": "customer_email"
        },
        {
            "description": "Empty customer name",
            "data": {
                "customer_name": "",
                "customer_email": "error@example.com",
                "items": [
                    {
                        "product_id": 1,
                        "quantity": 1,
                    }
                ],
            },
            "expected_error": "customer_name"
        },
        {
            "description": "Invalid item quantity",
            "data": {
                "customer_name": "Error Customer",
                "customer_email": "error@example.com",
                "items": [
                    {
                        "product_id": 1,
                        "quantity": 0,  # Invalid: quantity must be > 0
                    }
                ],
            },
            "expected_error": "quantity"
        },
        {
            "description": "Non-existent product ID",
            "data": {
                "customer_name": "Error Customer",
                "customer_email": "error@example.com",
                "items": [
                    {
                        "product_id": 9999,  # Non-existent product ID
                        "quantity": 1,
                    }
                ],
            },
            "expected_error": "product_id"
        },
    ]


# Fixture to create a function that verifies product data matches a product model
@pytest.fixture(scope="function")
def verify_product_data():
    """
    Create a function that verifies product data matches a product model.
    
    Returns:
        Function: A function that verifies product data matches a product model
    """
    def _verify_product_data(product: Product, data: Dict) -> bool:
        """
        Verify that product data matches a product model.
        
        Args:
            product: Product model
            data: Product data
            
        Returns:
            bool: True if the data matches the model, False otherwise
        """
        # Check required fields
        if product.name != data.get("name"):
            return False
        if float(product.price) != float(data.get("price", 0)):
            return False
        if product.inventory_count != data.get("inventory_count", 0):
            return False
        if product.sku != data.get("sku"):
            return False
        
        # Check optional fields if provided
        if "description" in data and product.description != data["description"]:
            return False
        if "category" in data and product.category != data["category"]:
            return False
        if "image_url" in data and product.image_url != data["image_url"]:
            return False
        if "weight" in data and product.weight != data["weight"]:
            return False
        if "dimensions" in data and product.dimensions != data["dimensions"]:
            return False
        if "is_active" in data and product.is_active != data["is_active"]:
            return False
        
        return True
    
    return _verify_product_data


# Fixture to create a function that verifies order data matches an order model
@pytest.fixture(scope="function")
def verify_order_data():
    """
    Create a function that verifies order data matches an order model.
    
    Returns:
        Function: A function that verifies order data matches an order model
    """
    def _verify_order_data(order: Order, data: Dict) -> bool:
        """
        Verify that order data matches an order model.
        
        Args:
            order: Order model
            data: Order data
            
        Returns:
            bool: True if the data matches the model, False otherwise
        """
        # Check required fields
        if order.customer_name != data.get("customer_name"):
            return False
        if order.customer_email != data.get("customer_email"):
            return False
        
        # Check optional fields if provided
        if "customer_phone" in data and order.customer_phone != data["customer_phone"]:
            return False
        if "shipping_address" in data and order.shipping_address != data["shipping_address"]:
            return False
        if "billing_address" in data and order.billing_address != data["billing_address"]:
            return False
        if "payment_method" in data and order.payment_method != data["payment_method"]:
            return False
        if "payment_id" in data and order.payment_id != data["payment_id"]:
            return False
        if "notes" in data and order.notes != data["notes"]:
            return False
        
        return True
    
    return _verify_order_data
