from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models.order import Order
from app.models.cart_item import CartItem

checkout_bp = Blueprint("checkout", __name__)


@checkout_bp.post("/")
@jwt_required()
def checkout():
    """
    POST /api/checkout
    Place order and clear cart
    """
    data = request.get_json()
    user_id = int(get_jwt_identity())

    order = Order(
        user_id=user_id,
        contact=data["contact"],
        address=data["address"],
        total_price=data["total_price"]
    )

    db.session.add(order)

    # Clear cart after order
    CartItem.query.filter_by(user_id=user_id).delete()

    db.session.commit()

    return jsonify({"message": "Order placed successfully"}), 201
