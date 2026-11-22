FROM python:3.12.3-slim-bookworm

RUN apt-get update && apt-get install -y --no-install-recommends \
    iproute2 \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY app/ /app/
COPY scripts/ /scripts/

RUN mkdir -p /app/reports /app/logs

WORKDIR /app

ENTRYPOINT ["/bin/sh", "/scripts/entrypoint.sh"]
