from typing import List, Optional, Dict, Any, Tuple
from decimal import Decimal
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import SQLAlchemyError

from app.crud.base import CRUDBase
from app.models.order import Order, OrderItem, OrderStatus
from app.schemas.order import OrderCreate, OrderUpdate, OrderItemCreate
from app.crud.product import product as product_crud
from app.errors import OrderValidationError, ProductValidationError


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
            
        Raises:
            ProductValidationError: If product validation fails
        """
        try:
            # Get the product to get its current price
            product_obj = await product_crud.get(db=db, id=obj_in.product_id)
            
            # Check if product exists
            if not product_obj:
                raise ProductValidationError(
                    detail=f"Product with ID {obj_in.product_id} not found",
                    product_ids=[obj_in.product_id],
                    error_type="product_not_found",
                    validation_errors=[{"msg": f"Product with ID {obj_in.product_id} not found"}]
                )
            
            # Check if product has sufficient inventory
            if product_obj.inventory_count < obj_in.quantity:
                raise ProductValidationError(
                    detail="Insufficient inventory",
                    product_ids=[obj_in.product_id],
                    error_type="insufficient_inventory",
                    validation_errors=[{
                        "product_id": obj_in.product_id,
                        "requested": obj_in.quantity,
                        "available": product_obj.inventory_count
                    }]
                )
            
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
            
            # Update product inventory
            updated_product = await product_crud.update_inventory(
                db=db, id=obj_in.product_id, quantity_change=-obj_in.quantity
            )
            
            if not updated_product:
                raise ProductValidationError(
                    detail=f"Failed to update inventory for product {obj_in.product_id}",
                    product_ids=[obj_in.product_id],
                    error_type="inventory_update_failed",
                    validation_errors=[{"msg": f"Failed to update inventory for product {obj_in.product_id}"}]
                )
                
            # Flush to persist changes without committing the transaction
            await db.flush()
            
            return db_obj
            
        except ProductValidationError:
            # Re-raise ProductValidationError for specific handling
            await db.rollback()
            raise
        except Exception as e:
            # Rollback transaction on any error
            await db.rollback()
            # If inventory update fails, raise a ProductValidationError
            raise ProductValidationError(
                detail=f"Error creating order item: {str(e)}",
                product_ids=[obj_in.product_id],
                error_type="inventory_update_failed",
                validation_errors=[{"msg": str(e)}]
            )


class CRUDOrder(CRUDBase[Order, OrderCreate, OrderUpdate]):
    """
    CRUD operations for Order model.
    
    Extends the base CRUD operations with order-specific functionality.
    """
    
    # PUBLIC_INTERFACE
    async def get(self, db: AsyncSession, id: int) -> Optional[Order]:
        """
        Get an order by ID.
        
        Args:
            db: Database session
            id: Order ID
            
        Returns:
            The order if found
            
        Raises:
            OrderValidationError: If order not found
        """
        order = await super().get(db=db, id=id)
        if not order:
            raise OrderValidationError(
                detail=f"Order with ID {id} not found",
                error_type="order_not_found",
                validation_errors=[{"msg": f"Order with ID {id} not found"}]
            )
        return order

    # PUBLIC_INTERFACE
    async def get_with_items(self, db: AsyncSession, id: int) -> Optional[Order]:
        """
        Get an order by ID including its items.
        
        Args:
            db: Database session
            id: Order ID
            
        Returns:
            The order with items if found
            
        Raises:
            OrderValidationError: If order not found
        """
        # First check if the order exists
        order = await super().get(db=db, id=id)
        
        if not order:
            raise OrderValidationError(
                detail=f"Order with ID {id} not found",
                error_type="order_not_found",
                validation_errors=[{"msg": f"Order with ID {id} not found"}]
            )
        
        # Refresh the order with its items to ensure it's attached to the session
        await db.refresh(order, ["items"])
            
        return order

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
            .options(selectinload(self.model.items))
            .where(self.model.customer_email == email)
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(query)
        orders = result.scalars().all()
        
        # No need to raise an exception if no orders found, just return empty list
        return orders

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
            
        Raises:
            OrderValidationError: If order validation fails
            ProductValidationError: If product validation fails
        """
        try:
            # Validate order has items
            if not obj_in.items or len(obj_in.items) == 0:
                raise OrderValidationError(
                    detail="Order must contain at least one item",
                    error_type="empty_order",
                    validation_errors=[{"msg": "Order must contain at least one item"}]
                )
                
            # Create order without items first
            order_data = obj_in.model_dump(exclude={"items"})
            
            # Set initial status to pending if not provided
            if "status" not in order_data:
                order_data["status"] = OrderStatus.PENDING
                
            # Calculate total amount from items and validate products
            total_amount = Decimal(0)
            invalid_products = []
            insufficient_inventory = []
            
            # Pre-validate all products before making any changes
            for item in obj_in.items:
                product_obj = await product_crud.get(db=db, id=item.product_id)
                
                # Check if product exists
                if not product_obj:
                    invalid_products.append(item.product_id)
                    continue
                    
                # Check if product has sufficient inventory
                if product_obj.inventory_count < item.quantity:
                    insufficient_inventory.append({
                        "product_id": item.product_id,
                        "requested": item.quantity,
                        "available": product_obj.inventory_count
                    })
                    continue
                    
                # Use the product's current price if not specified
                unit_price = item.unit_price if item.unit_price else product_obj.price
                item_total = unit_price * Decimal(item.quantity)
                total_amount += item_total
            
            # Handle validation errors
            if invalid_products:
                raise ProductValidationError(
                    detail=f"One or more products not found",
                    product_ids=invalid_products,
                    error_type="product_not_found",
                    validation_errors=[{"msg": f"Product with ID {pid} not found"} for pid in invalid_products]
                )
                
            if insufficient_inventory:
                raise ProductValidationError(
                    detail="Insufficient inventory for one or more products",
                    product_ids=[item["product_id"] for item in insufficient_inventory],
                    error_type="insufficient_inventory",
                    validation_errors=insufficient_inventory
                )
                
            # Create the order
            db_obj = Order(**order_data, total_amount=total_amount)
            db.add(db_obj)
            await db.flush()  # Flush to get the order ID but don't commit yet
            
            # Create order items
            order_item_crud = CRUDOrderItem(OrderItem)
            for item in obj_in.items:
                await order_item_crud.create_with_order(
                    db=db, obj_in=item, order_id=db_obj.id
                )
                
            # Commit the transaction after all operations are successful
            await db.commit()
            
            # Refresh the order with its items
            await db.refresh(db_obj, ["items"])
            
            return db_obj
            
        except (OrderValidationError, ProductValidationError):
            # Re-raise specific validation errors
            await db.rollback()
            raise
        except SQLAlchemyError as e:
            # Handle SQLAlchemy specific errors
            await db.rollback()
            raise OrderValidationError(
                detail=f"Database error while creating order: {str(e)}",
                error_type="database_error",
                validation_errors=[{"msg": str(e)}]
            )
        except Exception as e:
            # Handle any other unexpected errors
            await db.rollback()
            raise OrderValidationError(
                detail=f"Error creating order: {str(e)}",
                error_type="order_creation_failed",
                validation_errors=[{"msg": str(e)}]
            )

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
            
        Raises:
            OrderValidationError: If order validation fails
        """
        try:
            order = await self.get(db=db, id=id)
                
            # Validate status transition
            # For example, you might want to prevent changing from DELIVERED back to PENDING
            if order.status == OrderStatus.DELIVERED and status == OrderStatus.PENDING:
                raise OrderValidationError(
                    detail="Cannot change order status from DELIVERED to PENDING",
                    error_type="invalid_status_transition",
                    validation_errors=[{
                        "msg": "Invalid status transition",
                        "current_status": order.status.value,
                        "requested_status": status.value
                    }]
                )
                
            order.status = status
            db.add(order)
            await db.commit()
            await db.refresh(order)
            return order
            
        except OrderValidationError:
            # Re-raise OrderValidationError for specific handling
            raise
        except Exception as e:
            await db.rollback()
            raise OrderValidationError(
                detail=f"Error updating order status: {str(e)}",
                error_type="status_update_failed",
                validation_errors=[{"msg": str(e)}]
            )
        
    # PUBLIC_INTERFACE
    async def remove(self, db: AsyncSession, *, id: int) -> Order:
        """
        Remove an order.
        
        Args:
            db: Database session
            id: Order ID
            
        Returns:
            The removed order
            
        Raises:
            OrderValidationError: If order not found
        """
        try:
            order = await self.get(db=db, id=id)
            
            # Check if the order can be deleted (e.g., not already shipped)
            if order.status in [OrderStatus.SHIPPED, OrderStatus.DELIVERED]:
                raise OrderValidationError(
                    detail=f"Cannot delete order with status {order.status.value}",
                    error_type="invalid_order_deletion",
                    validation_errors=[{
                        "msg": "Cannot delete order that has been shipped or delivered",
                        "current_status": order.status.value
                    }]
                )
                
            await db.delete(order)
            await db.commit()
            return order
            
        except OrderValidationError:
            # Re-raise OrderValidationError for specific handling
            raise
        except Exception as e:
            await db.rollback()
            raise OrderValidationError(
                detail=f"Error deleting order: {str(e)}",
                error_type="deletion_failed",
                validation_errors=[{"msg": str(e)}]
            )


# Create instances of the CRUD classes
order = CRUDOrder(Order)
order_item = CRUDOrderItem(OrderItem)
