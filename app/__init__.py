import os
import json
import uuid
import logging
from logging.handlers import TimedRotatingFileHandler

from flask import Flask, jsonify, g, request
from flask_cors import CORS

from .config import Config
from .extensions import db, migrate, jwt


# =====================================================
# 🔧 BUILD INFO   
# =====================================================
def get_build_info():
    try:
        with open("build_info.json") as f:
            return json.load(f)
    except Exception as e:
        return {
            "version": "unknown",
            "commit": "unknown",
            "branch": "unknown",
            "build_time_utc": "unknown",
            "build_time_ist": "unknown",
            "error": str(e)
        }


# =====================================================
# 🧾 LOG FORMATTER
# =====================================================
class RequestFormatter(logging.Formatter):
    def format(self, record):
        try:
            record.request_id = getattr(g, "request_id", "N/A")
        except RuntimeError:
            record.request_id = "N/A"
        return super().format(record)


# =====================================================
# 🚀 APP FACTORY
# =====================================================
def create_app(testing: bool = False):
    app = Flask(__name__)
    app.config.from_object(Config)

    # ✅ Important
    app.url_map.strict_slashes = False

    # =====================================================
    # 🧪 TEST CONFIG
    # =====================================================
    if testing:
        app.config.update(
            TESTING=True,
            SQLALCHEMY_DATABASE_URI="sqlite:///:memory:",
            JWT_SECRET_KEY="test-secret"
        )

    # =====================================================
    # 🌐 CORS
    # =====================================================
    CORS(
        app,
        resources={r"/api/*": {"origins": "*"}},
        supports_credentials=True
    )

    # =====================================================
    # 🔗 Extensions
    # =====================================================
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    # =====================================================
    # 🆔 REQUEST ID
    # =====================================================
    @app.before_request
    def assign_request_id():
        g.request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))

    @app.after_request
    def attach_request_id(response):
        response.headers["X-Request-ID"] = g.request_id
        return response

    # =====================================================
    # 📂 LOGGING
    # =====================================================
    logs_path = os.path.join(os.getcwd(), "logs")
    os.makedirs(logs_path, exist_ok=True)

    handler = TimedRotatingFileHandler(
        os.path.join(logs_path, "cart.log"),
        when="midnight",
        backupCount=30,
        encoding="utf-8"
    )

    handler.setFormatter(RequestFormatter(
        "%(asctime)s [%(levelname)s] [REQ:%(request_id)s] %(message)s"
    ))

    if not app.logger.handlers:
        app.logger.addHandler(handler)

    app.logger.setLevel(logging.INFO)

    # =====================================================
    # 📦 ROUTES
    # =====================================================
    from .api.cart_routes import cart_bp
    from .api.checkout_routes import checkout_bp
    from .api.orders_routes import orders_bp

    app.register_blueprint(cart_bp, url_prefix="/api/cart")
    app.register_blueprint(checkout_bp, url_prefix="/api/checkout")
    app.register_blueprint(orders_bp, url_prefix="/api/orders")

    # =====================================================
    # ❤️ HEALTH (HTML + JSON)
    # =====================================================
    @app.get("/")
    def health():
        info = get_build_info()

        # Browser → HTML UI
        if "text/html" in request.headers.get("Accept", ""):
            html = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <title>Cart Service Health</title>
                <style>
                    body {{
                        font-family: Arial;
                        background: #f4f6f8;
                        padding: 40px;
                    }}
                    .card {{
                        max-width: 600px;
                        margin: auto;
                        background: white;
                        padding: 20px;
                        border-radius: 10px;
                        box-shadow: 0 2px 10px rgba(0,0,0,0.1);
                    }}
                    h1 {{
                        text-align: center;
                        color: #fbbc05;
                    }}
                    .row {{
                        display: flex;
                        justify-content: space-between;
                        padding: 8px 0;
                        border-bottom: 1px solid #eee;
                    }}
                </style>
            </head>
            <body>
                <div class="card">
                    <h1>🛒 Cart & Order Service</h1>
                    <div class="row"><b>Status</b><span>🟢 UP</span></div>
                    <div class="row"><b>Version</b><span>{info.get("version")}</span></div>
                    <div class="row"><b>Commit</b><span>{info.get("commit")}</span></div>
                    <div class="row"><b>Branch</b><span>{info.get("branch")}</span></div>
                    <div class="row"><b>UTC</b><span>{info.get("build_time_utc")}</span></div>
                    <div class="row"><b>IST</b><span>{info.get("build_time_ist")}</span></div>
                </div>
            </body>
            </html>
            """
            return html, 200

        # Default → JSON
        return jsonify({
            "status": "cart-order-service UP",
            "build": info
        }), 200

    return app
