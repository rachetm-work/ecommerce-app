from app.framework.services.base_crud_service import BaseCrudService
from app.products.models import Product


class ProductService(BaseCrudService):
    def __init__(self, db_session):
        super().__init__(model=Product, db_session=db_session)

    def get_all_products(self):
        return super().get_all()

    def create_product(self, product):
        return super().create(product)
