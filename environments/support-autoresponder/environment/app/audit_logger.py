"""
audit_logger.py - Structured audit logging for customer support actions.
(COMPLETE - do not edit.)
"""
from __future__ import annotations
import json
import os
from datetime import datetime, timezone
from pathlib import Path

DEFAULT_AUDIT_LOG = Path(os.environ.get("AUDIT_LOG_PATH", "/app/logs/support_audit.log"))


def record_action(
    action: str,
    ticket_id: str,
    details: dict | None = None,
    log_path: Path | None = None,
) -> None:
    """Record a structured event entry in the support audit log.

    Parameters
    ----------
    action : str
        Action name (e.g. 'ticket_received', 'response_rendered', 'email_dispatched').
    ticket_id : str
        Identifier of the target ticket.
    details : dict, optional
        Additional event metadata.
    log_path : Path, optional
        Destination log file override.
    """
    target = log_path or DEFAULT_AUDIT_LOG
    target.parent.mkdir(parents=True, exist_ok=True)
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "action": action,
        "ticket_id": ticket_id,
        "details": details or {},
    }
    with target.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry) + "\n")
