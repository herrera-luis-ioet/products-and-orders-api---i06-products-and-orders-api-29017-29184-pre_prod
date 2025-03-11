{"is_source_file": true, "format": "Python", "description": "Dependency injection functions for FastAPI routes providing common dependencies used across API routes, including database sessions, pagination parameters, and authentication.", "external_files": ["app/config.py", "app/database.py", "app/crud/product.py", "app/crud/order.py"], "external_methods": ["app.database.get_db", "app.crud.product.product.get", "app.crud.order.order.get"], "published": ["get_pagination_params", "get_sort_params", "get_correlation_id", "validate_product_exists", "validate_order_exists"], "classes": [], "methods": [{"name": "Tuple[int,int] get_pagination_params( skip: int = Query(0, ge=0, description=\"Number of items to skip\"), limit: int = Query( settings.PAGINATION_PAGE_SIZE, ge=1, le=100, description=\"Number of items to return\" ), )", "description": "Get pagination parameters from query parameters.", "scope": "", "scopeKind": ""}, {"name": "Tuple[Optional[str],bool] get_sort_params( sort_by: Optional[str] = Query(None, description=\"Field to sort by\"), sort_desc: bool = Query(False, description=\"Sort in descending order\"), )", "description": "Get sorting parameters from query parameters.", "scope": "", "scopeKind": ""}, {"name": "str get_correlation_id( x_correlation_id: Optional[str] = Header(None, description=\"Correlation ID for request tracing\") )", "description": "Get or generate a correlation ID for request tracing.", "scope": "", "scopeKind": ""}, {"name": "None validate_product_exists(product_id: int, db: DBSession)", "description": "Validate that a product exists.", "scope": "", "scopeKind": ""}, {"name": "None validate_order_exists(order_id: int, db: DBSession)", "description": "Validate that an order exists.", "scope": "", "scopeKind": ""}], "calls": ["app.crud.product.product.get", "app.crud.order.order.get"], "search-terms": ["FastAPI", "dependency injection", "pagination", "sorting", "correlation id", "validate product", "validate order"], "state": 2, "file_id": 25, "knowledge_revision": 54, "git_revision": "", "ctags": [{"_type": "tag", "name": "CorrelationId", "path": "/home/kavia/workspace/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/app/dependencies.py", "pattern": "/^CorrelationId = Annotated[str, Depends(get_correlation_id)]$/", "language": "Python", "kind": "variable"}, {"_type": "tag", "name": "DBSession", "path": "/home/kavia/workspace/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/app/dependencies.py", "pattern": "/^DBSession = Annotated[AsyncSession, Depends(get_db)]$/", "language": "Python", "kind": "variable"}, {"_type": "tag", "name": "PaginationParams", "path": "/home/kavia/workspace/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/app/dependencies.py", "pattern": "/^PaginationParams = Annotated[Tuple[int, int], Depends(get_pagination_params)]$/", "language": "Python", "kind": "variable"}, {"_type": "tag", "name": "SortParams", "path": "/home/kavia/workspace/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/app/dependencies.py", "pattern": "/^SortParams = Annotated[Tuple[Optional[str], bool], Depends(get_sort_params)]$/", "language": "Python", "kind": "variable"}, {"_type": "tag", "name": "get_correlation_id", "path": "/home/kavia/workspace/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/app/dependencies.py", "pattern": "/^def get_correlation_id($/", "language": "Python", "typeref": "typename:str", "kind": "function", "signature": "( x_correlation_id: Optional[str] = Header(None, description=\"Correlation ID for request tracing\") )"}, {"_type": "tag", "name": "get_pagination_params", "path": "/home/kavia/workspace/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/app/dependencies.py", "pattern": "/^def get_pagination_params($/", "language": "Python", "typeref": "typename:Tuple[int,int]", "kind": "function", "signature": "( skip: int = Query(0, ge=0, description=\"Number of items to skip\"), limit: int = Query( settings.PAGINATION_PAGE_SIZE, ge=1, le=100, description=\"Number of items to return\" ), )"}, {"_type": "tag", "name": "get_sort_params", "path": "/home/kavia/workspace/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/app/dependencies.py", "pattern": "/^def get_sort_params($/", "language": "Python", "typeref": "typename:Tuple[Optional[str],bool]", "kind": "function", "signature": "( sort_by: Optional[str] = Query(None, description=\"Field to sort by\"), sort_desc: bool = Query(False, description=\"Sort in descending order\"), )"}, {"_type": "tag", "name": "order_crud", "path": "/home/kavia/workspace/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/app/dependencies.py", "pattern": "/^    from app.crud.order import order as order_crud$/", "file": true, "language": "Python", "kind": "unknown", "scope": "validate_order_exists", "scopeKind": "function", "nameref": "unknown:order"}, {"_type": "tag", "name": "product_crud", "path": "/home/kavia/workspace/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/app/dependencies.py", "pattern": "/^    from app.crud.product import product as product_crud$/", "file": true, "language": "Python", "kind": "unknown", "scope": "validate_product_exists", "scopeKind": "function", "nameref": "unknown:product"}, {"_type": "tag", "name": "validate_order_exists", "path": "/home/kavia/workspace/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/app/dependencies.py", "pattern": "/^def validate_order_exists(order_id: int, db: DBSession) -> None:$/", "language": "Python", "typeref": "typename:None", "kind": "function", "signature": "(order_id: int, db: DBSession)"}, {"_type": "tag", "name": "validate_product_exists", "path": "/home/kavia/workspace/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/app/dependencies.py", "pattern": "/^def validate_product_exists(product_id: int, db: DBSession) -> None:$/", "language": "Python", "typeref": "typename:None", "kind": "function", "signature": "(product_id: int, db: DBSession)"}], "filename": "/home/kavia/workspace/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/app/dependencies.py", "hash": "00bb2f22fafc63ae77bcd0c3d9ced6a9", "format-version": 4, "code-base-name": "default", "fields": [{"name": "CorrelationId = Annotated[str, Depends(get_correlation_id)]", "scope": "", "scopeKind": "", "description": "unavailable"}, {"name": "DBSession = Annotated[AsyncSession, Depends(get_db)]", "scope": "", "scopeKind": "", "description": "unavailable"}, {"name": "PaginationParams = Annotated[Tuple[int, int], Depends(get_pagination_params)]", "scope": "", "scopeKind": "", "description": "unavailable"}, {"name": "SortParams = Annotated[Tuple[Optional[str], bool], Depends(get_sort_params)]", "scope": "", "scopeKind": "", "description": "unavailable"}], "revision_history": [{"54": ""}]}