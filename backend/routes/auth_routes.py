from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity


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
@auth_bp.route('/login', methods = ['POST'])
def login():
    data = request.get_json()

    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email = email).first()

    if not user:
        return jsonify({
            "message":"Invalid email or password"
        }), 401
    if not check_password_hash(user.password, password):
        return jsonify({
            "message":"Not valid id or password"
        }), 401
    
    access_token = create_access_token(identity=str(user.id))

    return jsonify({
        "message": "Login successful",
        "token": access_token,
        "user": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role 
        }
    }),200

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def profile():

    current_user = get_jwt_identity()

    return jsonify({
        "message": "Protected profile route",
        "user_id": current_user
    }), 200
    