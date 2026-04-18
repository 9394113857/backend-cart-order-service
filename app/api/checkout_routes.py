from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..services.checkout_service import CheckoutService

checkout_bp = Blueprint("checkout", __name__)


# ============================================================
# CHECKOUT
# ============================================================
@checkout_bp.post("/")
@jwt_required()
def checkout():
    user_id = get_jwt_identity()
    data = request.get_json() or {}
    return CheckoutService.checkout(user_id, data)