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
    - Create order
    - Create order items
    - Clear cart
    """
    data = request.get_json() or {}
    user_id = int(get_jwt_identity())

    contact = data.get("contact")
    address = data.get("address")
    total_price = data.get("total_price")

    if not contact or not address or not total_price:
        return jsonify({"message": "Invalid checkout data"}), 400

    cart_items = CartItem.query.filter_by(user_id=user_id).all()
    if not cart_items:
        return jsonify({"message": "Cart is empty"}), 400

    try:
        # ----------------------------
        # Create Order
        # ----------------------------
        order = Order(
            user_id=user_id,
            contact=contact,
            address=address,
            total_price=total_price,
            status="placed"
        )
        db.session.add(order)
        db.session.flush()  # get order.id

        # ----------------------------
        # Create Order Items
        # ----------------------------
        for item in cart_items:
            order_item = OrderItem(
                order_id=order.id,
                product_id=item.product_id,
                name=item.name,
                price=item.price,
                quantity=item.quantity,
                image=item.image
            )
            db.session.add(order_item)

        # ----------------------------
        # Clear Cart
        # ----------------------------
        CartItem.query.filter_by(user_id=user_id).delete()

        db.session.commit()

        return jsonify({
            "message": "Order placed successfully",
            "order_id": order.id
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({
            "message": "Checkout failed",
            "error": str(e)
        }), 500
