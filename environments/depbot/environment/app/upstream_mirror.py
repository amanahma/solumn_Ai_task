"""
upstream_mirror.py - Upstream package repository mirror stand-in.
(COMPLETE - do not edit.)

Generates and serves authentic vendor wheel packages and package metadata.
"""
from __future__ import annotations
import hashlib
import json
import os
import sys
import tempfile
import zipfile
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

MIRROR_STORE = Path(os.environ.get("MIRROR_STORE", "/app/data/mirror_store"))
PORT = int(os.environ.get("MIRROR_PORT", "8081"))


def create_authentic_wheel(dest_dir: Path, package: str = "acme-lib", version: str = "1.2.0") -> tuple[Path, str]:
    """Generate a valid, deterministic wheel artifact and return (path, sha256)."""
    dest_dir.mkdir(parents=True, exist_ok=True)
    norm = package.replace("-", "_")
    filename = f"{norm}-{version}-py3-none-any.whl"
    wheel_path = dest_dir / filename

    with tempfile.TemporaryDirectory() as tmp:
        tpath = Path(tmp)
        pkg_dir = tpath / norm
        pkg_dir.mkdir()
        (pkg_dir / "__init__.py").write_text(f'__version__ = "{version}"\n__package_name__ = "{package}"\n', encoding="utf-8")

        dist_info = tpath / f"{norm}-{version}.dist-info"
        dist_info.mkdir()
        (dist_info / "METADATA").write_text(
            f"Metadata-Version: 2.1\nName: {package}\nVersion: {version}\nSummary: Acme core library\n",
            encoding="utf-8"
        )
        (dist_info / "WHEEL").write_text(
            "Wheel-Version: 1.0\nGenerator: bdist_wheel\nRoot-Is-Purelib: true\nTag: py3-none-any\n",
            encoding="utf-8"
        )

        with zipfile.ZipFile(wheel_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
            for item in sorted(tpath.rglob("*")):
                if item.is_file():
                    zinfo = zipfile.ZipInfo(item.relative_to(tpath).as_posix(), date_time=(2024, 1, 1, 0, 0, 0))
                    zf.writestr(zinfo, item.read_bytes())

    h = hashlib.sha256(wheel_path.read_bytes()).hexdigest().lower()
    return wheel_path, h


def get_metadata(package: str = "acme-lib", version: str = "1.2.0") -> dict:
    wpath, digest = create_authentic_wheel(MIRROR_STORE, package, version)
    return {
        "package": package,
        "version": version,
        "filename": wpath.name,
        "sha256": digest,
        "size": wpath.stat().st_size,
    }


class MirrorHandler(BaseHTTPRequestHandler):
    def log_message(self, format: str, *args) -> None:
        pass

    def do_GET(self) -> None:
        if self.path.startswith("/metadata/"):
            # /metadata/<package>/<version>
            parts = self.path.strip("/").split("/")
            pkg = parts[1] if len(parts) > 1 else "acme-lib"
            ver = parts[2] if len(parts) > 2 else "1.2.0"
            meta = get_metadata(pkg, ver)
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(meta).encode("utf-8"))
        elif self.path.startswith("/wheels/"):
            fname = self.path.split("/")[-1]
            fpath = MIRROR_STORE / fname
            if not fpath.exists():
                get_metadata("acme-lib", "1.2.0")
            if fpath.exists():
                data = fpath.read_bytes()
                self.send_response(200)
                self.send_header("Content-Type", "application/octet-stream")
                self.send_header("Content-Length", str(len(data)))
                self.end_headers()
                self.wfile.write(data)
            else:
                self.send_response(404)
                self.end_headers()
        else:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b'{"status":"mirror-ready"}')


def main() -> None:
    create_authentic_wheel(MIRROR_STORE, "acme-lib", "1.2.0")
    server = HTTPServer(("0.0.0.0", PORT), MirrorHandler)
    print(f"[mirror] listening on port {PORT}", flush=True)
    server.serve_forever()


if __name__ == "__main__":
    main()
