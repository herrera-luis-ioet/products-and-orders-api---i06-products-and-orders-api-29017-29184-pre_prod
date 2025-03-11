{"is_source_file": true, "format": "Python", "description": "This file contains pytest configuration and fixtures for testing an application, including database fixtures, API client fixtures, and test data fixtures.", "external_files": ["app/__init__.py", "app/api/v1/api.py", "app/config.py", "app/database.py", "app/models/order.py", "app/models/product.py"], "external_methods": ["app.database.get_db"], "published": ["test_settings", "override_settings", "engine", "db_session", "override_get_db", "app", "client", "product_data", "order_data", "test_products", "test_orders"], "classes": [], "methods": [{"name": "Settings test_settings()", "description": "Creates test settings with an in-memory SQLite database.", "scope": "", "scopeKind": ""}, {"name": "None override_settings(test_settings: Settings)", "description": "Overrides global settings with test settings for testing purposes.", "scope": "", "scopeKind": ""}, {"name": "engine()", "description": "Creates an asynchronous SQLAlchemy engine for tests.", "scope": "", "scopeKind": ""}, {"name": "AsyncGenerator[AsyncSession,None] db_session(engine)", "description": "Creates an asynchronous SQLAlchemy session for tests.", "scope": "", "scopeKind": ""}, {"name": "AsyncGenerator override_get_db(db_session: AsyncSession)", "description": "Overrides the get_db dependency with a database session for tests.", "scope": "", "scopeKind": ""}, {"name": "FastAPI app(override_get_db)", "description": "Creates a test FastAPI application.", "scope": "", "scopeKind": ""}, {"name": "AsyncGenerator[AsyncClient,None] client(app: FastAPI)", "description": "Creates an asynchronous HTTPX client for testing the app.", "scope": "", "scopeKind": ""}, {"name": "Dict product_data()", "description": "Generates test data for a product.", "scope": "", "scopeKind": ""}, {"name": "Dict order_data()", "description": "Generates test data for an order.", "scope": "", "scopeKind": ""}, {"name": "List[Product] test_products(db_session: AsyncSession)", "description": "Creates test product entries in the database.", "scope": "", "scopeKind": ""}, {"name": "List[Order] test_orders(db_session: AsyncSession, test_products: List[Product])", "description": "Creates test order entries in the database.", "scope": "", "scopeKind": ""}, {"name": "_get_test_db()", "scope": "override_get_db", "scopeKind": "function", "description": "unavailable"}], "calls": [], "search-terms": ["pytest", "fixtures", "asynchronous", "FastAPI", "database testing"], "state": 2, "file_id": 30, "knowledge_revision": 64, "git_revision": "", "ctags": [{"_type": "tag", "name": "_get_test_db", "path": "/home/kavia/workspace/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/tests/conftest.py", "pattern": "/^    async def _get_test_db():$/", "file": true, "language": "Python", "kind": "function", "signature": "()", "scope": "override_get_db", "scopeKind": "function"}, {"_type": "tag", "name": "app", "path": "/home/kavia/workspace/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/tests/conftest.py", "pattern": "/^async def app(override_get_db) -> FastAPI:$/", "language": "Python", "typeref": "typename:FastAPI", "kind": "function", "signature": "(override_get_db)"}, {"_type": "tag", "name": "client", "path": "/home/kavia/workspace/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/tests/conftest.py", "pattern": "/^async def client(app: FastAPI) -> AsyncGenerator[AsyncClient, None]:$/", "language": "Python", "typeref": "typename:AsyncGenerator[AsyncClient,None]", "kind": "function", "signature": "(app: FastAPI)"}, {"_type": "tag", "name": "db_session", "path": "/home/kavia/workspace/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/tests/conftest.py", "pattern": "/^async def db_session(engine) -> AsyncGenerator[AsyncSession, None]:$/", "language": "Python", "typeref": "typename:AsyncGenerator[AsyncSession,None]", "kind": "function", "signature": "(engine)"}, {"_type": "tag", "name": "engine", "path": "/home/kavia/workspace/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/tests/conftest.py", "pattern": "/^async def engine():$/", "language": "Python", "kind": "function", "signature": "()"}, {"_type": "tag", "name": "main_app", "path": "/home/kavia/workspace/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/tests/conftest.py", "pattern": "/^    from app.main import app as main_app$/", "file": true, "language": "Python", "kind": "unknown", "scope": "app", "scopeKind": "function", "nameref": "unknown:app"}, {"_type": "tag", "name": "order_data", "path": "/home/kavia/workspace/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/tests/conftest.py", "pattern": "/^def order_data() -> Dict:$/", "language": "Python", "typeref": "typename:Dict", "kind": "function", "signature": "()"}, {"_type": "tag", "name": "override_get_db", "path": "/home/kavia/workspace/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/tests/conftest.py", "pattern": "/^async def override_get_db(db_session: AsyncSession) -> AsyncGenerator:$/", "language": "Python", "typeref": "typename:AsyncGenerator", "kind": "function", "signature": "(db_session: AsyncSession)"}, {"_type": "tag", "name": "override_settings", "path": "/home/kavia/workspace/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/tests/conftest.py", "pattern": "/^def override_settings(test_settings: Settings) -> None:$/", "language": "Python", "typeref": "typename:None", "kind": "function", "signature": "(test_settings: Settings)"}, {"_type": "tag", "name": "product_data", "path": "/home/kavia/workspace/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/tests/conftest.py", "pattern": "/^def product_data() -> Dict:$/", "language": "Python", "typeref": "typename:Dict", "kind": "function", "signature": "()"}, {"_type": "tag", "name": "test_orders", "path": "/home/kavia/workspace/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/tests/conftest.py", "pattern": "/^async def test_orders(db_session: AsyncSession, test_products: List[Product]) -> List[Order]:$/", "language": "Python", "typeref": "typename:List[Order]", "kind": "function", "signature": "(db_session: AsyncSession, test_products: List[Product])"}, {"_type": "tag", "name": "test_products", "path": "/home/kavia/workspace/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/tests/conftest.py", "pattern": "/^async def test_products(db_session: AsyncSession) -> List[Product]:$/", "language": "Python", "typeref": "typename:List[Product]", "kind": "function", "signature": "(db_session: AsyncSession)"}, {"_type": "tag", "name": "test_settings", "path": "/home/kavia/workspace/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/tests/conftest.py", "pattern": "/^def test_settings() -> Settings:$/", "language": "Python", "typeref": "typename:Settings", "kind": "function", "signature": "()"}], "filename": "/home/kavia/workspace/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/tests/conftest.py", "hash": "7785f0f6e2be1bcf8aa853f026a7aa71", "format-version": 4, "code-base-name": "default", "revision_history": [{"64": ""}]}