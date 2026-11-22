"""
classifier.py - Support ticket intent and category classification.
(COMPLETE - do not edit.)
"""
from __future__ import annotations


def classify_ticket(ticket: dict) -> str:
    """Classify ticket into 'password_reset', 'billing', or 'general'.

    Parameters
    ----------
    ticket : dict
        Ticket dictionary containing 'subject' and 'body'.

    Returns
    -------
    str
        Detected category name.
    """
    text = (ticket.get("subject", "") + " " + ticket.get("body", "")).lower()

    if any(k in text for k in ("password", "reset", "forgot", "login issue", "unlock")):
        return "password_reset"
    elif any(k in text for k in ("invoice", "payment", "billing", "charge", "refund")):
        return "billing"
    else:
        return "general"
