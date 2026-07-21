"""
=========================================================
🚀 Backend Warmup Checker (Parallel Version)
=========================================================

This script follows the SAME FLOW as your Angular code.

Flow
---------------------------------------------------------
1. checking
2. almost        (after >= half of services complete)
3. finalizing    (after all services succeed)
4. ready

Features
---------------------------------------------------------
✓ All requests sent at once
✓ Live console updates
✓ Dynamic progress bar
✓ Parallel warmup
✓ Success / Failure tracking
✓ Cold-start friendly
✓ Pure Python
✓ Lots of comments
"""

import time
import threading
import requests

from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed

# =========================================================
# Configuration
# =========================================================

URLS = [
    "https://backend-auth-service-ks6f.onrender.com",
    "https://backend-product-service-ncl2.onrender.com",
    "https://backend-cart-order-service-q6qh.onrender.com",
    "https://backend-ml-events-service-ba9v.onrender.com",
    "https://backend-ml-recommendation-service-huu6.onrender.com",
]

REQUEST_TIMEOUT = 30

# =========================================================
# Global State
# =========================================================

status = "idle"

completed = 0
success = 0
failed = 0

lock = threading.Lock()

# =========================================================
# Console Status
# =========================================================


def set_status(new_status):

    global status

    if status != new_status:

        status = new_status

        print()
        print("=" * 65)
        print(f"[{datetime.now().strftime('%H:%M:%S')}] STATUS : {status.upper()}")
        print("=" * 65)
        print()


# =========================================================
# Progress Bar
# =========================================================


def show_progress(done, total):

    percent = int((done / total) * 100)

    bar_length = 35

    filled = int(bar_length * done / total)

    bar = "█" * filled + "-" * (bar_length - filled)

    print(
        f"\nProgress : [{bar}] {done}/{total} ({percent}%)"
    )


# =========================================================
# Ping Backend
# =========================================================


def ping_backend(url):

    start = time.time()

    try:

        response = requests.get(
            url,
            timeout=REQUEST_TIMEOUT
        )

        elapsed = time.time() - start

        return {
            "url": url,
            "success": response.ok,
            "status": response.status_code,
            "elapsed": elapsed,
            "error": None
        }

    except Exception as e:

        elapsed = time.time() - start

        return {
            "url": url,
            "success": False,
            "status": None,
            "elapsed": elapsed,
            "error": str(e)
        }


# =========================================================
# Warmup Logic
# =========================================================


def warmup_backends():

    global completed
    global success
    global failed

    total = len(URLS)

    set_status("checking")

    print("🚀 Sending warmup requests...")
    print()

    with ThreadPoolExecutor(max_workers=total) as executor:

        futures = [
            executor.submit(ping_backend, url)
            for url in URLS
        ]

        for future in as_completed(futures):

            result = future.result()

            with lock:

                completed += 1

                if result["success"]:
                    success += 1

                    print(
                        f"✅ [{completed}/{total}] "
                        f"{result['url']}"
                    )

                    print(
                        f"   Response : {result['status']}"
                    )

                    print(
                        f"   Time     : {result['elapsed']:.2f}s"
                    )

                else:

                    failed += 1

                    print(
                        f"❌ [{completed}/{total}] "
                        f"{result['url']}"
                    )

                    if result["status"]:
                        print(
                            f"   HTTP : {result['status']}"
                        )

                    if result["error"]:
                        print(
                            f"   Error: {result['error']}"
                        )

                show_progress(completed, total)

                # Angular-like status update
                if completed >= total / 2:

                    if status == "checking":
                        set_status("almost")

    print()

    # =====================================================
    # Final Stage
    # =====================================================

    if success == total:

        set_status("finalizing")

        print("🔄 Performing final checks...")
        time.sleep(0.8)

        set_status("ready")

        print()
        print("🎉 ALL SERVICES ARE READY")
        print()

        # ===============================================
        # YOUR NEXT STEP
        # ===============================================

        print(">>> Triggering your next step...")
        print(">>> Put your code here.")
        print()

    else:

        set_status("ready")

        print()
        print("⚠️ Finished with some failures.")
        print()

    # =====================================================
    # Summary
    # =====================================================

    print("=" * 65)
    print("SUMMARY")
    print("=" * 65)
    print(f"Total      : {total}")
    print(f"Successful : {success}")
    print(f"Failed     : {failed}")
    print(f"Status     : {status}")
    print("=" * 65)


# =========================================================
# Main
# =========================================================

if __name__ == "__main__":

    print()
    print("🚀 Backend Cold Start Warmup")
    print("=" * 65)

    warmup_backends()