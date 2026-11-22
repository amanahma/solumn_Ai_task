FROM python:3.12.3-slim-bookworm

# Install dependencies
COPY app/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

# Copy application files
COPY app/ /app/
COPY scripts/ /scripts/

# Create required directories
RUN mkdir -p /app/data/source /app/data/encrypted /app/data/decrypted \
             /app/secure-storage /app/logs

# Seed deterministic source data
RUN /bin/sh /scripts/seed_data.sh

WORKDIR /app

ENTRYPOINT ["/bin/sh", "/scripts/entrypoint.sh"]
