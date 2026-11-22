"""
autoresponder_runner.py - Main entry point for the support-autoresponder service.
(COMPLETE - do not edit.)

Loads configuration, processes sample incoming tickets, and dispatches responses.
"""
from __future__ import annotations
import os
import sys
import tomllib
from pathlib import Path

from responder import dispatch_ticket_response

CONFIG_PATH = Path(os.environ.get("CONFIG_PATH", "/app/config.toml"))
if not CONFIG_PATH.exists():
    CONFIG_PATH = Path(__file__).parent / "config.toml"


SAMPLE_TICKETS = [
    {
        "ticket_id": "TICK-101",
        "user_id": "usr_94102",
        "recipient": "alice@customer.com",
        "subject": "Need password reset assistance",
        "body": "I cannot log in to my account. Please send a reset link.",
    },
    {
        "ticket_id": "TICK-102",
        "user_id": "usr_88219",
        "recipient": "bob@customer.com",
        "subject": "Question regarding recent invoice",
        "body": "Could you provide details on the charge from last week?",
    },
]


def load_config() -> dict:
    raw = CONFIG_PATH.read_bytes().lstrip(b"\xef\xbb\xbf")
    return tomllib.loads(raw.decode("utf-8"))


def main() -> int:
    cfg = load_config()
    base_url = cfg["auth"]["base_url"]
    templates_dir = os.environ.get("TEMPLATES_DIR", cfg["templates"]["dir"])

    print(f"[runner] starting support-autoresponder with base_url={base_url}", flush=True)

    for ticket in SAMPLE_TICKETS:
        res = dispatch_ticket_response(ticket, templates_dir=templates_dir, base_url=base_url)
        print(f"[runner] processed {res.get('ticket_id')} (category={res.get('category')})", flush=True)

    print("[runner] all tickets processed successfully", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
