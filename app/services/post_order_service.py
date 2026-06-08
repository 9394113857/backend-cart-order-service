import os
import json
import threading
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor


class PostOrderService:
    # Thread pool executor for handling file I/O operations asynchronously
    executor = ThreadPoolExecutor(max_workers=3)

    # ============================================================
    # INVOICE FILE
    # ============================================================
    @staticmethod
    def save_invoice_file(order_id, total_price, status):
        print(
            f"Invoice Thread = {threading.current_thread().name}"
        )

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
        print(
            f"Analytics Thread = {threading.current_thread().name}"
        )

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
        print(
            f"Audit Thread = {threading.current_thread().name}"
        )

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

    # ============================================================
    # MULTITHREADED FILE GENERATION
    # ============================================================
    @staticmethod
    def process_order_files(
        order_id,
        total_price,
        status
    ):
        PostOrderService.executor.submit(
            PostOrderService.save_invoice_file,
            order_id,
            total_price,
            status
        )

        PostOrderService.executor.submit(
            PostOrderService.save_analytics_file,
            order_id,
            total_price,
            status
        )

        PostOrderService.executor.submit(
            PostOrderService.save_audit_file,
            order_id,
            status
        )