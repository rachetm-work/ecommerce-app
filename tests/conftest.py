import os
import re
from datetime import datetime

import pytest
from dotenv import load_dotenv
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.framework.database.database import get_db
from src.framework.models import BaseModel
from src.orders.models import Order, OrderItem
from src.products.models import Product
from main import app

load_dotenv()


def get_db_url():
    url = '${DB_DRIVER}://${POSTGRES_USER}:${POSTGRES_PASSWORD}@${DB_HOST}:${DB_PORT}/${DB_NAME_FOR_TEST}'

    return re.sub(r"\${(.+?)}", lambda m: os.getenv(m.group(1)), url)


# Test database URL
SQLALCHEMY_DATABASE_URL = get_db_url()

engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, expire_on_commit=False)


@pytest.fixture(scope="function")
def db():
    BaseModel.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        BaseModel.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def sample_product(db):
    product = Product(
        name="Test Product",
        description="Test Description",
        price=99.99,
        stock=10,
        created_at=datetime.utcnow()
    )
    db.add(product)
    db.commit()
    db.refresh(product)
    return product


@pytest.fixture
def sample_order(db, sample_product):
    order = Order(
        total_price=99.99,
        status="pending",
        created_at=datetime.utcnow()
    )
    db.add(order)

    order_item = OrderItem(
        order=order,
        product_id=sample_product.id,
        quantity=1,
        unit_price=99.99
    )
    db.add(order_item)

    db.commit()
    db.refresh(order)
    return order
