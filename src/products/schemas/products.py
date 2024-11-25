from pydantic import BaseModel, ConfigDict


class ProductBaseSchema(BaseModel):
    name: str
    description: str
    price: float
    stock: int


class ProductCreateSchema(ProductBaseSchema):
    pass


class ProductSchema(ProductBaseSchema):
    id: int

    model_config = ConfigDict(from_attributes=True)
