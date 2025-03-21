{
  "is_source_file": true,
  "format": "Python",
  "description": "API endpoints for managing orders, including creating, updating, retrieving, and deleting orders.",
  "external_files": [
    "app/crud/order",
    "app/database",
    "app/schemas/order",
    "app/models/order",
    "app/config",
    "app/errors"
  ],
  "external_methods": [
    "order_crud.get_multi",
    "order_crud.get_by_status",
    "order_crud.create_with_items",
    "order_crud.get_with_items",
    "order_crud.update",
    "order_crud.remove",
    "order_crud.update_status",
    "order_crud.get_by_customer_email"
  ],
  "published": [
    "list_orders",
    "get_order",
    "create_order",
    "update_order",
    "delete_order",
    "update_order_status",
    "get_orders_by_customer_email"
  ],
  "classes": [],
  "methods": [
    {
      "name": "list_orders",
      "description": "Lists all orders with pagination, filtering, and sorting."
    },
    {
      "name": "get_order",
      "description": "Retrieves the details of a specific order by its ID."
    },
    {
      "name": "create_order",
      "description": "Creates a new order and returns the created order details."
    },
    {
      "name": "update_order",
      "description": "Updates an existing order identified by its ID."
    },
    {
      "name": "delete_order",
      "description": "Deletes an order identified by its ID."
    },
    {
      "name": "update_order_status",
      "description": "Updates the status of an existing order."
    },
    {
      "name": "get_orders_by_customer_email",
      "description": "Retrieves a list of orders that belong to a customer identified by their email address."
    }
  ],
  "calls": [
    "get_db",
    "logging.getLogger",
    "db.refresh",
    "order_crud.get_by_status",
    "order_crud.get_multi",
    "order_crud.get_with_items",
    "order_crud.create_with_items",
    "order_crud.update",
    "order_crud.remove",
    "order_crud.update_status",
    "order_crud.get_by_customer_email"
  ],
  "search-terms": [
    "order management",
    "order CRUD operations",
    "FastAPI endpoints",
    "order creation",
    "order deletion",
    "order update"
  ],
  "state": 2,
  "file_id": 54,
  "knowledge_revision": 230,
  "git_revision": "eb353a04eb44a748f9d419aff8f3771781040314",
  "ctags": [],
  "filename": "/home/kavia/workspace/code-maintenance-job-5304426d-d8e4-4cb3-91dd-2e6598d8ef5e/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/app/api/v1/endpoints/orders.py",
  "hash": "ae151e44f4d8fe56ee60d6f12ec33c0c",
  "format-version": 4,
  "code-base-name": "b9046lt",
  "revision_history": [
    {
      "230": "eb353a04eb44a748f9d419aff8f3771781040314"
    }
  ]
}