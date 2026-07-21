# from curses import echo
import os
from app import create_app

# Create Flask app at import time (required for Gunicorn later)
app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5003))
    app.run(host="0.0.0.0", port=port)

# venv\Scripts\activate

# echo $env:FLASK_APP
# $env:FLASK_APP = "run.py"
# echo $env:FLASK_APP


# ------------------------------------------------------------
# Initialize migrations (Run ONLY ONCE per project)
# Creates the migrations/ folder
# ------------------------------------------------------------
# flask db init

# ------------------------------------------------------------
# Create a new migration
# Run this whenever models.py changes
# ------------------------------------------------------------
# flask db migrate -m "Initial migration"

# Example:
# flask db migrate -m "Add cart table"
# flask db migrate -m "Add order status"

# ------------------------------------------------------------
# Apply pending migrations to the database
# ------------------------------------------------------------
# flask db upgrade


# Start Flask in Debug Mode (Development Only)
# Auto Reload + Live Code Changes + Debugger
# flask run --host=0.0.0.0 --port=5003 --debug
# flask run --port 5003 # This will only work if you have set FLASK_RUN_HOST=0.0.0.0 and FLASK_RUN_PORT=5003 in your environment variables
