import pytest
from cart_full_app_layered_debug import create_app


@pytest.fixture
def client():
    app = create_app()
    return app.test_client()


def get_token(client):
    return client.post("/login").get_json()["access_token"]


def test_full_flow(client):
    token = get_token(client)

    headers = {"Authorization": f"Bearer {token}"}

    # ADD TO CART
    res = client.post("/api/cart/", headers=headers, json={
        "product_id": 1,
        "variant_id": 1,
        "name": "Shirt",
        "color": "Red",
        "price": 500,
        "quantity": 2
    })
    assert res.status_code == 201

    # GET CART
    res = client.get("/api/cart/", headers=headers)
    assert res.status_code == 200

    # CHECKOUT
    res = client.post("/api/checkout/", headers=headers, json={
        "contact": "9999999999",
        "address": "Test Address"
    })
    assert res.status_code == 201

    order_id = res.get_json()["order_id"]

    # GET ORDERS
    res = client.get("/api/orders/", headers=headers)
    assert res.status_code == 200

    # GET ORDER DETAILS
    res = client.get(f"/api/orders/{order_id}", headers=headers)
    assert res.status_code == 200

    # CANCEL ORDER
    res = client.patch(f"/api/orders/{order_id}/cancel", headers=headers)
    assert res.status_code == 200