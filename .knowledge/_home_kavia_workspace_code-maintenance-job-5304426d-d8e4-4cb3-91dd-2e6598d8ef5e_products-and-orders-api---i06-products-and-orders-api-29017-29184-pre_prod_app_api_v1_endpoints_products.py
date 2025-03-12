{
  "is_source_file": true,
  "format": "Python",
  "description": "API endpoints for product management, providing CRUD operations for products.",
  "external_files": [
    "app/crud/product",
    "app/database",
    "app/schemas/product",
    "app/config"
  ],
  "external_methods": [
    "app.crud.product.get_active",
    "app.crud.product.get_multi",
    "app.crud.product.get",
    "app.crud.product.get_by_sku",
    "app.crud.product.create",
    "app.crud.product.update",
    "app.crud.product.remove",
    "app.crud.product.search_products",
    "app.crud.product.get_by_category"
  ],
  "published": [
    "list_products",
    "get_product",
    "create_product",
    "update_product",
    "delete_product",
    "search_products",
    "get_products_by_category"
  ],
  "classes": [],
  "methods": [
    {
      "name": "list_products",
      "description": "Lists all products with pagination, filtering, and sorting."
    },
    {
      "name": "get_product",
      "description": "Retrieves a specific product by its ID."
    },
    {
      "name": "create_product",
      "description": "Creates a new product."
    },
    {
      "name": "update_product",
      "description": "Updates an existing product identified by its ID."
    },
    {
      "name": "delete_product",
      "description": "Deletes a product identified by its ID."
    },
    {
      "name": "search_products",
      "description": "Searches for products by name or description."
    },
    {
      "name": "get_products_by_category",
      "description": "Retrieves products filtered by a specified category."
    }
  ],
  "calls": [
    "app.database.get_db"
  ],
  "search-terms": [
    "product management",
    "CRUD operations",
    "API endpoints"
  ],
  "state": 2,
  "file_id": 55,
  "knowledge_revision": 227,
  "git_revision": "53c1aa46b9f28ebc082b86b7e3129d155e1a251c",
  "ctags": [],
  "filename": "/home/kavia/workspace/code-maintenance-job-5304426d-d8e4-4cb3-91dd-2e6598d8ef5e/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/app/api/v1/endpoints/products.py",
  "hash": "6b3027686ec7b001e4f995399ed43d52",
  "format-version": 4,
  "code-base-name": "b9046lt",
  "revision_history": [
    {
      "227": "53c1aa46b9f28ebc082b86b7e3129d155e1a251c"
    }
  ]
}