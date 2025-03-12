{
  "is_source_file": true,
  "format": "Python",
  "description": "This module contains dependency injection functions for FastAPI routes, providing common dependencies like pagination, sorting, and request tracing for API endpoints.",
  "external_files": [
    "app.config",
    "app.database",
    "app.crud.product",
    "app.crud.order"
  ],
  "external_methods": [
    "app.database.get_db",
    "app.crud.product.product.get",
    "app.crud.order.order.get"
  ],
  "published": [
    "get_pagination_params",
    "get_sort_params",
    "get_correlation_id",
    "validate_product_exists",
    "validate_order_exists"
  ],
  "classes": [],
  "methods": [
    {
      "name": "get_pagination_params",
      "description": "Fetches pagination parameters (skip and limit) from query parameters."
    },
    {
      "name": "get_sort_params",
      "description": "Fetches sorting parameters (sort_by and sort_desc) from query parameters."
    },
    {
      "name": "get_correlation_id",
      "description": "Generates or retrieves a correlation ID for request tracing from the headers."
    },
    {
      "name": "validate_product_exists",
      "description": "Checks if a product exists in the database using its ID, raises HTTPException if not found."
    },
    {
      "name": "validate_order_exists",
      "description": "Checks if an order exists in the database using its ID, raises HTTPException if not found."
    }
  ],
  "calls": [
    "app.database.get_db",
    "app.crud.product.product.get",
    "app.crud.order.order.get"
  ],
  "search-terms": [
    "FastAPI dependencies",
    "pagination parameters",
    "sorting parameters",
    "correlation ID",
    "product validation",
    "order validation"
  ],
  "state": 2,
  "file_id": 64,
  "knowledge_revision": 237,
  "git_revision": "d388d9a7e7019e9bd32c3ada33343fc29b1bfd8a",
  "ctags": [],
  "filename": "/home/kavia/workspace/code-maintenance-job-5304426d-d8e4-4cb3-91dd-2e6598d8ef5e/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/app/dependencies.py",
  "hash": "00bb2f22fafc63ae77bcd0c3d9ced6a9",
  "format-version": 4,
  "code-base-name": "b9046lt",
  "revision_history": [
    {
      "237": "d388d9a7e7019e9bd32c3ada33343fc29b1bfd8a"
    }
  ]
}