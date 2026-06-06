from datetime import datetime
from app.extensions import db


class OrderEvent(db.Model):
    __tablename__ = "order_events"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    order_id = db.Column(
        db.Integer,
        nullable=False
    )

    event_type = db.Column(
        db.String(50),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )