from app.crud.product import product
from app.crud.order import order, order_item

# Export the CRUD instances
__all__ = ["product", "order", "order_item"]