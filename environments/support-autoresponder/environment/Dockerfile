FROM python:3.12.3-slim-bookworm

COPY app/requirements.txt /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

COPY app/ /app/
COPY scripts/ /scripts/

RUN mkdir -p /app/data/sent_emails /app/logs

WORKDIR /app

ENTRYPOINT ["/bin/sh", "/scripts/entrypoint.sh"]
