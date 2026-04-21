from flask import Flask, Blueprint, request, jsonify
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    jwt_required,
    get_jwt_identity,
)


def create_app():
    app = Flask(__name__)

    app.config["JWT_SECRET_KEY"] = "test-secret"
    app.config["TESTING"] = True

    jwt = JWTManager(app)

    # -----------------------------
    # IN-MEMORY STORAGE
    # -----------------------------
    carts = {}        # user_id -> items
    orders = {}       # user_id -> orders
    order_counter = {"id": 1}

    # -----------------------------
    # CART SERVICES
    # -----------------------------
    def add_to_cart_service(user_id, data):
        item = {
            "product_id": data["product_id"],
            "variant_id": data["variant_id"],
            "name": data["name"],
            "color": data["color"],
            "price": data["price"],
            "quantity": data["quantity"]
        }

        carts.setdefault(user_id, []).append(item)
        return {"message": "Added to cart"}, 201

    def get_cart_service(user_id):
        return carts.get(user_id, []), 200

    # -----------------------------
    # CHECKOUT SERVICE
    # -----------------------------
    def checkout_service(user_id, data):
        cart_items = carts.get(user_id, [])

        if not cart_items:
            return {"error": "Cart is empty"}, 400

        total = sum(i["price"] * i["quantity"] for i in cart_items)

        order_id = order_counter["id"]
        order_counter["id"] += 1

        order = {
            "order_id": order_id,
            "status": "placed",
            "total_price": total,
            "contact": data.get("contact"),
            "address": data.get("address"),
            "items": cart_items.copy()
        }

        orders.setdefault(user_id, []).append(order)

        # clear cart
        carts[user_id] = []

        return {"order_id": order_id, "status": "placed"}, 201

    # -----------------------------
    # ORDER SERVICES
    # -----------------------------
    def get_orders_service(user_id):
        return orders.get(user_id, []), 200

    def get_order_details_service(user_id, order_id):
        for o in orders.get(user_id, []):
            if o["order_id"] == order_id:
                return o, 200
        return {"error": "Order not found"}, 404

    def cancel_order_service(user_id, order_id):
        for o in orders.get(user_id, []):
            if o["order_id"] == order_id:
                if o["status"] != "placed":
                    return {"error": "Cannot cancel"}, 400
                o["status"] = "cancelled"
                return {"message": "Order cancelled"}, 200
        return {"error": "Order not found"}, 404

    # -----------------------------
    # BLUEPRINTS
    # -----------------------------
    cart_bp = Blueprint("cart", __name__)
    checkout_bp = Blueprint("checkout", __name__)
    orders_bp = Blueprint("orders", __name__)

    # -----------------------------
    # CART ROUTES
    # -----------------------------
    @cart_bp.post("/")
    @jwt_required()
    def add_to_cart():
        user_id = get_jwt_identity()
        data = request.get_json() or {}
        res, status = add_to_cart_service(user_id, data)
        return jsonify(res), status

    @cart_bp.get("/")
    @jwt_required()
    def get_cart():
        user_id = get_jwt_identity()
        res, status = get_cart_service(user_id)
        return jsonify(res), status

    # -----------------------------
    # CHECKOUT ROUTE
    # -----------------------------
    @checkout_bp.post("/")
    @jwt_required()
    def checkout():
        user_id = get_jwt_identity()
        data = request.get_json() or {}
        res, status = checkout_service(user_id, data)
        return jsonify(res), status

    # -----------------------------
    # ORDER ROUTES
    # -----------------------------
    @orders_bp.get("/")
    @jwt_required()
    def get_orders():
        user_id = get_jwt_identity()
        res, status = get_orders_service(user_id)
        return jsonify(res), status

    @orders_bp.get("/<int:order_id>")
    @jwt_required()
    def get_order(order_id):
        user_id = get_jwt_identity()
        res, status = get_order_details_service(user_id, order_id)
        return jsonify(res), status

    @orders_bp.patch("/<int:order_id>/cancel")
    @jwt_required()
    def cancel_order(order_id):
        user_id = get_jwt_identity()
        res, status = cancel_order_service(user_id, order_id)
        return jsonify(res), status

    # -----------------------------
    # LOGIN (TEST)
    # -----------------------------
    @app.post("/login")
    def login():
        return jsonify({
            "access_token": create_access_token(identity="1")
        }), 200

    app.register_blueprint(cart_bp, url_prefix="/api/cart")
    app.register_blueprint(checkout_bp, url_prefix="/api/checkout")
    app.register_blueprint(orders_bp, url_prefix="/api/orders")

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)