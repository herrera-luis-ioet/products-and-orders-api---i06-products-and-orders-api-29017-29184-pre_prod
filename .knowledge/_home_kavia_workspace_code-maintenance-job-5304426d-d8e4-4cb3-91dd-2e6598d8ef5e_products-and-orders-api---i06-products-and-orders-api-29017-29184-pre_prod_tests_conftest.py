{
  "is_source_file": true,
  "format": "Python",
  "description": "This file contains Pytest configuration and fixtures for testing the products and orders API in a FastAPI application, including database setups and test data generation for products and orders.",
  "external_files": [
    "app.api.v1.api",
    "app.config.Settings",
    "app.database",
    "app.models.order",
    "app.models.product"
  ],
  "external_methods": [
    "app.database.get_db",
    "app.database.init_db",
    "app.models.order.Order",
    "app.models.order.OrderItem",
    "app.models.product.Product"
  ],
  "published": [
    "test_settings",
    "override_settings",
    "engine",
    "reset_db",
    "db_session",
    "override_get_db",
    "app",
    "client",
    "product_data",
    "product_data_required_only",
    "product_data_invalid",
    "product_data_generator",
    "product_data_batch",
    "order_data",
    "order_data_required_only",
    "order_data_invalid",
    "order_data_generator",
    "order_data_multiple_items"
  ],
  "classes": [],
  "methods": [
    {
      "name": "test_settings",
      "description": "Fixture that provides test settings including a file-based SQLite database URL."
    },
    {
      "name": "override_settings",
      "description": "Fixture that overrides global settings with test settings before tests are run."
    },
    {
      "name": "engine",
      "description": "Fixture that creates an asynchronous SQLAlchemy engine for tests using a temporary SQLite database."
    },
    {
      "name": "reset_db",
      "description": "Fixture that resets the database tables before each test to ensure a clean state."
    },
    {
      "name": "db_session",
      "description": "Fixture that provides an asynchronous database session for testing."
    },
    {
      "name": "override_get_db",
      "description": "Fixture that overrides the dependency injection of the get_db function to use the test database session."
    },
    {
      "name": "app",
      "description": "Fixture that creates a test FastAPI application with overridden database dependencies."
    },
    {
      "name": "client",
      "description": "Fixture that creates an asynchronous HTTP client for testing API endpoints."
    },
    {
      "name": "product_data",
      "description": "Fixture that generates test product data with all fields filled."
    },
    {
      "name": "product_data_required_only",
      "description": "Fixture that generates test product data with only the required fields."
    },
    {
      "name": "product_data_invalid",
      "description": "Fixture that generates test product data with invalid field values."
    },
    {
      "name": "product_data_generator",
      "description": "Fixture that provides a generator function to create customizable test product data."
    },
    {
      "name": "product_data_batch",
      "description": "Fixture that generates a batch of test product data."
    },
    {
      "name": "order_data",
      "description": "Fixture that generates test order data with all fields filled."
    },
    {
      "name": "order_data_required_only",
      "description": "Fixture that generates test order data with only the required fields."
    },
    {
      "name": "order_data_invalid",
      "description": "Fixture that generates test order data with invalid field values."
    },
    {
      "name": "order_data_generator",
      "description": "Fixture that provides a generator function to create customizable test order data."
    },
    {
      "name": "order_data_multiple_items",
      "description": "Fixture that generates test order data containing multiple items."
    }
  ],
  "calls": [
    "os.path.exists",
    "os.remove",
    "settings.DATABASE_URL",
    "engine.begin",
    "Base.metadata.create_all",
    "Base.metadata.drop_all",
    "sessionmaker"
  ],
  "search-terms": [
    "Pytest",
    "FastAPI",
    "test fixtures",
    "SQLite database",
    "testing"
  ],
  "state": 2,
  "file_id": 73,
  "knowledge_revision": 247,
  "git_revision": "eb353a04eb44a748f9d419aff8f3771781040314",
  "ctags": [],
  "filename": "/home/kavia/workspace/code-maintenance-job-5304426d-d8e4-4cb3-91dd-2e6598d8ef5e/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/tests/conftest.py",
  "hash": "fea16938e6dcd397ffcbb3cf792550cb",
  "format-version": 4,
  "code-base-name": "b9046lt",
  "revision_history": [
    {
      "247": "eb353a04eb44a748f9d419aff8f3771781040314"
    }
  ]
}