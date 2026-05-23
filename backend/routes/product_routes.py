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

@product_bp.route('/products', methods=['GET'])
def get_products():

    products = Product.query.all()

    product_list = []

    for product in products:

        product_data = {
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "quantity": product.quantity,
            "image_url": product.image_url,
            "producer_id": product.producer_id
        }

        product_list.append(product_data)

    return jsonify(product_list), 200

@product_bp.route('/products/<int:product_id>', methods=['PUT'])
@jwt_required()
def update_product(product_id):

    current_user_id = int(get_jwt_identity())

    product = Product.query.get(product_id)

    if not product:
        return jsonify({
            "message": "Product not found"
        }), 404

    if product.producer_id != current_user_id:
        return jsonify({
            "message": "Unauthorized"
        }), 403

    data = request.get_json()

    product.name = data.get('name', product.name)
    product.description = data.get('description', product.description)
    product.price = data.get('price', product.price)
    product.quantity = data.get('quantity', product.quantity)
    product.image_url = data.get('image_url', product.image_url)

    db.session.commit()

    return jsonify({
        "message": "Product updated successfully"
    }), 200