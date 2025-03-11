{"is_source_file": true, "format": "Python", "description": "This file contains CRUD operations for Order and OrderItem models within an API, handling database interactions and business logic for creating, retrieving, updating, and deleting orders and order items.", "external_files": ["app/crud/base", "app/models.order", "app/schemas.order", "app/crud.product", "app.errors"], "external_methods": ["product_crud.get", "product_crud.update_inventory"], "published": ["CRUDOrderItem", "CRUDOrder"], "classes": [{"name": "CRUDOrderItem", "description": "Class handling CRUD operations for OrderItem model, including creation, validation, and inventory management."}, {"name": "CRUDOrder", "description": "Class handling CRUD operations for Order model, including order creation, retrieval by various filters, and status updates."}], "methods": [{"name": "OrderItem create_with_order( self, db: AsyncSession, *, obj_in: OrderItemCreate, order_id: int )", "description": "Creates a new OrderItem associated with a specific order, including inventory checks and price calculations.", "scope": "CRUDOrderItem", "scopeKind": "class"}, {"name": "Optional[Order] get(self, db: AsyncSession, id: int)", "description": "Fetches an Order by its ID, raising validation errors if the order is not found.", "scope": "CRUDOrder", "scopeKind": "class"}, {"name": "Optional[Order] get_with_items(self, db: AsyncSession, id: int)", "description": "Fetches an Order by its ID along with associated items.", "scope": "CRUDOrder", "scopeKind": "class"}, {"name": "List[Order] get_by_customer_email( self, db: AsyncSession, *, email: str, skip: int = 0, limit: int = 100 )", "description": "Fetches orders associated with a specific customer email with pagination support.", "scope": "CRUDOrder", "scopeKind": "class"}, {"name": "List[Order] get_by_status( self, db: AsyncSession, *, status: OrderStatus, skip: int = 0, limit: int = 100 )", "description": "Retrieves a list of orders that match a given status with pagination support.", "scope": "CRUDOrder", "scopeKind": "class"}, {"name": "Order create_with_items( self, db: AsyncSession, *, obj_in: OrderCreate )", "description": "Creates a new order along with its associated items, validating product conditions and handling errors.", "scope": "CRUDOrder", "scopeKind": "class"}, {"name": "Optional[Order] update_status( self, db: AsyncSession, *, id: int, status: OrderStatus )", "description": "Updates the status of an existing order, ensuring valid status transitions.", "scope": "CRUDOrder", "scopeKind": "class"}, {"name": "Order remove(self, db: AsyncSession, *, id: int)", "description": "Removes an order from the database, checking for valid deletion conditions based on the order's status.", "scope": "CRUDOrder", "scopeKind": "class"}], "calls": ["product_crud.get", "product_crud.update_inventory"], "search-terms": ["CRUD operations", "Order management", "OrderItem management", "Inventory validation"], "state": 2, "file_id": 17, "knowledge_revision": 98, "git_revision": "d6bec950efdce2c5b2d3c8ddab6531b59d63a5c9", "revision_history": [{"37": ""}, {"83": "370184de095522425ca19c1e5d95b8bdc488032e"}, {"84": "370184de095522425ca19c1e5d95b8bdc488032e"}, {"85": "370184de095522425ca19c1e5d95b8bdc488032e"}, {"86": "370184de095522425ca19c1e5d95b8bdc488032e"}, {"90": "370184de095522425ca19c1e5d95b8bdc488032e"}, {"92": "370184de095522425ca19c1e5d95b8bdc488032e"}, {"93": "370184de095522425ca19c1e5d95b8bdc488032e"}, {"95": "370184de095522425ca19c1e5d95b8bdc488032e"}, {"98": "d6bec950efdce2c5b2d3c8ddab6531b59d63a5c9"}], "ctags": [{"_type": "tag", "name": "CRUDOrder", "path": "/home/kavia/workspace/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/app/crud/order.py", "pattern": "/^class CRUDOrder(CRUDBase[Order, OrderCreate, OrderUpdate]):$/", "language": "Python", "kind": "class"}, {"_type": "tag", "name": "CRUDOrderItem", "path": "/home/kavia/workspace/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/app/crud/order.py", "pattern": "/^class CRUDOrderItem(CRUDBase[OrderItem, OrderItemCreate, Dict[str, Any]]):$/", "language": "Python", "kind": "class"}, {"_type": "tag", "name": "create_with_items", "path": "/home/kavia/workspace/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/app/crud/order.py", "pattern": "/^    async def create_with_items($/", "language": "Python", "typeref": "typename:Order", "kind": "member", "signature": "( self, db: AsyncSession, *, obj_in: OrderCreate )", "scope": "CRUDOrder", "scopeKind": "class"}, {"_type": "tag", "name": "create_with_order", "path": "/home/kavia/workspace/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/app/crud/order.py", "pattern": "/^    async def create_with_order($/", "language": "Python", "typeref": "typename:OrderItem", "kind": "member", "signature": "( self, db: AsyncSession, *, obj_in: OrderItemCreate, order_id: int )", "scope": "CRUDOrderItem", "scopeKind": "class"}, {"_type": "tag", "name": "get", "path": "/home/kavia/workspace/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/app/crud/order.py", "pattern": "/^    async def get(self, db: AsyncSession, id: int) -> Optional[Order]:$/", "language": "Python", "typeref": "typename:Optional[Order]", "kind": "member", "signature": "(self, db: AsyncSession, id: int)", "scope": "CRUDOrder", "scopeKind": "class"}, {"_type": "tag", "name": "get_by_customer_email", "path": "/home/kavia/workspace/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/app/crud/order.py", "pattern": "/^    async def get_by_customer_email($/", "language": "Python", "typeref": "typename:List[Order]", "kind": "member", "signature": "( self, db: AsyncSession, *, email: str, skip: int = 0, limit: int = 100 )", "scope": "CRUDOrder", "scopeKind": "class"}, {"_type": "tag", "name": "get_by_status", "path": "/home/kavia/workspace/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/app/crud/order.py", "pattern": "/^    async def get_by_status($/", "language": "Python", "typeref": "typename:List[Order]", "kind": "member", "signature": "( self, db: AsyncSession, *, status: OrderStatus, skip: int = 0, limit: int = 100 )", "scope": "CRUDOrder", "scopeKind": "class"}, {"_type": "tag", "name": "get_with_items", "path": "/home/kavia/workspace/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/app/crud/order.py", "pattern": "/^    async def get_with_items(self, db: AsyncSession, id: int) -> Optional[Order]:$/", "language": "Python", "typeref": "typename:Optional[Order]", "kind": "member", "signature": "(self, db: AsyncSession, id: int)", "scope": "CRUDOrder", "scopeKind": "class"}, {"_type": "tag", "name": "order", "path": "/home/kavia/workspace/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/app/crud/order.py", "pattern": "/^order = CRUDOrder(Order)$/", "language": "Python", "kind": "variable"}, {"_type": "tag", "name": "order_item", "path": "/home/kavia/workspace/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/app/crud/order.py", "pattern": "/^order_item = CRUDOrderItem(OrderItem)$/", "language": "Python", "kind": "variable"}, {"_type": "tag", "name": "product_crud", "path": "/home/kavia/workspace/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/app/crud/order.py", "pattern": "/^from app.crud.product import product as product_crud$/", "language": "Python", "kind": "unknown", "nameref": "unknown:product"}, {"_type": "tag", "name": "remove", "path": "/home/kavia/workspace/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/app/crud/order.py", "pattern": "/^    async def remove(self, db: AsyncSession, *, id: int) -> Order:$/", "language": "Python", "typeref": "typename:Order", "kind": "member", "signature": "(self, db: AsyncSession, *, id: int)", "scope": "CRUDOrder", "scopeKind": "class"}, {"_type": "tag", "name": "update_status", "path": "/home/kavia/workspace/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/app/crud/order.py", "pattern": "/^    async def update_status($/", "language": "Python", "typeref": "typename:Optional[Order]", "kind": "member", "signature": "( self, db: AsyncSession, *, id: int, status: OrderStatus )", "scope": "CRUDOrder", "scopeKind": "class"}], "filename": "/home/kavia/workspace/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/app/crud/order.py", "hash": "8269568923e04890e043d2732eff68d7", "format-version": 4, "code-base-name": "default", "fields": [{"name": "order = CRUDOrder(Order)", "scope": "", "scopeKind": "", "description": "unavailable"}, {"name": "order_item = CRUDOrderItem(OrderItem)", "scope": "", "scopeKind": "", "description": "unavailable"}]}