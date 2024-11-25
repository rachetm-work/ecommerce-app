from datetime import datetime

from sqlalchemy import Column, Integer, DateTime
from sqlalchemy import String, Float

from src.framework.models import BaseModel
from src.products.schemas import ProductSchema


class Product(BaseModel):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Float)
    stock = Column(Integer)

    _schema = ProductSchema
