from typing import List, Optional, Dict, Any, Tuple
from decimal import Decimal
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.crud.base import CRUDBase
from app.models.order import Order, OrderItem, OrderStatus
from app.schemas.order import OrderCreate, OrderUpdate, OrderItemCreate
from app.crud.product import product as product_crud


class CRUDOrderItem(CRUDBase[OrderItem, OrderItemCreate, Dict[str, Any]]):
    """
    CRUD operations for OrderItem model.
    
    Extends the base CRUD operations with order item-specific functionality.
    """
    
    # PUBLIC_INTERFACE
    async def create_with_order(
        self, db: AsyncSession, *, obj_in: OrderItemCreate, order_id: int
    ) -> OrderItem:
        """
        Create a new order item associated with an order.
        
        Args:
            db: Database session
            obj_in: Input data for creating the order item
            order_id: ID of the order to associate with
            
        Returns:
            The created order item
        """
        # Get the product to get its current price
        product_obj = await product_crud.get(db=db, id=obj_in.product_id)
        
        # Use the product's current price if not specified
        unit_price = obj_in.unit_price if obj_in.unit_price else product_obj.price
        
        # Calculate subtotal
        subtotal = unit_price * Decimal(obj_in.quantity)
        
        # Create order item
        db_obj = OrderItem(
            order_id=order_id,
            product_id=obj_in.product_id,
            quantity=obj_in.quantity,
            unit_price=unit_price,
            subtotal=subtotal
        )
        
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        
        # Update product inventory
        await product_crud.update_inventory(
            db=db, id=obj_in.product_id, quantity_change=-obj_in.quantity
        )
        
        return db_obj


class CRUDOrder(CRUDBase[Order, OrderCreate, OrderUpdate]):
    """
    CRUD operations for Order model.
    
    Extends the base CRUD operations with order-specific functionality.
    """

    # PUBLIC_INTERFACE
    async def get_with_items(self, db: AsyncSession, id: int) -> Optional[Order]:
        """
        Get an order by ID including its items.
        
        Args:
            db: Database session
            id: Order ID
            
        Returns:
            The order with items if found, None otherwise
        """
        query = (
            select(self.model)
            .options(selectinload(self.model.items))
            .where(self.model.id == id)
        )
        result = await db.execute(query)
        return result.scalars().first()

    # PUBLIC_INTERFACE
    async def get_by_customer_email(
        self, db: AsyncSession, *, email: str, skip: int = 0, limit: int = 100
    ) -> List[Order]:
        """
        Get orders by customer email with pagination.
        
        Args:
            db: Database session
            email: Customer email to filter by
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of orders for the specified customer
        """
        query = (
            select(self.model)
            .where(self.model.customer_email == email)
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(query)
        return result.scalars().all()

    # PUBLIC_INTERFACE
    async def get_by_status(
        self, db: AsyncSession, *, status: OrderStatus, skip: int = 0, limit: int = 100
    ) -> List[Order]:
        """
        Get orders by status with pagination.
        
        Args:
            db: Database session
            status: Order status to filter by
            skip: Number of records to skip
            limit: Maximum number of records to return
            
        Returns:
            List of orders with the specified status
        """
        query = (
            select(self.model)
            .where(self.model.status == status)
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(query)
        return result.scalars().all()

    # PUBLIC_INTERFACE
    async def create_with_items(
        self, db: AsyncSession, *, obj_in: OrderCreate
    ) -> Order:
        """
        Create a new order with its items.
        
        Args:
            db: Database session
            obj_in: Input data for creating the order and its items
            
        Returns:
            The created order
        """
        # Create order without items first
        order_data = obj_in.model_dump(exclude={"items"})
        
        # Set initial status to pending if not provided
        if "status" not in order_data:
            order_data["status"] = OrderStatus.PENDING
            
        # Calculate total amount from items
        total_amount = Decimal(0)
        for item in obj_in.items:
            product_obj = await product_crud.get(db=db, id=item.product_id)
            if not product_obj:
                raise ValueError(f"Product with ID {item.product_id} not found")
                
            # Use the product's current price if not specified
            unit_price = item.unit_price if item.unit_price else product_obj.price
            item_total = unit_price * Decimal(item.quantity)
            total_amount += item_total
            
        # Create the order
        db_obj = Order(**order_data, total_amount=total_amount)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        
        # Create order items
        order_item_crud = CRUDOrderItem(OrderItem)
        for item in obj_in.items:
            await order_item_crud.create_with_order(
                db=db, obj_in=item, order_id=db_obj.id
            )
            
        # Refresh order to include items
        await db.refresh(db_obj)
        return db_obj

    # PUBLIC_INTERFACE
    async def update_status(
        self, db: AsyncSession, *, id: int, status: OrderStatus
    ) -> Optional[Order]:
        """
        Update the status of an order.
        
        Args:
            db: Database session
            id: Order ID
            status: New order status
            
        Returns:
            The updated order if found, None otherwise
        """
        order = await self.get(db=db, id=id)
        if not order:
            return None
            
        order.status = status
        db.add(order)
        await db.commit()
        await db.refresh(order)
        return order


# Create instances of the CRUD classes
order = CRUDOrder(Order)
order_item = CRUDOrderItem(OrderItem)