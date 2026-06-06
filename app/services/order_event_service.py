from app.extensions import db
from app.models.order_event import OrderEvent


class OrderEventService:

    @staticmethod
    def create_event(order_id, event_type):

        event = OrderEvent(
            order_id=order_id,
            event_type=event_type
        )

        db.session.add(event)
        db.session.commit()