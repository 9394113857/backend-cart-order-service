from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import requests

from app.extensions import db
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.cart_item import CartItem

checkout_bp = Blueprint("checkout", __name__)

PRODUCT_SERVICE_URL = "https://backend-product-service.onrender.com/api/v1/products/decrease-stock"
ML_EVENTS_URL = "https://backend-ml-events-service.onrender.com/api/events"


@checkout_bp.post("/")
@jwt_required()
def checkout():
    data = request.get_json()
    user_id = int(get_jwt_identity())

    cart_items = CartItem.query.filter_by(user_id=user_id).all()
    if not cart_items:
        return jsonify({"error": "Cart is empty"}), 400

    try:
        order = Order(
            user_id=user_id,
            contact=data["contact"],
            address=data["address"],
            total_price=data["total_price"]
        )
        db.session.add(order)
        db.session.flush()

        items_payload = []

        for item in cart_items:
            db.session.add(OrderItem(
                order_id=order.id,
                product_id=item.product_id,
                name=item.name,
                price=item.price,
                quantity=item.quantity,
                image=item.image
            ))

            items_payload.append({
                "product_id": item.product_id,
                "quantity": item.quantity
            })

        # 🔥 STOCK DEDUCTION
        requests.post(
            PRODUCT_SERVICE_URL,
            json={"items": items_payload},
            headers={"Authorization": request.headers.get("Authorization")}
        )

        # 🔥 ML EVENT
        requests.post(
            ML_EVENTS_URL,
            json={
                "event_type": "order_completed",
                "object_type": "order",
                "object_id": order.id,
                "metadata": {
                    "total_price": order.total_price,
                    "items": items_payload
                }
            }
        )

        CartItem.query.filter_by(user_id=user_id).delete()
        db.session.commit()

        return jsonify({
            "order_id": order.id,
            "status": order.status,
            "message": "Order placed successfully"
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Checkout failed"}), 500
