from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from ..services.cart_service import CartService

cart_bp = Blueprint("cart", __name__)


# ============================================================
# ADD TO CART
# ============================================================
@cart_bp.post("/")
@jwt_required()
def add_to_cart():
    user_id = get_jwt_identity()
    data = request.get_json() or {}
    return CartService.add_to_cart(user_id, data)


# ============================================================
# GET CART
# ============================================================
@cart_bp.get("/")
@jwt_required()
def get_cart():
    user_id = get_jwt_identity()
    return CartService.get_cart(user_id)