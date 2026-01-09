from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.order import Order
from app.models.order_item import OrderItem
from app.extensions import db

orders_bp = Blueprint("orders", __name__)


@orders_bp.get("/")
@jwt_required()
def get_my_orders():
    """
    GET /api/orders
    Fetch all orders of logged-in user
    """
    user_id = int(get_jwt_identity())

    orders = Order.query.filter_by(user_id=user_id).order_by(
        Order.created_at.desc()
    ).all()

    return jsonify([
        {
            "order_id": o.id,
            "total_price": o.total_price,
            "status": o.status,
            "created_at": o.created_at
        }
        for o in orders
    ]), 200


@orders_bp.get("/<int:order_id>")
@jwt_required()
def get_order_details(order_id):
    """
    GET /api/orders/<order_id>
    """
    user_id = int(get_jwt_identity())

    order = Order.query.filter_by(id=order_id, user_id=user_id).first()
    if not order:
        return jsonify({"error": "Order not found"}), 404

    items = OrderItem.query.filter_by(order_id=order.id).all()

    return jsonify({
        "order_id": order.id,
        "status": order.status,
        "total_price": order.total_price,
        "items": [
            {
                "product_id": i.product_id,
                "name": i.name,
                "price": i.price,
                "quantity": i.quantity,
                "image": i.image
            }
            for i in items
        ]
    }), 200


@orders_bp.patch("/<int:order_id>/cancel")
@jwt_required()
def cancel_order(order_id):
    """
    PATCH /api/orders/<order_id>/cancel
    """
    user_id = int(get_jwt_identity())

    order = Order.query.filter_by(id=order_id, user_id=user_id).first()
    if not order:
        return jsonify({"error": "Order not found"}), 404

    if order.status != "placed":
        return jsonify({"error": "Order cannot be cancelled"}), 400

    order.status = "cancelled"
    db.session.commit()

    return jsonify({"message": "Order cancelled"}), 200
