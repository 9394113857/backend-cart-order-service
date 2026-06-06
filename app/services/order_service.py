from flask import jsonify, request, Response
import requests
import os
import csv
from io import StringIO

from ..extensions import db
from ..models.order import Order
from ..models.order_item import OrderItem


# ============================================================
# CONFIGURATION
# ============================================================

PRODUCT_BASE_URL = os.getenv(
    "PRODUCT_BASE_URL",
    "http://127.0.0.1:5002"
)


# ============================================================
# ORDER SERVICE
# ============================================================

class OrderService:

    # ========================================================
    # GET ALL ORDERS OF A USER
    # ========================================================
    @staticmethod
    def get_orders(user_id):

        orders = Order.query.filter_by(
            user_id=user_id
        ).all()

        return jsonify([
            {
                "order_id": order.id,
                "status": order.status,
                "total_price": order.total_price,
                "created_at": order.created_at
            }
            for order in orders
        ]), 200

    # ========================================================
    # GET SINGLE ORDER DETAILS
    # ========================================================
    @staticmethod
    def get_order_details(user_id, order_id):

        order = Order.query.filter_by(
            id=order_id,
            user_id=user_id
        ).first_or_404()

        items = OrderItem.query.filter_by(
            order_id=order.id
        ).all()

        return jsonify({
            "order_id": order.id,
            "status": order.status,
            "total_price": order.total_price,
            "created_at": order.created_at,
            "items": [
                {
                    "product_id": item.product_id,
                    "variant_id": item.variant_id,
                    "quantity": item.quantity,
                    "price": item.price
                }
                for item in items
            ]
        }), 200

    # ========================================================
    # CANCEL ORDER
    # ========================================================
    @staticmethod
    def cancel_order(user_id, order_id):

        order = Order.query.filter_by(
            id=order_id,
            user_id=user_id
        ).first_or_404()

        if order.status != "placed":
            return jsonify({
                "error": "Order cannot be cancelled"
            }), 400

        items = OrderItem.query.filter_by(
            order_id=order.id
        ).all()

        payload = {
            "items": [
                {
                    "product_id": item.product_id,
                    "variant_id": item.variant_id,
                    "quantity": item.quantity
                }
                for item in items
            ]
        }

        response = requests.post(
            f"{PRODUCT_BASE_URL}/api/v1/products/restore-stock",
            json=payload,
            headers={
                "Authorization": request.headers.get(
                    "Authorization"
                )
            }
        )

        if response.status_code != 200:
            return jsonify({
                "error": "Stock restore failed"
            }), 500

        order.status = "cancelled"
        db.session.commit()

        return jsonify({
            "message": "Order cancelled"
        }), 200

    # ========================================================
    # EXPORT ORDERS AS CSV
    # ========================================================
    @staticmethod
    def export_orders_csv(user_id):

        orders = Order.query.filter(
            Order.user_id == user_id,
            Order.status.in_([
                "placed",
                "delivered"
            ])
        ).all()  # Only export placed and delivered orders

        output = StringIO()
        writer = csv.writer(output)

        writer.writerow([
            "Order ID",
            "Status",
            "Total Price",
            "Created At",
            "Product ID",
            "Variant ID",
            "Quantity",
            "Price"
        ])

        for order in orders:

            items = OrderItem.query.filter_by(
                order_id=order.id
            ).all()

            for item in items:

                writer.writerow([
                    order.id,
                    order.status,
                    order.total_price,
                    order.created_at,
                    item.product_id,
                    item.variant_id,
                    item.quantity,
                    item.price
                ])

        return Response(
            output.getvalue(),
            mimetype="text/csv",
            headers={
                "Content-Disposition":
                "attachment; filename=orders.csv"
            }
        )
