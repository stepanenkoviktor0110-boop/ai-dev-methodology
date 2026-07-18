#!/usr/bin/env python
"""deploy-safety SMOKE — deterministic post-deploy runtime-behavior check (no LLM).

For each manifest runtime-behavior check: call the service endpoint with the anchor request and
assert HTTP 200 + non-empty body + the expected substring is present (a token that only correct
data/config produces — e.g. a price/SKU only the right feed yields). Deterministic on purpose: it
gates an AUTOMATIC rollback, so it must not depend on LLM judgment or flaky external egress.

    python smoke.py --manifest deploy-manifest.yml [--timeout 20]

Exit 0 = all anchors present; 1 = an anchor failed (caller rolls back); 2 = usage/manifest error.
"""

from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: smoke needs pyyaml", file=sys.stderr)
    sys.exit(2)


def call(check: dict, timeout: int) -> tuple[bool, str]:
    url = check.get("url", "")
    request = check.get("request", "")
    method = (check.get("method") or ("POST" if request else "GET")).upper()
    data = None
    headers = {"Accept": "*/*"}
    if method == "POST":
        # payload_field lets a project map the anchor question onto its /answer contract
        field = check.get("payload_field", "message")
        payload = check.get("payload") or {field: request}
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:  # noqa: S310 (trusted deploy URL)
            code = resp.getcode()
            body = resp.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        return False, f"HTTP {e.code}"
    except (urllib.error.URLError, TimeoutError, OSError) as e:
        return False, f"unreachable: {e}"
    if code != 200:
        return False, f"HTTP {code}"
    if not body.strip():
        return False, "empty body"
    want = check.get("expect_substring", "")
    if want and want not in body:
        return False, f"anchor missing: {want!r} not in response"
    return True, "anchor present" if want else "responds 200 non-empty"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--manifest", default="deploy-manifest.yml")
    ap.add_argument("--timeout", type=int, default=20)
    args = ap.parse_args()

    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")

    man = Path(args.manifest)
    if not man.exists():
        print(f"ERROR: {man} missing", file=sys.stderr)
        return 2
    manifest = yaml.safe_load(man.read_text(encoding="utf-8")) or {}
    checks = (manifest.get("classes", {}).get("runtime-behavior", {}) or {}).get("checks", [])
    checks = [c for c in checks if c.get("url", "").startswith("http") and "<" not in c.get("url", "")]
    if not checks:
        print("smoke: no runtime-behavior checks configured — skipped (fill manifest to enable)")
        return 0

    failed = 0
    for c in checks:
        ok, detail = call(c, args.timeout)
        print(f"  [{'PASS' if ok else 'FAIL'}] {c.get('service', c.get('url'))}: {detail}")
        failed += 0 if ok else 1
    if failed:
        print(f"SMOKE FAILED: {failed} anchor(s) — deploy will roll back", file=sys.stderr)
        return 1
    print("SMOKE OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
