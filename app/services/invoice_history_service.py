from app.extensions import db
from app.models.invoice_history import InvoiceHistory


class InvoiceHistoryService:

    @staticmethod
    def create_record(order_id, status):

        record = InvoiceHistory(
            order_id=order_id,
            status=status
        )

        db.session.add(record)
        db.session.commit()