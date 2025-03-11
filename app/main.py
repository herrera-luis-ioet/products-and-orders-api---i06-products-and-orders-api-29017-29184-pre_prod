"""
Main FastAPI application.

This module sets up the FastAPI application with middleware,
exception handlers, and API router registration.
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from app import __app_name__, __version__
from app.config import settings
from app.database import init_db
from app.api.v1.api import api_router
from app.errors import OrderValidationError, ProductValidationError, setup_exception_handlers

# Configure logging
logging.basicConfig(
    level=logging.INFO if not settings.DEBUG else logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__app_name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for FastAPI application.
    
    Handles startup and shutdown events.
    """
    # Startup
    logger.info("Starting up application...")
    await init_db()
    logger.info("Database initialized")
    
    yield
    
    # Shutdown
    logger.info("Shutting down application...")


# Create FastAPI application
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API for managing products and orders",
    version=__version__,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Exception handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors in requests."""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors(), "body": exc.body},
    )

@app.exception_handler(OrderValidationError)
async def order_validation_error_handler(request: Request, exc: OrderValidationError):
    """Handle order validation errors."""
    # Get correlation ID from request state if available
    correlation_id = getattr(request.state, "correlation_id", None)
    
    # Log the error
    logger.error(
        f"Order Validation Error: {exc.detail} "
        f"(code: {exc.code}, error_type: {exc.error_type}, "
        f"correlation_id: {correlation_id})"
    )
    
    # Create error response
    error_response = {
        "code": exc.code,
        "message": exc.detail,
        "correlation_id": correlation_id,
        "product_ids": exc.product_ids,
        "error_type": exc.error_type,
        "validation_errors": exc.validation_errors
    }
    
    # Return JSON response
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": jsonable_encoder(error_response)},
        headers=exc.headers,
    )

@app.exception_handler(ProductValidationError)
async def product_validation_error_handler(request: Request, exc: ProductValidationError):
    """Handle product validation errors."""
    # Get correlation ID from request state if available
    correlation_id = getattr(request.state, "correlation_id", None)
    
    # Log the error
    logger.error(
        f"Product Validation Error: {exc.detail} "
        f"(code: {exc.code}, error_type: {exc.error_type}, "
        f"correlation_id: {correlation_id})"
    )
    
    # Create error response
    error_response = {
        "code": exc.code,
        "message": exc.detail,
        "correlation_id": correlation_id,
        "product_ids": exc.product_ids,
        "error_type": exc.error_type,
        "validation_errors": exc.validation_errors
    }
    
    # Return JSON response
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": jsonable_encoder(error_response)},
        headers=exc.headers,
    )


# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    """
    Health check endpoint.
    
    Returns:
        dict: Status information about the API
    """
    return {
        "status": "healthy",
        "version": __version__,
        "name": __app_name__,
        "environment": settings.ENV,
    }


# Set up all exception handlers from app.errors
setup_exception_handlers(app)

# Include API router
app.include_router(
    api_router,
    prefix=settings.API_V1_STR,
)


@app.get("/", tags=["Root"])
async def root():
    """
    Root endpoint.
    
    Returns:
        dict: Basic information about the API
    """
    return {
        "message": "Welcome to the Product and Order Management API",
        "docs_url": "/docs",
        "version": __version__,
    }
