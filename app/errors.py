"""
Custom exceptions and exception handlers.

This module provides custom exception classes and exception handlers
for consistent error responses across the API.
"""

import logging
from typing import Any, Dict, List, Optional, Union

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from app import __app_name__


logger = logging.getLogger(__app_name__)


class APIError(Exception):
    """
    Base class for all API errors.
    
    Attributes:
        status_code: HTTP status code
        detail: Error detail message
        code: Error code for client reference
        headers: Additional headers to include in the response
    """
    
    def __init__(
        self,
        status_code: int,
        detail: str,
        code: Optional[str] = None,
        headers: Optional[Dict[str, str]] = None,
    ):
        self.status_code = status_code
        self.detail = detail
        self.code = code or "error"
        self.headers = headers
        super().__init__(detail)


class NotFoundError(APIError):
    """
    Error raised when a requested resource is not found.
    
    Attributes:
        detail: Error detail message
        code: Error code for client reference
        headers: Additional headers to include in the response
    """
    
    def __init__(
        self,
        detail: str = "Resource not found",
        code: str = "not_found",
        headers: Optional[Dict[str, str]] = None,
    ):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail,
            code=code,
            headers=headers,
        )


class BadRequestError(APIError):
    """
    Error raised when the request is malformed or invalid.
    
    Attributes:
        detail: Error detail message
        code: Error code for client reference
        headers: Additional headers to include in the response
    """
    
    def __init__(
        self,
        detail: str = "Bad request",
        code: str = "bad_request",
        headers: Optional[Dict[str, str]] = None,
    ):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
            code=code,
            headers=headers,
        )


class ConflictError(APIError):
    """
    Error raised when there is a conflict with the current state of a resource.
    
    Attributes:
        detail: Error detail message
        code: Error code for client reference
        headers: Additional headers to include in the response
    """
    
    def __init__(
        self,
        detail: str = "Resource conflict",
        code: str = "conflict",
        headers: Optional[Dict[str, str]] = None,
    ):
        super().__init__(
            status_code=status.HTTP_409_CONFLICT,
            detail=detail,
            code=code,
            headers=headers,
        )


class UnauthorizedError(APIError):
    """
    Error raised when authentication is required but not provided or invalid.
    
    Attributes:
        detail: Error detail message
        code: Error code for client reference
        headers: Additional headers to include in the response
    """
    
    def __init__(
        self,
        detail: str = "Not authenticated",
        code: str = "unauthorized",
        headers: Optional[Dict[str, str]] = None,
    ):
        if headers is None:
            headers = {"WWW-Authenticate": "Bearer"}
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            code=code,
            headers=headers,
        )


class ForbiddenError(APIError):
    """
    Error raised when the authenticated user doesn't have permission.
    
    Attributes:
        detail: Error detail message
        code: Error code for client reference
        headers: Additional headers to include in the response
    """
    
    def __init__(
        self,
        detail: str = "Not authorized to perform this action",
        code: str = "forbidden",
        headers: Optional[Dict[str, str]] = None,
    ):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
            code=code,
            headers=headers,
        )


class ValidationErrorResponse(JSONResponse):
    """
    Custom response for validation errors.
    
    Formats validation errors in a consistent way.
    """
    
    def __init__(
        self,
        status_code: int,
        content: Dict[str, Any],
        headers: Optional[Dict[str, str]] = None,
    ):
        super().__init__(
            status_code=status_code,
            content=content,
            headers=headers,
        )


# PUBLIC_INTERFACE
def setup_exception_handlers(app: FastAPI) -> None:
    """
    Set up exception handlers for the FastAPI application.
    
    Args:
        app: The FastAPI application instance
        
    Example:
        ```python
        app = FastAPI()
        setup_exception_handlers(app)
        ```
    """
    
    @app.exception_handler(APIError)
    async def api_error_handler(request: Request, exc: APIError) -> JSONResponse:
        """Handle custom API errors."""
        # Get correlation ID from request state if available
        correlation_id = getattr(request.state, "correlation_id", None)
        
        # Log the error
        logger.error(
            f"API Error: {exc.detail} "
            f"(status_code: {exc.status_code}, code: {exc.code}, "
            f"correlation_id: {correlation_id})"
        )
        
        # Return JSON response
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": {
                    "code": exc.code,
                    "message": exc.detail,
                    "correlation_id": correlation_id,
                }
            },
            headers=exc.headers,
        )
    
    @app.exception_handler(RequestValidationError)
    async def validation_error_handler(
        request: Request, exc: RequestValidationError
    ) -> ValidationErrorResponse:
        """Handle request validation errors."""
        # Get correlation ID from request state if available
        correlation_id = getattr(request.state, "correlation_id", None)
        
        # Format validation errors
        errors = []
        for error in exc.errors():
            error_detail = {
                "loc": error.get("loc", []),
                "msg": error.get("msg", ""),
                "type": error.get("type", ""),
            }
            errors.append(error_detail)
        
        # Log the error
        logger.error(
            f"Validation Error: {errors} "
            f"(correlation_id: {correlation_id})"
        )
        
        # Return JSON response
        return ValidationErrorResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "error": {
                    "code": "validation_error",
                    "message": "Validation error",
                    "errors": errors,
                    "correlation_id": correlation_id,
                }
            },
        )
    
    @app.exception_handler(ValidationError)
    async def pydantic_validation_error_handler(
        request: Request, exc: ValidationError
    ) -> ValidationErrorResponse:
        """Handle Pydantic validation errors."""
        # Get correlation ID from request state if available
        correlation_id = getattr(request.state, "correlation_id", None)
        
        # Format validation errors
        errors = []
        for error in exc.errors():
            error_detail = {
                "loc": error.get("loc", []),
                "msg": error.get("msg", ""),
                "type": error.get("type", ""),
            }
            errors.append(error_detail)
        
        # Log the error
        logger.error(
            f"Pydantic Validation Error: {errors} "
            f"(correlation_id: {correlation_id})"
        )
        
        # Return JSON response
        return ValidationErrorResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "error": {
                    "code": "validation_error",
                    "message": "Validation error",
                    "errors": errors,
                    "correlation_id": correlation_id,
                }
            },
        )
    
    @app.exception_handler(IntegrityError)
    async def integrity_error_handler(
        request: Request, exc: IntegrityError
    ) -> JSONResponse:
        """Handle database integrity errors."""
        # Get correlation ID from request state if available
        correlation_id = getattr(request.state, "correlation_id", None)
        
        # Log the error
        logger.error(
            f"Database Integrity Error: {str(exc)} "
            f"(correlation_id: {correlation_id})"
        )
        
        # Return JSON response
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={
                "error": {
                    "code": "database_integrity_error",
                    "message": "Database integrity error",
                    "detail": str(exc),
                    "correlation_id": correlation_id,
                }
            },
        )
    
    @app.exception_handler(SQLAlchemyError)
    async def sqlalchemy_error_handler(
        request: Request, exc: SQLAlchemyError
    ) -> JSONResponse:
        """Handle SQLAlchemy errors."""
        # Get correlation ID from request state if available
        correlation_id = getattr(request.state, "correlation_id", None)
        
        # Log the error
        logger.error(
            f"Database Error: {str(exc)} "
            f"(correlation_id: {correlation_id})"
        )
        
        # Return JSON response
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": {
                    "code": "database_error",
                    "message": "Database error",
                    "correlation_id": correlation_id,
                }
            },
        )
    
    @app.exception_handler(Exception)
    async def general_exception_handler(
        request: Request, exc: Exception
    ) -> JSONResponse:
        """Handle all other exceptions."""
        # Get correlation ID from request state if available
        correlation_id = getattr(request.state, "correlation_id", None)
        
        # Log the error
        logger.exception(
            f"Unhandled Exception: {str(exc)} "
            f"(correlation_id: {correlation_id})"
        )
        
        # Return JSON response
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error": {
                    "code": "internal_server_error",
                    "message": "Internal server error",
                    "correlation_id": correlation_id,
                }
            },
        )