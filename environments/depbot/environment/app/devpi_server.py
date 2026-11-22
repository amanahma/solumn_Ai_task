"""
devpi_server.py - Internal private package index stand-in (Devpi API compatible).
(COMPLETE - do not edit.)

Receives published wheels, writes them to /app/data/index_store/,
and logs all upload transactions to /app/logs/index_uploads.log.
"""
from __future__ import annotations
import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

STORE_DIR = Path(os.environ.get("INDEX_STORE", "/app/data/index_store"))
LOG_PATH = Path(os.environ.get("INDEX_LOG_PATH", "/app/logs/index_uploads.log"))
PORT = int(os.environ.get("INDEX_PORT", "8082"))


class IndexHandler(BaseHTTPRequestHandler):
    def log_message(self, format: str, *args) -> None:
        pass

    def _record_upload(self, filename: str, data: bytes) -> None:
        STORE_DIR.mkdir(parents=True, exist_ok=True)
        LOG_PATH.parent.mkdir(parents=True, exist_ok=True)

        target_file = STORE_DIR / filename
        target_file.write_bytes(data)

        digest = hashlib.sha256(data).hexdigest().lower()
        entry = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "filename": filename,
            "bytes_received": len(data),
            "sha256": digest,
            "client_ip": self.client_address[0],
        }
        with LOG_PATH.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(entry) + "\n")
        print(f"[devpi] stored {filename} ({len(data)} bytes, sha256={digest[:12]}...)", flush=True)

    def do_POST(self) -> None:
        length = int(self.headers.get("Content-Length", 0))
        data = self.rfile.read(length) if length else b""
        filename = self.headers.get("X-Wheel-Filename") or self.path.split("/")[-1] or "upload.whl"
        if not filename.endswith(".whl"):
            filename = f"{filename}.whl"

        # Check internal namespace policy
        is_allowed = (self.headers.get("X-Allow-Upstream") == "true" or "allow_upstream=true" in self.path)
        if not is_allowed:
            try:
                import io, zipfile
                with zipfile.ZipFile(io.BytesIO(data), "r") as zf:
                    for name in zf.namelist():
                        if name.endswith("METADATA"):
                            meta = zf.read(name).decode("utf-8", errors="replace")
                            for line in meta.splitlines():
                                if line.startswith("Name:"):
                                    pkg_name = line.split(":", 1)[1].strip()
                                    if pkg_name.startswith("internal-"):
                                        is_allowed = True
                                    break
                            break
            except Exception:
                pass

        if not is_allowed:
            self.send_response(409)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"error": "Package name \'acme-lib\' conflicts with internal namespace policy \xe2\x80\x94 see internal packaging guidelines"}')
            print(f"[devpi] rejected {filename} (409 Conflict: internal namespace policy violation)", flush=True)
            return

        self._record_upload(filename, data)
        self.send_response(201)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(b'{"status":"uploaded"}')

    def do_PUT(self) -> None:
        self.do_POST()

    def do_GET(self) -> None:
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        wheels = [f.name for f in STORE_DIR.glob("*.whl")] if STORE_DIR.exists() else []
        self.wfile.write(json.dumps({"packages": wheels}).encode("utf-8"))


def main() -> None:
    server = HTTPServer(("0.0.0.0", PORT), IndexHandler)
    print(f"[devpi] listening on port {PORT}", flush=True)
    server.serve_forever()


if __name__ == "__main__":
    main()
