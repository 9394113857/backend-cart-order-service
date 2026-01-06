from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models.cart_item import CartItem

cart_bp = Blueprint('cart', __name__)

@cart_bp.post('/')
@jwt_required()
def add_to_cart():
    data = request.get_json()
    user_id = get_jwt_identity()

    item = CartItem(
        user_id=user_id,
        product_id=data['productId'],
        name=data['name'],
        price=data['price'],
        quantity=data['quantity'],
        image=data.get('image')
    )
    db.session.add(item)
    db.session.commit()
    return jsonify({'message': 'Added to cart'}), 201

@cart_bp.get('/')
@jwt_required()
def get_cart():
    user_id = get_jwt_identity()
    items = CartItem.query.filter_by(user_id=user_id).all()
    return jsonify([item.__dict__ for item in items]), 200

@cart_bp.delete('/<int:id>')
@jwt_required()
def delete_cart_item(id):
    CartItem.query.filter_by(id=id).delete()
    db.session.commit()
    return jsonify({'message': 'Item removed'}), 200
