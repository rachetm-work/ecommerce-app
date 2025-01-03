from typing import List

from fastapi import APIRouter

from src.framework.exceptions import BadRequest
from src.framework.services import BaseCrudService
from src.orders.models import Order, OrderItem
from src.orders.schemas import OrderItemSchema
from src.products.models import Product

router = APIRouter()


class OrderService(BaseCrudService):
    def __init__(self, db_session):
        super().__init__(model=Order, db_session=db_session)

    def validate_products_exist(self, product_ids: List[int]) -> None:
        """Validate all products exist in the database"""
        existing_products = self.db_session.query(Product).filter(
            Product.id.in_(product_ids)
        ).all()

        existing_ids = {p.id for p in existing_products}
        missing_ids = set(product_ids) - existing_ids

        if missing_ids:
            raise BadRequest(error_message=f"Products with ids {missing_ids} not found")

    def check_and_lock_stock(self, order_items: List[OrderItemSchema]) -> List[Product]:
        """Check and lock stock for products with FOR UPDATE"""
        products = []

        for item in order_items:
            # Lock the product row for update
            product = self.db_session.query(Product).with_for_update().filter(
                Product.id == item.product_id
            ).first()

            if not product:
                raise BadRequest(error_message=f"Product {item.product_id} not found")

            if product.stock < item.quantity:
                raise BadRequest(
                    error_message=f"Insufficient stock for product {product.id}. Requested: {item.quantity}, Available: {product.stock}"
                )

            products.append(product)

        return products

    @staticmethod
    def calculate_total_price(products: List[Product], order_items: List[OrderItemSchema]) -> float:
        """Calculate total price for the order"""
        product_map = {p.id: p for p in products}
        return sum(
            product_map[item.product_id].price * item.quantity
            for item in order_items
        )

    @staticmethod
    def update_stock(products: List[Product], order_items: List[OrderItemSchema]) -> None:
        """Update stock levels for products"""
        product_map = {p.id: p for p in products}
        for item in order_items:
            product = product_map[item.product_id]
            product.stock -= item.quantity

    def create_order(self, order_data) -> Order:
        """Create order with products"""
        try:
            # Start transaction
            self.db_session.begin_nested()

            # Validate all products exist
            product_ids = [item.product_id for item in order_data.products]
            self.validate_products_exist(product_ids)

            # Check and lock stock
            products = self.check_and_lock_stock(order_data.products)

            # Calculate total price
            total_price = self.calculate_total_price(products, order_data.products)

            # Create order
            order = Order(
                total_price=total_price,
            )
            self.db_session.add(order)

            # Create order items
            for item in order_data.products:
                order_item = OrderItem(
                    order=order,
                    product_id=item.product_id,
                    quantity=item.quantity,
                    unit_price=next(p.price for p in products if p.id == item.product_id)
                )
                self.db_session.add(order_item)

            # Update stock levels
            self.update_stock(products, order_data.products)

            self.db_session.commit()

            return order

        except Exception as e:
            # Rollback and re-raise the exception
            self.db_session.rollback()
            raise e
