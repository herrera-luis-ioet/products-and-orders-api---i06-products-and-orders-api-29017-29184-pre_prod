{
  "is_source_file": true,
  "format": "Python",
  "description": "Custom exceptions and exception handlers for the API, providing structured error responses and logging.",
  "external_files": [
    "from fastapi import FastAPI, Request, status",
    "from fastapi.encoders import jsonable_encoder",
    "from fastapi.exceptions import RequestValidationError",
    "from fastapi.responses import JSONResponse",
    "from pydantic import ValidationError",
    "from sqlalchemy.exc import IntegrityError, SQLAlchemyError",
    "from app import __app_name__"
  ],
  "external_methods": [
    "FastAPI",
    "Request",
    "status",
    "jsonable_encoder",
    "RequestValidationError",
    "JSONResponse",
    "ValidationError",
    "IntegrityError",
    "SQLAlchemyError",
    "__app_name__"
  ],
  "published": [
    "APIError",
    "NotFoundError",
    "BadRequestError",
    "ConflictError",
    "UnauthorizedError",
    "ForbiddenError",
    "OrderValidationError",
    "ProductValidationError",
    "ValidationErrorResponse",
    "setup_exception_handlers"
  ],
  "classes": [
    {
      "name": "APIError",
      "description": "Base class for all API errors."
    },
    {
      "name": "NotFoundError",
      "description": "Error raised when a requested resource is not found."
    },
    {
      "name": "BadRequestError",
      "description": "Error raised when the request is malformed or invalid."
    },
    {
      "name": "ConflictError",
      "description": "Error raised when there is a conflict with the current state of a resource."
    },
    {
      "name": "UnauthorizedError",
      "description": "Error raised when authentication is required but not provided or invalid."
    },
    {
      "name": "ForbiddenError",
      "description": "Error raised when the authenticated user doesn't have permission."
    },
    {
      "name": "OrderValidationError",
      "description": "Error raised when order validation fails."
    },
    {
      "name": "ProductValidationError",
      "description": "Error raised when product validation fails."
    },
    {
      "name": "ValidationErrorResponse",
      "description": "Custom response for validation errors."
    }
  ],
  "methods": [
    {
      "name": "setup_exception_handlers",
      "description": "Set up exception handlers for the FastAPI application."
    }
  ],
  "calls": [
    "logger.error",
    "JSONResponse"
  ],
  "search-terms": [
    "custom exceptions",
    "API error handling",
    "FastAPI error handlers",
    "validation errors"
  ],
  "state": 2,
  "file_id": 47,
  "knowledge_revision": 223,
  "git_revision": "7f14946b607f1dc5e2b27ea2a09034a3b648b508",
  "ctags": [],
  "filename": "/home/kavia/workspace/code-maintenance-job-5304426d-d8e4-4cb3-91dd-2e6598d8ef5e/products-and-orders-api---i06-products-and-orders-api-29017-29184-pre_prod/app/errors.py",
  "hash": "a81e58a514f88fc1bbe61accd2dfa2ea",
  "format-version": 4,
  "code-base-name": "b9046lt",
  "revision_history": [
    {
      "223": "7f14946b607f1dc5e2b27ea2a09034a3b648b508"
    }
  ]
}