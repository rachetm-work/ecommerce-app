from pydantic import BaseModel


class ProductBaseSchema(BaseModel):
    name: str
    description: str
    price: float
    stock: int


class ProductCreateSchema(ProductBaseSchema):
    pass


class ProductSchema(ProductBaseSchema):
    id: int

    class Config:
        from_attributes = True
