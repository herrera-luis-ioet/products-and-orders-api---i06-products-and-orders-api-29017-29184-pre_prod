from typing import List, Optional, Dict, Any
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductUpdate


class CRUDProduct(CRUDBase[Product, ProductCreate, ProductUpdate]):
    """
    CRUD operations for Product model.
    
    Extends the base CRUD operations with product-specific functionality.
    """

    # PUBLIC_INTERFACE
    async def get_by_sku(self, db: AsyncSession, *, sku: str) -> Optional[Product]:
        """
        Get a product by its SKU.
        
        Args:
            db: Database session
            sku: Stock Keeping Unit of the product
            
        Returns:
            The product if found, None otherwise
        """
        query = select(self.model).where(self.model.sku == sku)
        result = await db.execute(query)
        return result.scalars().first()

    # PUBLIC_INTERFACE
    async def get_by_category(
        self, db: AsyncSession, *, category: str, skip: int = 0, limit: int = 100
    ) -> List[Product]:
        """
        Get products by category with pagination.
        
        Args:
            db: Database session
            category: Category to filter by
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of products in the specified category
        """
        query = (
            select(self.model)
            .where(self.model.category == category)
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(query)
        return result.scalars().all()

    # PUBLIC_INTERFACE
    async def get_active(
        self, db: AsyncSession, *, skip: int = 0, limit: int = 100
    ) -> List[Product]:
        """
        Get active products with pagination.
        
        Args:
            db: Database session
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of active products
        """
        query = (
            select(self.model)
            .where(self.model.is_active == True)
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(query)
        return result.scalars().all()

    # PUBLIC_INTERFACE
    async def update_inventory(
        self, db: AsyncSession, *, id: int, quantity_change: int
    ) -> Optional[Product]:
        """
        Update product inventory count.
        
        Args:
            db: Database session
            id: Product ID
            quantity_change: Amount to change inventory by (positive or negative)
            
        Returns:
            Updated product if found, None otherwise
        """
        product = await self.get(db=db, id=id)
        if not product:
            return None
            
        # Ensure inventory doesn't go below zero
        new_count = max(0, product.inventory_count + quantity_change)
        product.inventory_count = new_count
        
        db.add(product)
        await db.commit()
        await db.refresh(product)
        return product

    # PUBLIC_INTERFACE
    async def search_products(
        self, db: AsyncSession, *, query: str, skip: int = 0, limit: int = 100
    ) -> List[Product]:
        """
        Search products by name or description.
        
        Args:
            db: Database session
            query: Search query string
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of products matching the search query
        """
        search_pattern = f"%{query}%"
        query = (
            select(self.model)
            .where(
                (func.lower(self.model.name).like(func.lower(search_pattern))) |
                (func.lower(self.model.description).like(func.lower(search_pattern)))
            )
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(query)
        return result.scalars().all()

    # PUBLIC_INTERFACE
    async def remove(self, db: AsyncSession, *, id: int) -> Optional[Product]:
        """
        Remove a product by ID.
        
        Args:
            db: Database session
            id: Product ID
            
        Returns:
            The removed product if found, None otherwise
        """
        return await self.delete(db, id=id)


# Create an instance of the CRUD class for products
product = CRUDProduct(Product)
