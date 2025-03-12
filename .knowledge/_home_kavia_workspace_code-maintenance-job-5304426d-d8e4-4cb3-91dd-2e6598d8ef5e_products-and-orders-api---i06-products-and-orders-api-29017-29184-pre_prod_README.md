{
  "is_source_file": true,
  "format": "Markdown",
  "description": "A README file providing an overview, installation instructions, usage details, and development guidelines for the Product and Order Management API implemented with FastAPI and SQLAlchemy.",
  "external_files": [
    "<repository-url>",
    ".env.example",
    ".github/workflows/ci.yml"
  ],
  "external_methods": [
    "alembic upgrade head",
    "uvicorn app.main:app --reload",
    "docker build -t products-and-orders-api .",
    "docker run -p 8000:8000 products-and-orders-api",
    "docker-compose up -d",
    "pytest",
    "pytest --cov=app"
  ],
  "published": [],
  "classes": [],
  "methods": [],
  "calls": [],
  "search-terms": [
    "Product and Order Management",
    "FastAPI",
    "SQLAlchemy",
    "API Documentation",
    "Docker",
    "GitHub Actions"
  ],
  "state": 2,
  "file_id": 69,
  "knowledge_revision": 240,
  "git_revision": "b436a95daea430bb64bfe449e30952d32df443aa",
  "filename": "/home/kavia/workspace/code-maintenance-job-5304426d-d8e4-4cb3-91dd-2e6598d8ef5e/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/README.md",
  "hash": "90ef411afb4fd841db939f4e76ee0105",
  "format-version": 4,
  "code-base-name": "b9046lt",
  "revision_history": [
    {
      "240": "b436a95daea430bb64bfe449e30952d32df443aa"
    }
  ]
}