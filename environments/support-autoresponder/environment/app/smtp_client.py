"""
smtp_client.py - Outbound SMTP delivery client and transaction logger.
(COMPLETE - do not edit.)
"""
from __future__ import annotations
import json
import os
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_OUTBOX = Path(os.environ.get("SMTP_OUTBOX", "/app/data/sent_emails"))
DEFAULT_LOG = Path(os.environ.get("SMTP_LOG_PATH", "/app/logs/smtp_sent.log"))


def send_email(
    to_addr: str,
    subject: str,
    html_body: str,
    ticket_id: str,
    outbox_dir: Path | None = None,
    log_path: Path | None = None,
) -> Path:
    """Deliver email by writing formatted HTML to outbox and logging record."""
    outbox = outbox_dir or DEFAULT_OUTBOX
    outbox.mkdir(parents=True, exist_ok=True)
    log_file = log_path or DEFAULT_LOG
    log_file.parent.mkdir(parents=True, exist_ok=True)

    email_file = outbox / f"{ticket_id}.html"
    email_file.write_text(html_body, encoding="utf-8")

    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "ticket_id": ticket_id,
        "recipient": to_addr,
        "subject": subject,
        "email_file": str(email_file),
    }
    with log_file.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry) + "\n")

    print(f"[smtp] sent email for ticket #{ticket_id} to {to_addr} -> {email_file}", flush=True)
    return email_file
