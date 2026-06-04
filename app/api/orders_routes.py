from flask import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_cors import CORS

from ..services.order_service import OrderService

orders_bp = Blueprint("orders", __name__)
CORS(orders_bp)  # keep as-is


# ============================================================
# GET ALL ORDERS
# ============================================================
@orders_bp.get("/")
@jwt_required()
def get_orders():
    user_id = get_jwt_identity()
    return OrderService.get_orders(user_id)


# ============================================================
# GET SINGLE ORDER
# ============================================================
@orders_bp.get("/<int:order_id>")
@jwt_required()
def get_order_details(order_id):
    user_id = get_jwt_identity()
    return OrderService.get_order_details(user_id, order_id)


# ============================================================
# CANCEL ORDER
# ============================================================
@orders_bp.patch("/<int:order_id>/cancel")
@jwt_required()
def cancel_order(order_id):
    user_id = get_jwt_identity()
    return OrderService.cancel_order(user_id, order_id)


# ============================================================
# EXPORT ORDERS CSV
# ============================================================
@orders_bp.get("/export/csv")
@jwt_required()
def export_orders_csv():
    user_id = get_jwt_identity()
    return OrderService.export_orders_csv(user_id)