from datetime import datetime
from app.extensions import db


class InvoiceHistory(db.Model):
    __tablename__ = "invoice_history"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    order_id = db.Column(
        db.Integer,
        nullable=False
    )

    invoice_version = db.Column(
        db.Integer,
        default=1
    )

    status = db.Column(
        db.String(30),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )