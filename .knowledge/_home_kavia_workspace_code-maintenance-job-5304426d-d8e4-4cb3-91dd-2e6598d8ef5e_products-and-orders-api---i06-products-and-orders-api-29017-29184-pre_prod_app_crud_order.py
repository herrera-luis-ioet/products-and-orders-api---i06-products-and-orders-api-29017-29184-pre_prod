{
  "is_source_file": true,
  "format": "Python",
  "description": "This file contains CRUD (Create, Read, Update, Delete) operations specific to Order and OrderItem models in a database context. It utilizes SQLAlchemy for database interactions and handles product validation and inventory management on order creation.",
  "external_files": [
    "app/crud/base.py",
    "app/models/order.py",
    "app/schemas/order.py",
    "app/crud/product.py",
    "app/errors.py"
  ],
  "external_methods": [
    "product_crud.get",
    "product_crud.update_inventory"
  ],
  "published": [
    "order",
    "order_item"
  ],
  "classes": [
    {
      "name": "CRUDOrderItem",
      "description": "Handles CRUD operations specifically for OrderItem with methods to create order items associated with an order."
    },
    {
      "name": "CRUDOrder",
      "description": "Handles CRUD operations specifically for Order with methods for creating orders, retrieving orders by various filters, and updating order statuses."
    }
  ],
  "methods": [
    {
      "name": "create_with_order",
      "description": "Creates a new order item associated with a specific order, validating product availability and inventory before adding the item."
    },
    {
      "name": "get",
      "description": "Retrieves an order by its ID, raising an OrderValidationError if the order is not found."
    },
    {
      "name": "get_with_items",
      "description": "Retrieves an order by its ID and includes associated order items."
    },
    {
      "name": "get_by_customer_email",
      "description": "Retrieves orders associated with a specific customer email, allowing for pagination."
    },
    {
      "name": "get_by_status",
      "description": "Retrieves orders based on their status with pagination support."
    },
    {
      "name": "create_with_items",
      "description": "Creates a new order along with its items, ensuring that all products are valid and have sufficient inventory."
    },
    {
      "name": "update_status",
      "description": "Updates the status of a specific order, ensuring valid status transitions."
    },
    {
      "name": "remove",
      "description": "Removes an order from the database, checking that the order is in a deletable state."
    }
  ],
  "calls": [
    "db.add",
    "db.commit",
    "db.rollback",
    "db.refresh",
    "db.delete",
    "db.flush",
    "await db.execute",
    "await product_crud.get",
    "await product_crud.update_inventory"
  ],
  "search-terms": [
    "CRUD operations",
    "Order management",
    "OrderItem CRUD functionality",
    "Product validation",
    "SQLAlchemy interactions"
  ],
  "state": 2,
  "file_id": 62,
  "knowledge_revision": 241,
  "git_revision": "7a97cd1e9a5a9d847b2ffcf57e9d5f75fa3a9be6",
  "ctags": [],
  "filename": "/home/kavia/workspace/code-maintenance-job-5304426d-d8e4-4cb3-91dd-2e6598d8ef5e/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/app/crud/order.py",
  "hash": "47b94b5bf02fbfc68438f90635c0103f",
  "format-version": 4,
  "code-base-name": "b9046lt",
  "revision_history": [
    {
      "241": "7a97cd1e9a5a9d847b2ffcf57e9d5f75fa3a9be6"
    }
  ]
}