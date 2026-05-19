from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash

from extensions import db
from models.user_model import User

auth_bp = Blueprint('auth', __name__)
@auth_bp.route('/register', methods= ['POST'])
def register():
    data = request.get_json()

    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    role = data.get('role')

    existing_user = User.query.filter_by(email = email ).first()

    if existing_user:
        return jsonify({
            "message":"Email already exists"
        }), 400
    
    hashed_password = generate_password_hash(password)

    new_user = User(
        name = name,
        email = email,
        password = hashed_password,
        role = role
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "message": "User registerd successfully"
    }), 201