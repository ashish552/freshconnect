from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from extensions import db
from models.product_model import Product

product_bp = Blueprint('products', __name__)

@product_bp.route('/products', methods=['POST'])
@jwt_required()
def add_product():

    current_user_id = get_jwt_identity()

    data = request.get_json()

    name = data.get('name')
    description = data.get('description')
    price = data.get('price')
    quantity = data.get('quantity')
    image_url = data.get('image_url')

    new_product = Product(
        name=name,
        description=description,
        price=price,
        quantity=quantity,
        image_url=image_url,
        producer_id=current_user_id
    )

    db.session.add(new_product)
    db.session.commit()

    return jsonify({
        "message": "Product added successfully"
    }), 201