from flask import jsonify, request
import requests
import os

from ..extensions import db
from ..models.order import Order
from ..models.order_item import OrderItem


PRODUCT_BASE_URL = os.getenv(
    "PRODUCT_BASE_URL",
    "http://127.0.0.1:5002"
)


class OrderService:

    @staticmethod
    def get_orders(user_id):
        orders = Order.query.filter_by(user_id=user_id).all()

        return jsonify([
            {
                "order_id": o.id,
                "status": o.status,
                "total_price": o.total_price,
                "created_at": o.created_at
            }
            for o in orders
        ]), 200

    @staticmethod
    def get_order_details(user_id, order_id):
        order = Order.query.filter_by(
            id=order_id,
            user_id=user_id
        ).first_or_404()

        items = OrderItem.query.filter_by(order_id=order.id).all()

        return jsonify({
            "order_id": order.id,
            "status": order.status,
            "total_price": order.total_price,
            "created_at": order.created_at,
            "items": [
                {
                    "product_id": i.product_id,
                    "variant_id": i.variant_id,
                    "quantity": i.quantity,
                    "price": i.price
                }
                for i in items
            ]
        }), 200

    @staticmethod
    def cancel_order(user_id, order_id):
        order = Order.query.filter_by(
            id=order_id,
            user_id=user_id
        ).first_or_404()

        if order.status != "placed":
            return jsonify({"error": "Order cannot be cancelled"}), 400

        items = OrderItem.query.filter_by(order_id=order.id).all()

        payload = {
            "items": [
                {
                    "product_id": i.product_id,
                    "variant_id": i.variant_id,
                    "quantity": i.quantity
                }
                for i in items
            ]
        }

        resp = requests.post(
            f"{PRODUCT_BASE_URL}/api/v1/products/restore-stock",
            json=payload,
            headers={
                "Authorization": request.headers.get("Authorization")
            }
        )

        if resp.status_code != 200:
            return jsonify({"error": "Stock restore failed"}), 500

        order.status = "cancelled"
        db.session.commit()

        return jsonify({"message": "Order cancelled"}), 200