from flask import Flask, jsonify
from flask_cors import CORS
from .extensions import db, migrate, jwt
from .api.cart_routes import cart_bp
from .api.checkout_routes import checkout_bp
from .api.orders_routes import orders_bp
from .config import Config


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app, resources={r"/api/*": {"origins": "*"}})

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    app.register_blueprint(cart_bp, url_prefix="/api/cart")
    app.register_blueprint(checkout_bp, url_prefix="/api/checkout")
    app.register_blueprint(orders_bp, url_prefix="/api/orders")

    @app.get("/")
    def health():
        return jsonify({"status": "Cart-Order-Service UP"}), 200

    return app
