from app.extensions import db
from app.models.order_analytics import OrderAnalytics


class OrderAnalyticsService:

    @staticmethod
    def create_record(
        order_id,
        total_price,
        status
    ):

        record = OrderAnalytics(
            order_id=order_id,
            total_price=total_price,
            status=status
        )

        db.session.add(record)
        db.session.commit()