# ============================================================
# 🛒 CHECKOUT ROUTES (FINAL PRODUCTION READY)
# ============================================================

from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
import requests

from ..extensions import db
from ..models.cart_item import CartItem
from ..models.order import Order
from ..models.order_item import OrderItem

checkout_bp = Blueprint("checkout", __name__)


@checkout_bp.post("/")
@jwt_required()
def checkout():
    user_id = get_jwt_identity()
    data = request.get_json() or {}

    try:
        # 1️⃣ Fetch cart items
        cart_items = CartItem.query.filter_by(user_id=user_id).all()

        if not cart_items:
            return jsonify({"error": "Cart is empty"}), 400

        # 2️⃣ Prepare payload for Product Service
        payload = {
            "items": [
                {
                    "product_id": c.product_id,
                    "variant_id": c.variant_id,
                    "quantity": c.quantity
                }
                for c in cart_items
            ]
        }

        # 3️⃣ Call Product Service (dynamic URL)
        resp = requests.post(
            f"{current_app.config['PRODUCT_BASE_URL']}/api/v1/products/decrease-stock",
            json=payload,
            headers={
                "Authorization": request.headers.get("Authorization")
            },
            timeout=5
        )

        if resp.status_code != 200:
            return jsonify({"error": "Insufficient stock"}), 400

        # 4️⃣ Create Order
        order = Order(
            user_id=user_id,
            total_price=sum(c.price * c.quantity for c in cart_items),
            contact=data.get("contact"),
            address=data.get("address")
        )

        db.session.add(order)
        db.session.flush()   # 🔥 IMPORTANT

        # 5️⃣ Create Order Items + Clear Cart
        for c in cart_items:
            db.session.add(OrderItem(
                order_id=order.id,
                product_id=c.product_id,
                variant_id=c.variant_id,
                quantity=c.quantity,
                price=c.price
            ))
            db.session.delete(c)

        db.session.commit()

        return jsonify({
            "order_id": order.id,
            "status": "placed"
        }), 201

    except Exception as e:
        current_app.logger.error(f"Checkout error: {str(e)}")
        return jsonify({"error": str(e)}), 500