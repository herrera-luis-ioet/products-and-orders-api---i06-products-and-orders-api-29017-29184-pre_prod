{
  "is_source_file": true,
  "format": "Python",
  "description": "This file contains tests for the product API endpoints, including tests for creating, reading, updating, and deleting products.",
  "external_files": [
    "app/models/product"
  ],
  "external_methods": [],
  "published": [],
  "classes": [],
  "methods": [
    {
      "name": "test_list_products",
      "description": "Test listing products."
    },
    {
      "name": "test_list_products_pagination",
      "description": "Test listing products with pagination."
    },
    {
      "name": "test_get_product",
      "description": "Test getting a specific product."
    },
    {
      "name": "test_get_product_not_found",
      "description": "Test getting a non-existent product."
    },
    {
      "name": "test_create_product",
      "description": "Test creating a product."
    },
    {
      "name": "test_create_product_duplicate_sku",
      "description": "Test creating a product with a duplicate SKU."
    },
    {
      "name": "test_update_product",
      "description": "Test updating a product."
    },
    {
      "name": "test_update_product_not_found",
      "description": "Test updating a non-existent product."
    },
    {
      "name": "test_update_product_duplicate_sku",
      "description": "Test updating a product with a duplicate SKU."
    },
    {
      "name": "test_delete_product",
      "description": "Test deleting a product."
    },
    {
      "name": "test_delete_product_not_found",
      "description": "Test deleting a non-existent product."
    },
    {
      "name": "test_search_products",
      "description": "Test searching products."
    },
    {
      "name": "test_get_products_by_category",
      "description": "Test getting products by category."
    }
  ],
  "calls": [
    "client.get",
    "client.post",
    "client.put",
    "client.delete"
  ],
  "search-terms": [
    "product",
    "API",
    "tests",
    "endpoints"
  ],
  "state": 2,
  "file_id": 70,
  "knowledge_revision": 245,
  "git_revision": "ff18e2b0ed147be6b70a9c294b26f436f021ecbe",
  "ctags": [],
  "filename": "/home/kavia/workspace/code-maintenance-job-5304426d-d8e4-4cb3-91dd-2e6598d8ef5e/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/tests/test_api/test_products.py",
  "hash": "9eac0ec4efab7d8fbef4819d0f7b009a",
  "format-version": 4,
  "code-base-name": "b9046lt",
  "revision_history": [
    {
      "245": "ff18e2b0ed147be6b70a9c294b26f436f021ecbe"
    }
  ]
}