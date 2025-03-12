{
  "is_source_file": true,
  "format": "Python",
  "description": "This file defines middleware components for a FastAPI application, including request logging and timing functionalities.",
  "external_files": [
    "app/__app_name__",
    "app/config"
  ],
  "external_methods": [
    "settings.ENV"
  ],
  "published": [
    "setup_middlewares"
  ],
  "classes": [
    {
      "name": "RequestLoggingMiddleware",
      "description": "Middleware for logging request and response information, capturing details about incoming requests and outgoing responses."
    },
    {
      "name": "TimingMiddleware",
      "description": "Middleware for timing request processing, adding processing time information to response headers."
    }
  ],
  "methods": [
    {
      "name": "dispatch",
      "description": "Processes the request and logs information in the RequestLoggingMiddleware."
    },
    {
      "name": "dispatch",
      "description": "Processes the request and adds timing information in the TimingMiddleware."
    },
    {
      "name": "setup_middlewares",
      "description": "Sets up all middleware for the FastAPI application, adding necessary middleware based on the environment."
    }
  ],
  "calls": [
    "call_next",
    "logger.info",
    "logger.exception"
  ],
  "search-terms": [
    "FastAPI middleware",
    "logging middleware",
    "timing middleware"
  ],
  "state": 2,
  "file_id": 65,
  "knowledge_revision": 239,
  "git_revision": "d388d9a7e7019e9bd32c3ada33343fc29b1bfd8a",
  "ctags": [],
  "filename": "/home/kavia/workspace/code-maintenance-job-5304426d-d8e4-4cb3-91dd-2e6598d8ef5e/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/app/middleware.py",
  "hash": "6af496a40326d14b2156bcbd7ff3e2e1",
  "format-version": 4,
  "code-base-name": "b9046lt",
  "revision_history": [
    {
      "239": "d388d9a7e7019e9bd32c3ada33343fc29b1bfd8a"
    }
  ]
}