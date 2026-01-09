import os


class Config:
    """
    Cart + Order Service Configuration
    """

    SECRET_KEY = os.getenv("SECRET_KEY", "cart-secret-key")

    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        "sqlite:///cart.db"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # MUST MATCH AUTH SERVICE
    JWT_SECRET_KEY = os.getenv(
        "JWT_SECRET_KEY",
        "jwt-secret-key"
    )
