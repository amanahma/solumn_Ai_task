"""
netutils.py - Network validation and endpoint parsing helpers for netdiag-cli.
(COMPLETE - do not edit.)
"""
from __future__ import annotations
import ipaddress


def parse_endpoint(endpoint: str, default_port: int = 80) -> tuple[str, int]:
    """Parse a host string or host:port pair into (host, port).

    Parameters
    ----------
    endpoint : str
        Endpoint string, e.g. "127.0.0.1", "10.0.1.5:8080".
    default_port : int, default 80
        Port to use if not specified in endpoint.

    Returns
    -------
    tuple[str, int]
        (host, port) tuple.
    """
    endpoint = endpoint.strip()
    if ":" in endpoint:
        host, port_str = endpoint.split(":", 1)
        try:
            return host.strip(), int(port_str.strip())
        except ValueError:
            return host.strip(), default_port
    return endpoint, default_port


def is_allowed_host(host: str) -> bool:
    """Return True if host belongs to approved internal network ranges.

    Approved ranges include:
      - Loopback: 127.0.0.0/8
      - RFC 1918 internal subnets: 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16

    Parameters
    ----------
    host : str
        IP address or hostname string.

    Returns
    -------
    bool
        True if the host is within approved internal subnets, False otherwise.
    """
    clean_host = host.split(":")[0].strip()
    try:
        ip = ipaddress.ip_address(clean_host)
        return (
            ip.is_loopback
            or (ip in ipaddress.ip_network("10.0.0.0/8"))
            or (ip in ipaddress.ip_network("172.16.0.0/12"))
            or (ip in ipaddress.ip_network("192.168.0.0/16"))
        )
    except ValueError:
        return clean_host in ("localhost", "127.0.0.1")
