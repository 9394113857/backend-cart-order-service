from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.cart_item import CartItem

checkout_bp = Blueprint("checkout", __name__)


@checkout_bp.post("/")
@jwt_required()
def checkout():
    """
    POST /api/checkout
    Create order + order items + clear cart
    """
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

        for item in cart_items:
            db.session.add(OrderItem(
                order_id=order.id,
                product_id=item.product_id,
                name=item.name,
                price=item.price,
                quantity=item.quantity,
                image=item.image
            ))

        CartItem.query.filter_by(user_id=user_id).delete()

        # TODO (orders-flow-v1):
        # Deduct product stock from Product Service

        db.session.commit()

        return jsonify({
            "order_id": order.id,
            "status": order.status,
            "message": "Order placed successfully"
        }), 201

    except Exception:
        db.session.rollback()
        return jsonify({"error": "Checkout failed"}), 500
