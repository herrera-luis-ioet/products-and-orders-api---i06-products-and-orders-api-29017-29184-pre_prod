"""
Order models.

This module provides the Order and OrderItem models for storing order information.
"""

from decimal import Decimal
from enum import Enum
from typing import List, Optional

from sqlalchemy import (
    String, Numeric, Integer, Text, ForeignKey, 
    CheckConstraint, Index, Enum as SQLAEnum
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import BaseModel


class OrderStatus(str, Enum):
    """Enum for order status."""
    PENDING = "pending"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"


class Order(BaseModel):
    """
    Order model for storing order information.
    
    Attributes:
        status: The current status of the order
        total_amount: The total amount of the order
        customer_name: The name of the customer
        customer_email: The email of the customer
        customer_phone: The phone number of the customer
        shipping_address: The shipping address
        billing_address: The billing address
        payment_method: The payment method used
        payment_id: The payment ID from the payment gateway
        notes: Additional notes for the order
        items: Relationship to order items
    """
    __tablename__ = "orders"
    
    # Required fields
    status: Mapped[OrderStatus] = mapped_column(
        SQLAEnum(OrderStatus),
        nullable=False,
        default=OrderStatus.PENDING,
        index=True,
        comment="Current status of the order"
    )
    total_amount: Mapped[Decimal] = mapped_column(
        Numeric(precision=10, scale=2),
        nullable=False,
        default=0.0,
        comment="Total order amount in USD"
    )
    customer_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        comment="Customer's full name"
    )
    customer_email: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True,
        comment="Customer's email address"
    )
    
    # Optional fields
    customer_phone: Mapped[Optional[str]] = mapped_column(
        String(20),
        nullable=True,
        comment="Customer's phone number"
    )
    shipping_address: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        comment="Shipping address"
    )
    billing_address: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        comment="Billing address"
    )
    payment_method: Mapped[Optional[str]] = mapped_column(
        String(50),
        nullable=True,
        comment="Payment method used"
    )
    payment_id: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True,
        comment="Payment ID from payment gateway"
    )
    notes: Mapped[Optional[str]] = mapped_column(
        Text,
        nullable=True,
        comment="Additional notes for the order"
    )
    
    # Relationships
    items: Mapped[List["OrderItem"]] = relationship(
        back_populates="order",
        cascade="all, delete-orphan"
    )
    
    # Constraints
    __table_args__ = (
        CheckConstraint("total_amount >= 0", name="check_total_amount_positive"),
        Index("ix_orders_customer_email_status", "customer_email", "status"),
    )
    
    def __repr__(self) -> str:
        return f"<Order(id={self.id}, status='{self.status}', total_amount={self.total_amount})>"


class OrderItem(BaseModel):
    """
    OrderItem model for storing order item information.
    
    This model represents the many-to-many relationship between orders and products.
    
    Attributes:
        order_id: The ID of the order
        product_id: The ID of the product
        quantity: The quantity of the product
        unit_price: The unit price of the product at the time of order
        subtotal: The subtotal for this item (quantity * unit_price)
        order: Relationship to the order
        product: Relationship to the product
    """
    __tablename__ = "order_items"
    
    # Foreign keys
    order_id: Mapped[int] = mapped_column(
        ForeignKey("orders.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id", ondelete="RESTRICT"),
        nullable=False,
        index=True
    )
    
    # Required fields
    quantity: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1,
        comment="Quantity of the product"
    )
    unit_price: Mapped[Decimal] = mapped_column(
        Numeric(precision=10, scale=2),
        nullable=False,
        comment="Unit price at time of order"
    )
    subtotal: Mapped[Decimal] = mapped_column(
        Numeric(precision=10, scale=2),
        nullable=False,
        comment="Subtotal for this item (quantity * unit_price)"
    )
    
    # Relationships
    order: Mapped["Order"] = relationship(back_populates="items")
    product: Mapped["Product"] = relationship(back_populates="order_items")
    
    # Constraints
    __table_args__ = (
        CheckConstraint("quantity > 0", name="check_quantity_positive"),
        CheckConstraint("unit_price >= 0", name="check_unit_price_positive"),
        CheckConstraint("subtotal >= 0", name="check_subtotal_positive"),
        Index("ix_order_items_order_id_product_id", "order_id", "product_id", unique=True),
    )
    
    def __repr__(self) -> str:
        return f"<OrderItem(order_id={self.order_id}, product_id={self.product_id}, quantity={self.quantity})>"