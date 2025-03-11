{"is_source_file": true, "format": "Python", "description": "This module defines API endpoints for managing orders, including creating, reading, updating, and deleting orders. It utilizes FastAPI for routing and SQLAlchemy for database interactions.", "external_files": ["app/crud/order", "app/database", "app/schemas/order", "app/models/order", "app/config", "app/errors"], "external_methods": ["app.crud.order.order.get_by_status", "app.crud.order.order.get_multi", "app.crud.order.order.create_with_items", "app.crud.order.order.update", "app.crud.order.order.get", "app.crud.order.order.remove", "app.crud.order.order.update_status", "app.crud.order.order.get_by_customer_email"], "published": ["list_orders", "get_order", "create_order", "update_order", "delete_order", "update_order_status", "get_orders_by_customer_email"], "classes": [], "methods": [{"name": "Any list_orders( db: AsyncSession = Depends(get_db), skip: int = Query(0, ge=0, description=\"Number of orders to skip\"), limit: int = Query(settings.PAGINATION_PAGE_SIZE, ge=1, le=100, description=\"Number of orders to return\"), sort_by: Optional[str] = Query(None, description=\"Field to sort by\"), sort_desc: bool = Query(False, description=\"Sort in descending order\"), status: Optional[OrderStatus] = Query(None, description=\"Filter by order status\") )", "description": "Lists all orders with options for pagination, filtering by status, and sorting.", "scope": "", "scopeKind": ""}, {"name": "Any get_order( order_id: int = Path(..., gt=0, description=\"The ID of the order to get\"), db: AsyncSession = Depends(get_db) )", "description": "Retrieves a specific order by its ID.", "scope": "", "scopeKind": ""}, {"name": "Any create_order( order_in: OrderCreate, db: AsyncSession = Depends(get_db) )", "description": "Creates a new order with the provided order data.", "scope": "", "scopeKind": ""}, {"name": "Any update_order( order_in: OrderUpdate, order_id: int = Path(..., gt=0, description=\"The ID of the order to update\"), db: AsyncSession = Depends(get_db) )", "description": "Updates an existing order with new data based on the order ID.", "scope": "", "scopeKind": ""}, {"name": "Any delete_order( order_id: int = Path(..., gt=0, description=\"The ID of the order to delete\"), db: AsyncSession = Depends(get_db) )", "description": "Deletes an order based on its ID.", "scope": "", "scopeKind": ""}, {"name": "Any update_order_status( status: OrderStatus = Body(..., description=\"New order status\"), order_id: int = Path(..., gt=0, description=\"The ID of the order to update\"), db: AsyncSession = Depends(get_db) )", "description": "Updates the status of an order based on its ID.", "scope": "", "scopeKind": ""}, {"name": "Any get_orders_by_customer_email( customer_email: str = Path(..., description=\"Customer email address\"), db: AsyncSession = Depends(get_db), skip: int = Query(0, ge=0, description=\"Number of orders to skip\"), limit: int = Query(settings.PAGINATION_PAGE_SIZE, ge=1, le=100, description=\"Number of orders to return\") )", "description": "Retrieves orders associated with a specific customer email address.", "scope": "", "scopeKind": ""}], "calls": ["app.database.get_db", "app.crud.order.order.get_by_status", "app.crud.order.order.get_multi", "app.crud.order.order.create_with_items", "app.crud.order.order.get", "app.crud.order.order.update", "app.crud.order.order.remove", "app.crud.order.order.update_status", "app.crud.order.order.get_by_customer_email"], "search-terms": ["order management", "FastAPI endpoints", "order CRUD operations"], "state": 2, "file_id": 24, "knowledge_revision": 94, "git_revision": "53c1aa46b9f28ebc082b86b7e3129d155e1a251c", "revision_history": [{"51": ""}, {"87": "53c1aa46b9f28ebc082b86b7e3129d155e1a251c"}, {"88": "53c1aa46b9f28ebc082b86b7e3129d155e1a251c"}, {"89": "53c1aa46b9f28ebc082b86b7e3129d155e1a251c"}, {"91": "53c1aa46b9f28ebc082b86b7e3129d155e1a251c"}, {"94": "53c1aa46b9f28ebc082b86b7e3129d155e1a251c"}], "ctags": [{"_type": "tag", "name": "create_order", "path": "/home/kavia/workspace/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/app/api/v1/endpoints/orders.py", "pattern": "/^async def create_order($/", "language": "Python", "typeref": "typename:Any", "kind": "function", "signature": "( order_in: OrderCreate, db: AsyncSession = Depends(get_db) )"}, {"_type": "tag", "name": "delete_order", "path": "/home/kavia/workspace/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/app/api/v1/endpoints/orders.py", "pattern": "/^async def delete_order($/", "language": "Python", "typeref": "typename:Any", "kind": "function", "signature": "( order_id: int = Path(..., gt=0, description=\"The ID of the order to delete\"), db: AsyncSession = Depends(get_db) )"}, {"_type": "tag", "name": "get_order", "path": "/home/kavia/workspace/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/app/api/v1/endpoints/orders.py", "pattern": "/^async def get_order($/", "language": "Python", "typeref": "typename:Any", "kind": "function", "signature": "( order_id: int = Path(..., gt=0, description=\"The ID of the order to get\"), db: AsyncSession = Depends(get_db) )"}, {"_type": "tag", "name": "get_orders_by_customer_email", "path": "/home/kavia/workspace/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/app/api/v1/endpoints/orders.py", "pattern": "/^async def get_orders_by_customer_email($/", "language": "Python", "typeref": "typename:Any", "kind": "function", "signature": "( customer_email: str = Path(..., description=\"Customer email address\"), db: AsyncSession = Depends(get_db), skip: int = Query(0, ge=0, description=\"Number of orders to skip\"), limit: int = Query(settings.PAGINATION_PAGE_SIZE, ge=1, le=100, description=\"Number of orders to return\") )"}, {"_type": "tag", "name": "list_orders", "path": "/home/kavia/workspace/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/app/api/v1/endpoints/orders.py", "pattern": "/^async def list_orders($/", "language": "Python", "typeref": "typename:Any", "kind": "function", "signature": "( db: AsyncSession = Depends(get_db), skip: int = Query(0, ge=0, description=\"Number of orders to skip\"), limit: int = Query(settings.PAGINATION_PAGE_SIZE, ge=1, le=100, description=\"Number of orders to return\"), sort_by: Optional[str] = Query(None, description=\"Field to sort by\"), sort_desc: bool = Query(False, description=\"Sort in descending order\"), status: Optional[OrderStatus] = Query(None, description=\"Filter by order status\") )"}, {"_type": "tag", "name": "order_crud", "path": "/home/kavia/workspace/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/app/api/v1/endpoints/orders.py", "pattern": "/^from app.crud.order import order as order_crud$/", "language": "Python", "kind": "unknown", "nameref": "unknown:order"}, {"_type": "tag", "name": "router", "path": "/home/kavia/workspace/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/app/api/v1/endpoints/orders.py", "pattern": "/^router = APIRouter()$/", "language": "Python", "kind": "variable"}, {"_type": "tag", "name": "update_order", "path": "/home/kavia/workspace/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/app/api/v1/endpoints/orders.py", "pattern": "/^async def update_order($/", "language": "Python", "typeref": "typename:Any", "kind": "function", "signature": "( order_in: OrderUpdate, order_id: int = Path(..., gt=0, description=\"The ID of the order to update\"), db: AsyncSession = Depends(get_db) )"}, {"_type": "tag", "name": "update_order_status", "path": "/home/kavia/workspace/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/app/api/v1/endpoints/orders.py", "pattern": "/^async def update_order_status($/", "language": "Python", "typeref": "typename:Any", "kind": "function", "signature": "( status: OrderStatus = Body(..., description=\"New order status\"), order_id: int = Path(..., gt=0, description=\"The ID of the order to update\"), db: AsyncSession = Depends(get_db) )"}], "filename": "/home/kavia/workspace/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/app/api/v1/endpoints/orders.py", "hash": "e0a810bc773b413f29774266d53daf5d", "format-version": 4, "code-base-name": "default", "fields": [{"name": "router = APIRouter()", "scope": "", "scopeKind": "", "description": "unavailable"}]}