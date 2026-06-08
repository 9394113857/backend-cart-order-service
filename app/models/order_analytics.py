from datetime import datetime
from app.extensions import db

# This model is designed to store analytical data related to orders. It can be used to track various metrics such as total price, order status, and timestamps for when the analytics were created. This information can be valuable for generating reports, analyzing trends, and making data-driven decisions to improve the order processing system.
class OrderAnalytics(db.Model):
    __tablename__ = "order_analytics"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    order_id = db.Column(
        db.Integer,
        nullable=False
    )

    total_price = db.Column(
        db.Float,
        nullable=False
    )

    status = db.Column(
        db.String(30),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )