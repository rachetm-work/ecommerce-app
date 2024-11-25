import pytest

from app.framework.exceptions import BadRequest
from app.orders.schemas import OrderItemSchema
from app.orders.services import OrderService
from app.products.models import Product


class TestProductModel:
    def test_product_creation(self, db):
        product = Product(
            name="Test Product",
            description="Test Description",
            price=99.99,
            stock=10
        )
        db.add(product)
        db.commit()

        assert product.id is not None
        assert product.name == "Test Product"
        assert product.price == 99.99
        assert product.stock == 10

    def test_product_price_decimal_places(self, db):
        product = Product(
            name="Test Product",
            description="Test Description",
            price=99.999,
            stock=10
        )
        db.add(product)
        db.commit()

        assert float(product.price) == 99.999


class TestOrderService:
    def test_validate_products_exist(self, db, sample_product):
        service = OrderService(db)
        # Should not raise exception
        service.validate_products_exist([sample_product.id])

        with pytest.raises(BadRequest) as exc:
            service.validate_products_exist([999])
        assert exc.value.status == 400

    def test_check_and_lock_stock(self, db, sample_product):
        service = OrderService(db)
        items = [OrderItemSchema(product_id=sample_product.id, quantity=5)]

        products = service.check_and_lock_stock(items)
        assert len(products) == 1
        assert products[0].id == sample_product.id

        # Test insufficient stock
        items = [OrderItemSchema(product_id=sample_product.id, quantity=20)]
        with pytest.raises(BadRequest):
            service.check_and_lock_stock(items)

    def test_calculate_total_price(self, db, sample_product):
        service = OrderService(db)
        items = [OrderItemSchema(product_id=sample_product.id, quantity=2)]
        products = [sample_product]

        total = service.calculate_total_price(products, items)
        assert total == 199.98  # 99.99 * 2

    def test_update_stock(self, db, sample_product):
        service = OrderService(db)
        items = [OrderItemSchema(product_id=sample_product.id, quantity=3)]
        products = [sample_product]

        initial_stock = sample_product.stock
        service.update_stock(products, items)
        db.commit()

        updated_product = db.get(Product, sample_product.id)
        assert updated_product.stock == initial_stock - 3
