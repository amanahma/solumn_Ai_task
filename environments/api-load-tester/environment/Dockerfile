# ── Base image (pinned) ────────────────────────────────────────────────────────
FROM python:3.12.3-slim-bookworm

# ── System dependencies ────────────────────────────────────────────────────────
RUN apt-get update \
 && apt-get install -y --no-install-recommends gcc curl \
 && rm -rf /var/lib/apt/lists/*

# ── Python dependencies ────────────────────────────────────────────────────────
WORKDIR /app
COPY app/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# ── Application code ───────────────────────────────────────────────────────────
COPY app/ /app/

# ── Runtime directories ────────────────────────────────────────────────────────
RUN mkdir -p /app/logs /app/results /app/secure-storage \
 && chmod 777 /app/logs /app/results /app/secure-storage

# ── Startup: launch the API stand-in in the background, then idle ──────────────
# The grader (tests/grader.py) will run controller.py itself after the agent
# has finished editing.  The stand-in must already be up when that happens.
COPY scripts/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

ENTRYPOINT ["/bin/sh", "/entrypoint.sh"]
