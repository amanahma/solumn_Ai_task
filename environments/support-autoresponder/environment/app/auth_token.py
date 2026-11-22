"""
auth_token.py - HMAC token generation and verification for auth links.
(COMPLETE - do not edit.)
"""
from __future__ import annotations
import hashlib
import hmac
import time


SECRET_KEY = b"acme_corp_auth_secret_key_2024"


def sign_token(user_id: str, timestamp: int | None = None) -> str:
    """Generate an HMAC-SHA256 signature token for user_id."""
    ts = timestamp if timestamp is not None else int(time.time())
    message = f"{user_id}:{ts}".encode("utf-8")
    sig = hmac.new(SECRET_KEY, message, hashlib.sha256).hexdigest()[:32]
    return f"{ts}.{sig}"


def verify_token(user_id: str, token: str, max_age_seconds: int = 3600) -> bool:
    """Verify validity and signature of a token for user_id."""
    try:
        ts_str, sig = token.split(".", 1)
        ts = int(ts_str)
        if time.time() - ts > max_age_seconds:
            return False
        expected_sig = hmac.new(SECRET_KEY, f"{user_id}:{ts}".encode("utf-8"), hashlib.sha256).hexdigest()[:32]
        return hmac.compare_digest(sig, expected_sig)
    except Exception:
        return False
