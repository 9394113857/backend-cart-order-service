# =====================================================
# 🐳 DOCKERFILE – CART + ORDER SERVICE (FINAL)
# =====================================================

FROM python:3.11-slim

WORKDIR /app

# 🔥 Build args
ARG APP_VERSION
ARG APP_COMMIT
ARG APP_BRANCH

# 📦 Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 📂 Copy code
COPY . .

# 🧾 Build metadata
RUN python - <<EOF
import json
from datetime import datetime, timezone, timedelta

ist = timezone(timedelta(hours=5, minutes=30))

data = {
    "version": "${APP_VERSION}",
    "commit": "${APP_COMMIT}",
    "branch": "${APP_BRANCH}",
    "build_time_utc": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"),
    "build_time_ist": datetime.now(ist).strftime("%Y-%m-%d %H:%M:%S IST")
}

with open("build_info.json", "w") as f:
    json.dump(data, f, indent=2)
EOF

# 🚀 Run
CMD ["sh", "-c", "gunicorn run:app -w 1 -b 0.0.0.0:$PORT --access-logfile - --error-logfile -"]
