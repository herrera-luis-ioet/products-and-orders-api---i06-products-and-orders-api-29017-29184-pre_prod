"""
Main API router for version 1.

This module combines all endpoint routers for version 1 of the API.
"""

from fastapi import APIRouter

from app.api.v1.endpoints import products, orders

# Create the main API router for v1
api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(products.router, prefix="/products", tags=["Products"])
api_router.include_router(orders.router, prefix="/orders", tags=["Orders"])