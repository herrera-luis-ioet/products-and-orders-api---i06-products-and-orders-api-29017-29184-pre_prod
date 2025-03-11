{"is_source_file": true, "format": "Python", "description": "API endpoints for product management, providing functionality to create, read, update, and delete products.", "external_files": ["app/crud/product", "app/database", "app/schemas/product", "app/config"], "external_methods": ["app.crud.product.product_crud.get_active", "app.crud.product.product_crud.get_multi", "app.crud.product.product_crud.get", "app.crud.product.product_crud.get_by_sku", "app.crud.product.product_crud.create", "app.crud.product.product_crud.update", "app.crud.product.product_crud.remove", "app.crud.product.product_crud.search_products", "app.crud.product.product_crud.get_by_category"], "published": [], "classes": [], "methods": [{"name": "Any list_products( db: AsyncSession = Depends(get_db), skip: int = Query(0, ge=0, description=\"Number of products to skip\"), limit: int = Query(settings.PAGINATION_PAGE_SIZE, ge=1, le=100, description=\"Number of products to return\"), sort_by: Optional[str] = Query(None, description=\"Field to sort by\"), sort_desc: bool = Query(False, description=\"Sort in descending order\"), is_active: Optional[bool] = Query(None, description=\"Filter by active status\") )", "description": "Lists all products with pagination, filtering, and sorting options.", "scope": "", "scopeKind": ""}, {"name": "Any get_product( product_id: int = Path(..., gt=0, description=\"The ID of the product to get\"), db: AsyncSession = Depends(get_db) )", "description": "Retrieves a specific product by its ID.", "scope": "", "scopeKind": ""}, {"name": "Any create_product( product_in: ProductCreate, db: AsyncSession = Depends(get_db) )", "description": "Creates a new product with the provided data.", "scope": "", "scopeKind": ""}, {"name": "Any update_product( product_in: ProductUpdate, product_id: int = Path(..., gt=0, description=\"The ID of the product to update\"), db: AsyncSession = Depends(get_db) )", "description": "Updates an existing product based on its ID and input data.", "scope": "", "scopeKind": ""}, {"name": "Any delete_product( product_id: int = Path(..., gt=0, description=\"The ID of the product to delete\"), db: AsyncSession = Depends(get_db) )", "description": "Deletes a product by its ID.", "scope": "", "scopeKind": ""}, {"name": "Any search_products( query: str = Query(..., min_length=1, description=\"Search query string\"), db: AsyncSession = Depends(get_db), skip: int = Query(0, ge=0, description=\"Number of products to skip\"), limit: int = Query(settings.PAGINATION_PAGE_SIZE, ge=1, le=100, description=\"Number of products to return\") )", "description": "Searches for products by name or description based on the provided query.", "scope": "", "scopeKind": ""}, {"name": "Any get_products_by_category( category: str = Path(..., description=\"Category name\"), db: AsyncSession = Depends(get_db), skip: int = Query(0, ge=0, description=\"Number of products to skip\"), limit: int = Query(settings.PAGINATION_PAGE_SIZE, ge=1, le=100, description=\"Number of products to return\") )", "description": "Retrieves products filtered by a specified category.", "scope": "", "scopeKind": ""}], "calls": [], "search-terms": ["product management", "API endpoints", "list products", "get product", "create product", "update product", "delete product", "search products", "get products by category"], "state": 2, "file_id": 23, "knowledge_revision": 49, "git_revision": "", "ctags": [{"_type": "tag", "name": "create_product", "path": "/home/kavia/workspace/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/app/api/v1/endpoints/products.py", "pattern": "/^async def create_product($/", "language": "Python", "typeref": "typename:Any", "kind": "function", "signature": "( product_in: ProductCreate, db: AsyncSession = Depends(get_db) )"}, {"_type": "tag", "name": "delete_product", "path": "/home/kavia/workspace/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/app/api/v1/endpoints/products.py", "pattern": "/^async def delete_product($/", "language": "Python", "typeref": "typename:Any", "kind": "function", "signature": "( product_id: int = Path(..., gt=0, description=\"The ID of the product to delete\"), db: AsyncSession = Depends(get_db) )"}, {"_type": "tag", "name": "get_product", "path": "/home/kavia/workspace/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/app/api/v1/endpoints/products.py", "pattern": "/^async def get_product($/", "language": "Python", "typeref": "typename:Any", "kind": "function", "signature": "( product_id: int = Path(..., gt=0, description=\"The ID of the product to get\"), db: AsyncSession = Depends(get_db) )"}, {"_type": "tag", "name": "get_products_by_category", "path": "/home/kavia/workspace/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/app/api/v1/endpoints/products.py", "pattern": "/^async def get_products_by_category($/", "language": "Python", "typeref": "typename:Any", "kind": "function", "signature": "( category: str = Path(..., description=\"Category name\"), db: AsyncSession = Depends(get_db), skip: int = Query(0, ge=0, description=\"Number of products to skip\"), limit: int = Query(settings.PAGINATION_PAGE_SIZE, ge=1, le=100, description=\"Number of products to return\") )"}, {"_type": "tag", "name": "list_products", "path": "/home/kavia/workspace/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/app/api/v1/endpoints/products.py", "pattern": "/^async def list_products($/", "language": "Python", "typeref": "typename:Any", "kind": "function", "signature": "( db: AsyncSession = Depends(get_db), skip: int = Query(0, ge=0, description=\"Number of products to skip\"), limit: int = Query(settings.PAGINATION_PAGE_SIZE, ge=1, le=100, description=\"Number of products to return\"), sort_by: Optional[str] = Query(None, description=\"Field to sort by\"), sort_desc: bool = Query(False, description=\"Sort in descending order\"), is_active: Optional[bool] = Query(None, description=\"Filter by active status\") )"}, {"_type": "tag", "name": "product_crud", "path": "/home/kavia/workspace/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/app/api/v1/endpoints/products.py", "pattern": "/^from app.crud.product import product as product_crud$/", "language": "Python", "kind": "unknown", "nameref": "unknown:product"}, {"_type": "tag", "name": "router", "path": "/home/kavia/workspace/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/app/api/v1/endpoints/products.py", "pattern": "/^router = APIRouter()$/", "language": "Python", "kind": "variable"}, {"_type": "tag", "name": "search_products", "path": "/home/kavia/workspace/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/app/api/v1/endpoints/products.py", "pattern": "/^async def search_products($/", "language": "Python", "typeref": "typename:Any", "kind": "function", "signature": "( query: str = Query(..., min_length=1, description=\"Search query string\"), db: AsyncSession = Depends(get_db), skip: int = Query(0, ge=0, description=\"Number of products to skip\"), limit: int = Query(settings.PAGINATION_PAGE_SIZE, ge=1, le=100, description=\"Number of products to return\") )"}, {"_type": "tag", "name": "update_product", "path": "/home/kavia/workspace/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/app/api/v1/endpoints/products.py", "pattern": "/^async def update_product($/", "language": "Python", "typeref": "typename:Any", "kind": "function", "signature": "( product_in: ProductUpdate, product_id: int = Path(..., gt=0, description=\"The ID of the product to update\"), db: AsyncSession = Depends(get_db) )"}], "filename": "/home/kavia/workspace/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/app/api/v1/endpoints/products.py", "hash": "6b3027686ec7b001e4f995399ed43d52", "format-version": 4, "code-base-name": "default", "fields": [{"name": "router = APIRouter()", "scope": "", "scopeKind": "", "description": "unavailable"}], "revision_history": [{"49": ""}]}