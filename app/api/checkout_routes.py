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
    data = request.get_json()
    user_id = int(get_jwt_identity())

    cart_items = CartItem.query.filter_by(user_id=user_id).all()

    if not cart_items:
        return jsonify({"message": "Cart is empty"}), 400

    # Create order
    order = Order(
        user_id=user_id,
        contact=data["contact"],
        address=data["address"],
        total_price=data["total_price"]
    )
    db.session.add(order)
    db.session.flush()  # get order.id before commit

    # Create order items
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

    # Clear cart
    CartItem.query.filter_by(user_id=user_id).delete()

    db.session.commit()

    return jsonify({
        "message": "Order placed successfully",
        "order_id": order.id
    }), 201
