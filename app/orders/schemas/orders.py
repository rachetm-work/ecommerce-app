from datetime import datetime
from typing import List

from pydantic import BaseModel, conint

from app.orders.enums import OrderStatus


class OrderItemSchema(BaseModel):
    product_id: int
    quantity: conint(gt=0)  # Ensure quantity is positive


class OrderCreateSchema(BaseModel):
    products: List[OrderItemSchema]


class OrderItemResponseSchema(OrderItemSchema):
    unit_price: float

    class Config:
        from_attributes = True


class OrderSchema(BaseModel):
    id: int
    total_price: float
    status: OrderStatus
    created_at: datetime
    items: List[OrderItemResponseSchema]

    class Config:
        from_attributes = True
