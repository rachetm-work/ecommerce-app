from src.framework.utils import call_api


class TestProductAPI:
    def test_create_product(self, client):
        response = call_api(
            client.post,
            "/products",
            json={
                "name": "Test Product",
                "description": "Test Description",
                "price": 99.99,
                "stock": 10
            }
        )

        assert response.status_code == 200
        res = response.json()
        assert res['success'] is True
        assert res['data'][0]['name'] == "Test Product"
        assert res['data'][0]['price'] == 99.99

    def test_get_products(self, client, sample_product):
        response = call_api(client.get, "/products")
        assert response.status_code == 200
        res = response.json()
        assert res['success'] is True
        data = res['data']
        assert len(data) == 1
        assert data[0]["id"] == sample_product.id


class TestOrderAPI:
    def test_create_order_success(self, client, sample_product):
        response = call_api(
            client.post,
            "/orders",
            json={
                "products": [
                    {"product_id": sample_product.id, "quantity": 2}
                ]
            }
        )
        assert response.status_code == 200
        res = response.json()
        assert res['success'] is True
        data = res['data'][0]
        assert data["status"] == "Pending"
        assert data["total_price"] == 199.98
        assert len(data["items"]) == 1

    def test_create_order_insufficient_stock(self, client, sample_product):
        response = call_api(
            client.post,
            "/orders",
            json={
                "products": [
                    {"product_id": sample_product.id, "quantity": 20}
                ]
            }
        )
        assert response.status_code == 400

    def test_create_order_product_not_found(self, client):
        response = call_api(
            client.post,
            "/orders",
            json={
                "products": [
                    {"product_id": 999, "quantity": 1}
                ]
            }
        )
        assert response.status_code == 400
        res = response.json()
        assert res['success'] is False

    def test_create_order_updates_stock(self, client, sample_product):
        initial_stock = sample_product.stock

        response = call_api(
            client.post,
            "/orders",
            json={
                "products": [
                    {"product_id": sample_product.id, "quantity": 3}
                ]
            }
        )
        assert response.status_code == 200

        # Check updated stock
        response = call_api(client.get, f"/products")
        assert response.status_code == 200
        res = response.json()
        data = res["data"]
        updated_product = next(p for p in data if p["id"] == sample_product.id)
        assert updated_product["stock"] == initial_stock - 3
