{
  "is_source_file": true,
  "format": "Python",
  "description": "CRUD operations for the Product model, including methods for retrieving, updating, and removing products from a database.",
  "external_files": [
    "app/crud/base.py",
    "app/models/product.py",
    "app/schemas/product.py"
  ],
  "external_methods": [
    "CRUDBase.get",
    "CRUDBase.delete"
  ],
  "published": [
    "CRUDProduct"
  ],
  "classes": [
    {
      "name": "CRUDProduct",
      "description": "Extends CRUDBase with product-specific CRUD operations."
    }
  ],
  "methods": [
    {
      "name": "get_by_sku",
      "description": "Fetches a product by its SKU."
    },
    {
      "name": "get_by_category",
      "description": "Retrieves a list of products filtered by category with pagination."
    },
    {
      "name": "get_active",
      "description": "Fetches active products with pagination."
    },
    {
      "name": "update_inventory",
      "description": "Updates the inventory count of a product."
    },
    {
      "name": "search_products",
      "description": "Searches products by name or description based on a query string."
    },
    {
      "name": "remove",
      "description": "Removes a product by its ID."
    }
  ],
  "calls": [
    "asyncio.get",
    "asyncio.delete",
    "sqlalchemy.select"
  ],
  "search-terms": [
    "CRUD",
    "Product",
    "SKU",
    "Category",
    "Inventory",
    "Search"
  ],
  "state": 2,
  "file_id": 60,
  "knowledge_revision": 233,
  "git_revision": "78da84a7ddc34a059904ebc8292ed997620817b5",
  "ctags": [],
  "filename": "/home/kavia/workspace/code-maintenance-job-5304426d-d8e4-4cb3-91dd-2e6598d8ef5e/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/app/crud/product.py",
  "hash": "0852761bd18b4ecf5ced42ae49c1486f",
  "format-version": 4,
  "code-base-name": "b9046lt",
  "revision_history": [
    {
      "233": "78da84a7ddc34a059904ebc8292ed997620817b5"
    }
  ]
}