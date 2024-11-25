from datetime import datetime

from sqlalchemy import Column, Integer, String, Numeric, Enum, DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from app.framework.models import BaseModel
from app.orders.enums import OrderStatus
from app.orders.schemas import OrderSchema, OrderItemResponseSchema


class OrderItem(BaseModel):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False, index=True)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Numeric(10, 2), nullable=False)

    order = relationship("Order", back_populates="items")
    product = relationship("Product")

    _schema = OrderItemResponseSchema


class Order(BaseModel):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    total_price = Column(Numeric(10, 2), nullable=False)
    status = Column(String, Enum(OrderStatus), default=OrderStatus.Pending.value, nullable=False)

    items = relationship("OrderItem", back_populates="order")

    _schema = OrderSchema
