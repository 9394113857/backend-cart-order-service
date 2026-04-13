# ===============================
# 🔧 CONFIG (PRODUCTION READY)
# ===============================

import os


class Config:
    # 🔐 SECRET
    SECRET_KEY = os.getenv("SECRET_KEY", "cart-secret")

    # 🗄️ DATABASE
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "sqlite:///cart.db"   # ✅ local fallback
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 🔑 JWT
    JWT_SECRET_KEY = os.getenv(
        "JWT_SECRET_KEY",
        "jwt-secret-key"
    )

    # 🔗 PRODUCT SERVICE (MICROSERVICE URL)
    PRODUCT_BASE_URL = os.getenv(
        "PRODUCT_BASE_URL",
        "http://127.0.0.1:5002"   # ✅ local fallback
    )