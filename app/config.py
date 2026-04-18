# ===============================
# 🔧 CONFIG (PRODUCTION READY)
# ===============================

import os
from dotenv import load_dotenv

# 🔹 Load .env file (VERY IMPORTANT)
load_dotenv()


class Config:
    # 🔐 SECRET
    SECRET_KEY = os.getenv("SECRET_KEY", "cart-secret")

    # 🗄️ DATABASE
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "sqlite:///cart.db"   # ✅ fallback if no env
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # 🔑 JWT
    JWT_SECRET_KEY = os.getenv(
        "JWT_SECRET_KEY",
        "jwt-secret-key"
    )

    # 🔗 PRODUCT SERVICE
    PRODUCT_BASE_URL = os.getenv(
        "PRODUCT_BASE_URL",
        "http://127.0.0.1:5002"   # ✅ fallback if no env
    )