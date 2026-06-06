import os
import json
from datetime import datetime


class PostOrderService:

    # ============================================================
    # INVOICE FILE
    # ============================================================
    @staticmethod
    def save_invoice_file(order_id, total_price, status):

        invoices_dir = os.path.join(
            os.getcwd(),
            "storage",
            "invoices"
        )

        os.makedirs(invoices_dir, exist_ok=True)

        file_path = os.path.join(
            invoices_dir,
            f"order_{order_id}.json"
        )

        payload = {
            "order_id": order_id,
            "total_price": total_price,
            "status": status,
            "generated_at": datetime.utcnow().isoformat()
        }

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=4)

    # ============================================================
    # ANALYTICS FILE
    # ============================================================
    @staticmethod
    def save_analytics_file(order_id, total_price, status):

        analytics_dir = os.path.join(
            os.getcwd(),
            "storage",
            "analytics"
        )

        os.makedirs(analytics_dir, exist_ok=True)

        file_path = os.path.join(
            analytics_dir,
            f"order_{order_id}.json"
        )

        payload = {
            "order_id": order_id,
            "total_price": total_price,
            "status": status,
            "analytics_created_at": datetime.utcnow().isoformat()
        }

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=4)

    # ============================================================
    # AUDIT FILE
    # ============================================================
    @staticmethod
    def save_audit_file(order_id, status):

        audit_dir = os.path.join(
            os.getcwd(),
            "storage",
            "audit"
        )

        os.makedirs(audit_dir, exist_ok=True)

        file_path = os.path.join(
            audit_dir,
            f"order_{order_id}.txt"
        )

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(
                f"ORDER_ID={order_id}\n"
                f"STATUS={status}\n"
                f"TIMESTAMP={datetime.utcnow().isoformat()}\n"
            )