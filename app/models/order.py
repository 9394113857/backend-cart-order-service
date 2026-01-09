from app.extensions import db
from datetime import datetime


class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)

    contact = db.Column(db.String(20), nullable=False)
    address = db.Column(db.String(500), nullable=False)

    total_price = db.Column(db.Float, nullable=False)

    status = db.Column(
        db.String(20),
        default="placed"  # placed | cancelled | shipped | delivered
    )

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
