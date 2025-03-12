{
  "is_source_file": true,
  "format": "Python",
  "description": "A base class for CRUD operations using SQLAlchemy and Pydantic, providing methods to create, read, update, and delete records in a database.",
  "external_files": [
    "app.database"
  ],
  "external_methods": [
    "db.execute",
    "db.commit",
    "db.refresh",
    "db.delete"
  ],
  "published": [],
  "classes": [
    {
      "name": "CRUDBase",
      "description": "A generic base class for performing CRUD operations on SQLAlchemy models."
    }
  ],
  "methods": [
    {
      "name": "get",
      "description": "Fetch a single record by ID from the database."
    },
    {
      "name": "get_multi",
      "description": "Fetch multiple records from the database with pagination."
    },
    {
      "name": "create",
      "description": "Create a new record in the database."
    },
    {
      "name": "update",
      "description": "Update an existing record in the database."
    },
    {
      "name": "delete",
      "description": "Delete a record by ID from the database."
    }
  ],
  "calls": [
    "select",
    "jsonable_encoder"
  ],
  "search-terms": [
    "CRUD",
    "base",
    "operations",
    "SQLAlchemy",
    "Pydantic"
  ],
  "state": 2,
  "file_id": 61,
  "knowledge_revision": 232,
  "git_revision": "370184de095522425ca19c1e5d95b8bdc488032e",
  "ctags": [],
  "filename": "/home/kavia/workspace/code-maintenance-job-5304426d-d8e4-4cb3-91dd-2e6598d8ef5e/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/app/crud/base.py",
  "hash": "b89aef37f3ca65afaf30dc80a1a106f2",
  "format-version": 4,
  "code-base-name": "b9046lt",
  "revision_history": [
    {
      "232": "370184de095522425ca19c1e5d95b8bdc488032e"
    }
  ]
}