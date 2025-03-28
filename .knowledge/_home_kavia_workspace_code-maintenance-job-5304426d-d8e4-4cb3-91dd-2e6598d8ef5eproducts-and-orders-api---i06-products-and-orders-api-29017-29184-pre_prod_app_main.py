{
  "is_source_file": true,
  "format": "Python",
  "description": "Main FastAPI application module that configures the API, middleware, error handling, and routing.",
  "external_files": [
    "app.config",
    "app.database",
    "app.api.v1.api",
    "app.errors"
  ],
  "external_methods": [
    "app.database.init_db",
    "app.errors.setup_exception_handlers"
  ],
  "published": [
    "app",
    "health_check",
    "root"
  ],
  "classes": [],
  "methods": [
    {
      "name": "lifespan",
      "description": "Lifespan context manager for managing application startup and shutdown events."
    },
    {
      "name": "validation_exception_handler",
      "description": "Handles validation errors for incoming requests and returns a JSON response."
    },
    {
      "name": "order_validation_error_handler",
      "description": "Handles validation errors specific to orders and logs the error details."
    },
    {
      "name": "product_validation_error_handler",
      "description": "Handles validation errors specific to products and logs the error details."
    },
    {
      "name": "health_check",
      "description": "Health check endpoint that returns the API's status and version."
    },
    {
      "name": "root",
      "description": "Root endpoint that returns basic information about the API."
    }
  ],
  "calls": [
    "logging.basicConfig",
    "logger.getLogger",
    "asynccontextmanager",
    "app.add_middleware",
    "JSONResponse",
    "jsonable_encoder",
    "setup_exception_handlers",
    "api_router"
  ],
  "search-terms": [
    "FastAPI",
    "API",
    "products",
    "orders"
  ],
  "state": 2,
  "file_id": 52,
  "knowledge_revision": 229,
  "git_revision": "009342fdb76af178c6a05f2090956477d317308e",
  "ctags": [],
  "filename": "/home/kavia/workspace/code-maintenance-job-5304426d-d8e4-4cb3-91dd-2e6598d8ef5e/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/app/main.py",
  "hash": "9dc430fbcf8469cddc11082a0e66ffd0",
  "format-version": 4,
  "code-base-name": "b9046lt",
  "revision_history": [
    {
      "229": "009342fdb76af178c6a05f2090956477d317308e"
    }
  ]
}