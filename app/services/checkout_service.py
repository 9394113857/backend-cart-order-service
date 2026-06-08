from flask import jsonify, current_app, request
import requests

from ..extensions import db
from ..models.cart_item import CartItem
from ..models.order import Order
from ..models.order_item import OrderItem

from .order_event_service import OrderEventService
from .invoice_history_service import InvoiceHistoryService
from .order_analytics_service import OrderAnalyticsService


class CheckoutService:

    @staticmethod
    def checkout(user_id, data):
        try:
            cart_items = CartItem.query.filter_by(user_id=user_id).all()

            if not cart_items:
                return jsonify({"error": "Cart is empty"}), 400

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

            order = Order(
                user_id=user_id,
                total_price=sum(c.price * c.quantity for c in cart_items),
                contact=data.get("contact"),
                address=data.get("address")
            )

            db.session.add(order)
            db.session.flush()

            for c in cart_items:
                db.session.add(
                    OrderItem(
                        order_id=order.id,
                        product_id=c.product_id,
                        variant_id=c.variant_id,
                        quantity=c.quantity,
                        price=c.price
                    )
                )
                db.session.delete(c)

            db.session.commit()

            # Create order event
            OrderEventService.create_event(
                order.id,
                "ORDER_PLACED"
            )

            # Create invoice history record
            InvoiceHistoryService.create_record(
                order.id,
                "CREATED"
            )

            # Create analytics record
            OrderAnalyticsService.create_record(
                order.id,
                order.total_price,
                order.status
            )

            return jsonify({
                "order_id": order.id,
                "status": "placed"
            }), 201

        except Exception as e:
            current_app.logger.error(f"Checkout error: {str(e)}")
            return jsonify({"error": str(e)}), 500