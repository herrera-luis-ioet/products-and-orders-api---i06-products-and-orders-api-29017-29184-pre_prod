{
  "is_source_file": true,
  "format": "Python",
  "description": "This module provides SQLAlchemy setup with engine and session management, along with a base class for models.",
  "external_files": [
    "app.config",
    "app.models.product",
    "app.models.order"
  ],
  "external_methods": [
    "Depends",
    "create_all"
  ],
  "published": [
    "get_db",
    "init_db"
  ],
  "classes": [
    {
      "name": "Base",
      "description": "Base class for all SQLAlchemy models."
    }
  ],
  "methods": [
    {
      "name": "get_db",
      "description": "Dependency for database session that yields an async session."
    },
    {
      "name": "init_db",
      "description": "Initializes the database by creating all tables."
    }
  ],
  "calls": [
    "app.models.product.Product",
    "app.models.order.Order",
    "app.models.order.OrderItem"
  ],
  "search-terms": [
    "SQLAlchemy",
    "database",
    "async",
    "session",
    "Base class"
  ],
  "state": 2,
  "file_id": 53,
  "knowledge_revision": 226,
  "git_revision": "16c27c10cb3f4ee6eb8de8b9a14ff8819c7da72c",
  "ctags": [],
  "filename": "/home/kavia/workspace/code-maintenance-job-5304426d-d8e4-4cb3-91dd-2e6598d8ef5e/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/app/database.py",
  "hash": "15d96ff25447265ccfa2bc698dbcc5f3",
  "format-version": 4,
  "code-base-name": "b9046lt",
  "revision_history": [
    {
      "226": "16c27c10cb3f4ee6eb8de8b9a14ff8819c7da72c"
    }
  ]
}