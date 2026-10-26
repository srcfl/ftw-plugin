#!/usr/bin/env python3
"""Build the ChatGPT and Codex upload ZIP from openai/package.

Run from the repository root: python3 scripts/build-chatgpt-package.py
Writes dist/ftw-chatgpt-<version>.zip. Refuses to build if a file differs from openai/SHA256SUMS.
"""
import hashlib
import json
import pathlib
import sys
import zipfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
PKG = ROOT / "openai/package"

sums = {}
for line in (ROOT / "openai/SHA256SUMS").read_text().splitlines():
    digest, rel = line.split(maxsplit=1)
    sums[rel.removeprefix("./")] = digest
for rel, digest in sums.items():
    if hashlib.sha256((PKG / rel).read_bytes()).hexdigest() != digest:
        sys.exit(f"{rel} differs from openai/SHA256SUMS; update the sums only for a new OpenAI submission")

version = json.loads((PKG / "plugin.json").read_text())["version"]
out = ROOT / "dist" / f"ftw-chatgpt-{version}.zip"
out.parent.mkdir(exist_ok=True)
with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as z:
    for rel in sorted(sums):
        info = zipfile.ZipInfo(rel, date_time=(2026, 1, 1, 0, 0, 0))
        info.compress_type = zipfile.ZIP_DEFLATED
        info.external_attr = 0o644 << 16
        z.writestr(info, (PKG / rel).read_bytes())
print(f"{out.relative_to(ROOT)}: {len(sums)} files, sha256 {hashlib.sha256(out.read_bytes()).hexdigest()}")
