{
  "is_source_file": true,
  "format": "Python",
  "description": "This file contains an asynchronous function to create database tables using SQLAlchemy.",
  "external_files": [
    "app/database",
    "app/models/product",
    "app/models/order"
  ],
  "external_methods": [
    "engine.begin",
    "conn.run_sync",
    "Base.metadata.create_all"
  ],
  "published": [],
  "classes": [],
  "methods": [
    {
      "name": "create_tables",
      "description": "An asynchronous function that creates all tables defined in the database metadata."
    }
  ],
  "calls": [
    "asyncio.run"
  ],
  "search-terms": [
    "create_tables",
    "asyncio",
    "SQLAlchemy",
    "database initialization"
  ],
  "state": 2,
  "file_id": 68,
  "knowledge_revision": 238,
  "git_revision": "4586f58059eec306d9691b476a20a49522f4c730",
  "ctags": [],
  "filename": "/home/kavia/workspace/code-maintenance-job-5304426d-d8e4-4cb3-91dd-2e6598d8ef5e/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/create_tables.py",
  "hash": "1bffa539ee3ba0e6ec99e15280bb03d5",
  "format-version": 4,
  "code-base-name": "b9046lt",
  "revision_history": [
    {
      "238": "4586f58059eec306d9691b476a20a49522f4c730"
    }
  ]
}