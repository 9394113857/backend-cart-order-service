from flask import Flask, jsonify
from flask_cors import CORS

from .extensions import db, migrate, jwt
from .api.cart_routes import cart_bp
from .api.checkout_routes import checkout_bp
from .config import Config


def create_app():
    """
    Cart + Checkout Service Factory
    Port: 5003
    """

    app = Flask(__name__)
    app.config.from_object(Config)

    # ------------------------------------
    # CORS (Angular / Netlify / Local)
    # ------------------------------------
    CORS(
        app,
        resources={r"/api/*": {"origins": "*"}},
        supports_credentials=True
    )

    # ------------------------------------
    # Extensions
    # ------------------------------------
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # ------------------------------------
    # Blueprints
    # ------------------------------------
    app.register_blueprint(cart_bp, url_prefix="/api/cart")
    app.register_blueprint(checkout_bp, url_prefix="/api/checkout")

    # ------------------------------------
    # Health Check (VERY IMPORTANT)
    # ------------------------------------
    @app.get("/")
    def health():
        return jsonify({"status": "cart-order-service UP"}), 200

    return app
