from datetime import datetime
from app.extensions import db

# This model keeps track of the history of invoices for each order. It allows us to maintain a record of all invoice versions and their statuses, which can be useful for auditing and troubleshooting purposes.
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