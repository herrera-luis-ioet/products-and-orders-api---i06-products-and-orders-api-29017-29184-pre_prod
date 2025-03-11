"""
Custom middleware for FastAPI application.

This module provides middleware components for request processing,
including logging, correlation IDs, and request timing.
"""

import logging
import time
import uuid
from typing import Callable, Dict, Optional

from fastapi import FastAPI, Request, Response
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.types import ASGIApp

from app import __app_name__
from app.config import settings


logger = logging.getLogger(__app_name__)


class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """
    Middleware for logging request and response information.
    
    Logs details about incoming requests and outgoing responses,
    including method, path, status code, and processing time.
    """
    
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        """
        Process the request and log information.
        
        Args:
            request: The incoming request
            call_next: The next middleware or endpoint handler
            
        Returns:
            Response: The response from the next handler
        """
        start_time = time.time()
        
        # Get or generate correlation ID
        correlation_id = request.headers.get("X-Correlation-ID", str(uuid.uuid4()))
        request.state.correlation_id = correlation_id
        
        # Log request details
        logger.info(
            f"Request started: {request.method} {request.url.path} "
            f"(correlation_id: {correlation_id})"
        )
        
        # Process the request
        try:
            response = await call_next(request)
            
            # Calculate processing time
            process_time = time.time() - start_time
            
            # Log response details
            logger.info(
                f"Request completed: {request.method} {request.url.path} "
                f"- Status: {response.status_code} - Time: {process_time:.3f}s "
                f"(correlation_id: {correlation_id})"
            )
            
            # Add correlation ID to response headers
            response.headers["X-Correlation-ID"] = correlation_id
            response.headers["X-Process-Time"] = str(process_time)
            
            return response
            
        except Exception as e:
            # Log exception
            logger.exception(
                f"Request failed: {request.method} {request.url.path} "
                f"- Error: {str(e)} "
                f"(correlation_id: {correlation_id})"
            )
            raise


class TimingMiddleware(BaseHTTPMiddleware):
    """
    Middleware for timing request processing.
    
    Measures and adds processing time information to response headers.
    """
    
    async def dispatch(
        self, request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        """
        Process the request and add timing information.
        
        Args:
            request: The incoming request
            call_next: The next middleware or endpoint handler
            
        Returns:
            Response: The response from the next handler with timing headers
        """
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        
        response.headers["X-Process-Time"] = f"{process_time:.6f}"
        return response


# PUBLIC_INTERFACE
def setup_middlewares(app: FastAPI) -> None:
    """
    Set up all middleware for the FastAPI application.
    
    Args:
        app: The FastAPI application instance
        
    Example:
        ```python
        app = FastAPI()
        setup_middlewares(app)
        ```
    """
    # Add request logging middleware if not in testing mode
    if settings.ENV != "testing":
        app.add_middleware(RequestLoggingMiddleware)
    
    # Add timing middleware
    app.add_middleware(TimingMiddleware)