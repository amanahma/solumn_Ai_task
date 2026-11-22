FROM python:3.12.3-slim-bookworm

COPY app/ /app/
COPY scripts/ /scripts/

RUN mkdir -p /app/data/cache /app/data/index_store /app/data/mirror_store /app/logs

WORKDIR /app

ENTRYPOINT ["/bin/sh", "/scripts/entrypoint.sh"]
