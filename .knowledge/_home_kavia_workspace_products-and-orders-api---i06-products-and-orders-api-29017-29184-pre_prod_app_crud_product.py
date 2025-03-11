{"is_source_file": true, "format": "Python", "description": "This file defines a CRUDProduct class that implements CRUD operations specific to a Product model using SQLAlchemy.", "external_files": ["app/crud/base", "app/models/product", "app/schemas/product"], "external_methods": ["CRUDBase.get", "CRUDBase.delete"], "published": ["CRUDProduct", "get_by_sku", "get_by_category", "get_active", "update_inventory", "search_products", "remove"], "classes": [{"name": "CRUDProduct", "description": "Extends CRUDBase with product-specific functionality for managing product records."}], "methods": [{"name": "Optional[Product] get_by_sku(self, db: AsyncSession, *, sku: str)", "description": "Retrieves a product by its SKU.", "scope": "CRUDProduct", "scopeKind": "class"}, {"name": "List[Product] get_by_category( self, db: AsyncSession, *, category: str, skip: int = 0, limit: int = 100 )", "description": "Retrieves products filtered by category with pagination.", "scope": "CRUDProduct", "scopeKind": "class"}, {"name": "List[Product] get_active( self, db: AsyncSession, *, skip: int = 0, limit: int = 100 )", "description": "Retrieves active products with pagination.", "scope": "CRUDProduct", "scopeKind": "class"}, {"name": "Optional[Product] update_inventory( self, db: AsyncSession, *, id: int, quantity_change: int )", "description": "Updates the inventory count for a specific product.", "scope": "CRUDProduct", "scopeKind": "class"}, {"name": "List[Product] search_products( self, db: AsyncSession, *, query: str, skip: int = 0, limit: int = 100 )", "description": "Searches for products by name or description.", "scope": "CRUDProduct", "scopeKind": "class"}, {"name": "Optional[Product] remove(self, db: AsyncSession, *, id: int)", "description": "Removes a product based on its ID.", "scope": "CRUDProduct", "scopeKind": "class"}], "calls": ["select", "func.lower", "AsyncSession.execute", "db.add", "db.commit", "db.refresh"], "search-terms": ["CRUD operations", "Product management", "Inventory management"], "state": 2, "file_id": 16, "knowledge_revision": 133, "git_revision": "370184de095522425ca19c1e5d95b8bdc488032e", "revision_history": [{"35": ""}, {"133": "370184de095522425ca19c1e5d95b8bdc488032e"}], "ctags": [{"_type": "tag", "name": "CRUDProduct", "path": "/home/kavia/workspace/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/app/crud/product.py", "pattern": "/^class CRUDProduct(CRUDBase[Product, ProductCreate, ProductUpdate]):$/", "language": "Python", "kind": "class"}, {"_type": "tag", "name": "get_active", "path": "/home/kavia/workspace/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/app/crud/product.py", "pattern": "/^    async def get_active($/", "language": "Python", "typeref": "typename:List[Product]", "kind": "member", "signature": "( self, db: AsyncSession, *, skip: int = 0, limit: int = 100 )", "scope": "CRUDProduct", "scopeKind": "class"}, {"_type": "tag", "name": "get_by_category", "path": "/home/kavia/workspace/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/app/crud/product.py", "pattern": "/^    async def get_by_category($/", "language": "Python", "typeref": "typename:List[Product]", "kind": "member", "signature": "( self, db: AsyncSession, *, category: str, skip: int = 0, limit: int = 100 )", "scope": "CRUDProduct", "scopeKind": "class"}, {"_type": "tag", "name": "get_by_sku", "path": "/home/kavia/workspace/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/app/crud/product.py", "pattern": "/^    async def get_by_sku(self, db: AsyncSession, *, sku: str) -> Optional[Product]:$/", "language": "Python", "typeref": "typename:Optional[Product]", "kind": "member", "signature": "(self, db: AsyncSession, *, sku: str)", "scope": "CRUDProduct", "scopeKind": "class"}, {"_type": "tag", "name": "product", "path": "/home/kavia/workspace/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/app/crud/product.py", "pattern": "/^product = CRUDProduct(Product)$/", "language": "Python", "kind": "variable"}, {"_type": "tag", "name": "remove", "path": "/home/kavia/workspace/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/app/crud/product.py", "pattern": "/^    async def remove(self, db: AsyncSession, *, id: int) -> Optional[Product]:$/", "language": "Python", "typeref": "typename:Optional[Product]", "kind": "member", "signature": "(self, db: AsyncSession, *, id: int)", "scope": "CRUDProduct", "scopeKind": "class"}, {"_type": "tag", "name": "search_products", "path": "/home/kavia/workspace/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/app/crud/product.py", "pattern": "/^    async def search_products($/", "language": "Python", "typeref": "typename:List[Product]", "kind": "member", "signature": "( self, db: AsyncSession, *, query: str, skip: int = 0, limit: int = 100 )", "scope": "CRUDProduct", "scopeKind": "class"}, {"_type": "tag", "name": "update_inventory", "path": "/home/kavia/workspace/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/app/crud/product.py", "pattern": "/^    async def update_inventory($/", "language": "Python", "typeref": "typename:Optional[Product]", "kind": "member", "signature": "( self, db: AsyncSession, *, id: int, quantity_change: int )", "scope": "CRUDProduct", "scopeKind": "class"}], "filename": "/home/kavia/workspace/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/app/crud/product.py", "hash": "0852761bd18b4ecf5ced42ae49c1486f", "format-version": 4, "code-base-name": "default", "fields": [{"name": "product = CRUDProduct(Product)", "scope": "", "scopeKind": "", "description": "unavailable"}]}