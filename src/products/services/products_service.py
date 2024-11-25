from typing import List

from src.framework.services import BaseCrudService
from src.products.models import Product


class ProductService(BaseCrudService):
    def __init__(self, db_session):
        super().__init__(model=Product, db_session=db_session)

    def get_all_products(self) -> List[Product]:
        return super().get_all()

    def create_product(self, product) -> Product:
        return super().create(product)
