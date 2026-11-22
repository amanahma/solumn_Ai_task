"""
email_validator.py - Email address validation and domain parsing utilities.
(COMPLETE - do not edit.)
"""
from __future__ import annotations
import re


EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")


def is_valid_email(address: str) -> bool:
    """Validate whether address adheres to standard email format.

    Parameters
    ----------
    address : str
        Email address string to validate.

    Returns
    -------
    bool
        True if address matches email format, False otherwise.
    """
    if not address or not isinstance(address, str):
        return False
    return bool(EMAIL_REGEX.match(address.strip()))


def extract_domain(address: str) -> str:
    """Extract and return lowercase domain component from email address.

    Parameters
    ----------
    address : str
        Email address string.

    Returns
    -------
    str
        Domain string, or empty string if malformed.
    """
    if "@" not in address:
        return ""
    return address.split("@", 1)[1].strip().lower()
