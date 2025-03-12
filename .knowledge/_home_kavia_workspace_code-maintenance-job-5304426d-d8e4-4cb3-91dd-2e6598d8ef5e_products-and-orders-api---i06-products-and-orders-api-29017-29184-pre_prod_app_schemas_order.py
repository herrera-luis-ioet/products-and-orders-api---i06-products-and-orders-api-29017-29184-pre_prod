{
  "is_source_file": true,
  "format": "Python",
  "description": "This module provides Pydantic schemas for order validation and serialization, including classes for creating, updating, and responding with order and order item data.",
  "external_files": [
    "app.models.order",
    "app.schemas.product"
  ],
  "external_methods": [],
  "published": [
    "OrderItemCreate",
    "OrderItemUpdate",
    "OrderCreate",
    "OrderUpdate",
    "OrderInDB",
    "OrderResponse",
    "OrderSummary",
    "OrderStatusResponse"
  ],
  "classes": [
    {
      "name": "OrderItemBase",
      "description": "Base schema for order item data, defining common fields for order item-related schemas."
    },
    {
      "name": "OrderItemCreate",
      "description": "Schema for creating a new order item, validating order item creation requests."
    },
    {
      "name": "OrderItemUpdate",
      "description": "Schema for updating an existing order item, allowing partial updates."
    },
    {
      "name": "OrderItemInDB",
      "description": "Schema for order item data as stored in the database, including database-specific fields."
    },
    {
      "name": "OrderItemResponse",
      "description": "Schema for order item response used for serializing data in API responses."
    },
    {
      "name": "OrderBase",
      "description": "Base schema for order data, defining common fields for order-related schemas."
    },
    {
      "name": "OrderCreate",
      "description": "Schema for creating a new order, validating requests for order creation."
    },
    {
      "name": "OrderUpdate",
      "description": "Schema for updating an existing order with optional fields for partial updates."
    },
    {
      "name": "OrderInDB",
      "description": "Schema for order data stored in the database, including id and timestamps."
    },
    {
      "name": "OrderResponse",
      "description": "Schema for order response in API, including serialized order items."
    },
    {
      "name": "OrderSummary",
      "description": "Schema for summarizing order data for listing purposes without full details."
    },
    {
      "name": "OrderStatusResponse",
      "description": "Schema for order status update response, similar to OrderResponse but without required items."
    }
  ],
  "methods": [],
  "calls": [],
  "search-terms": [
    "Pydantic schemas",
    "order validation",
    "order serialization",
    "order management"
  ],
  "state": 2,
  "file_id": 45,
  "knowledge_revision": 222,
  "git_revision": "ca96b22d169e77f3639f4853a4923848cd8dcd9d",
  "ctags": [],
  "filename": "/home/kavia/workspace/code-maintenance-job-5304426d-d8e4-4cb3-91dd-2e6598d8ef5e/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/app/schemas/order.py",
  "hash": "dbf275bfc2d7d24e2522954ec941b9d0",
  "format-version": 4,
  "code-base-name": "b9046lt",
  "revision_history": [
    {
      "222": "ca96b22d169e77f3639f4853a4923848cd8dcd9d"
    }
  ]
}