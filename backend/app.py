from flask import Flask
from flask_cors import CORS
from routes.auth_routes import auth_bp

from config import Config
from extensions import db, jwt
from models.user_model import User
from models.product_model import Product

app = Flask(__name__)

app.config.from_object(Config)

db.init_app(app)
jwt.init_app(app)

CORS(app)
app.register_blueprint(auth_bp)

@app.route('/')
def home():
    return {"message": "FreshConnect API Running"}

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)