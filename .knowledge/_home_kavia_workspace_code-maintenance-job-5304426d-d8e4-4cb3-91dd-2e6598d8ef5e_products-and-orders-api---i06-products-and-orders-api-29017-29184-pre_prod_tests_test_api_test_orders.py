{
  "is_source_file": true,
  "format": "Python",
  "description": "This file contains unit tests for the order API endpoints, verifying functionality related to creating, reading, updating, and deleting orders and testing various scenarios including error handling.",
  "external_files": [
    "app.models.order",
    "app.models.product",
    "app.api.v1.endpoints.orders",
    "app.errors"
  ],
  "external_methods": [
    "OrderValidationError",
    "ProductValidationError",
    "_safely_refresh_product_relationships"
  ],
  "published": [],
  "classes": [],
  "methods": [
    {
      "name": "test_list_orders",
      "description": "Tests the endpoint for listing orders, ensuring it returns the correct status code and data."
    },
    {
      "name": "test_create_order",
      "description": "Tests the endpoint for creating an order, checking that it properly processes valid order data."
    },
    {
      "name": "test_update_order",
      "description": "Tests the updating of an order, ensuring the order is updated correctly and responds with the right data."
    },
    {
      "name": "test_delete_order",
      "description": "Tests the deletion of an order, verifying that upon successful deletion the order can no longer be retrieved."
    },
    {
      "name": "test_list_orders_by_status",
      "description": "Tests the endpoint for listing orders by their status."
    },
    {
      "name": "test_get_order",
      "description": "Tests fetching a specific order by its ID."
    },
    {
      "name": "test_get_orders_by_customer_email",
      "description": "Tests retrieving orders associated with a specific customer email."
    },
    {
      "name": "test_safely_refresh_product_relationships_none_order",
      "description": "Tests the method _safely_refresh_product_relationships when the order parameter is None."
    }
  ],
  "calls": [
    "client.get",
    "client.post",
    "client.put",
    "client.delete",
    "_safely_refresh_product_relationships"
  ],
  "search-terms": [
    "order API tests",
    "test creation of orders",
    "test updating orders",
    "test deleting orders",
    "test listing orders"
  ],
  "state": 2,
  "file_id": 71,
  "knowledge_revision": 246,
  "git_revision": "2ac50873130053b1f3092f91d4e6d192009d9be3",
  "ctags": [],
  "filename": "/home/kavia/workspace/code-maintenance-job-5304426d-d8e4-4cb3-91dd-2e6598d8ef5e/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/tests/test_api/test_orders.py",
  "hash": "e852ebfaab8515746fd3e5f09e17684a",
  "format-version": 4,
  "code-base-name": "b9046lt",
  "revision_history": [
    {
      "246": "2ac50873130053b1f3092f91d4e6d192009d9be3"
    }
  ]
}