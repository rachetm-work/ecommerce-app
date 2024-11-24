from sqlalchemy import Column, Integer, String, Float

from app.framework.models import BaseModel
from app.products.schemas import ProductSchema


class Product(BaseModel):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    price = Column(Float)
    stock = Column(Integer)

    _schema = ProductSchema
