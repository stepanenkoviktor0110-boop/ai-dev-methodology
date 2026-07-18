#!/usr/bin/env python
"""deploy-safety SMOKE — deterministic post-deploy runtime-behavior check (no LLM).

Proves the right DATA is bound after a deploy, deterministically — so it can safely gate an
AUTOMATIC rollback. Each manifest runtime-behavior check is one of two kinds:

- `command`: run a shell command (a read-only DB/data query) and assert its output. This is the
  preferred kind — it reflects bound-data state directly, free of the conversational endpoint's
  schedule window, Origin allowlist and LLM phrasing. `remote: true` runs it on the deploy target
  over ssh (where the DB is local). Example fingerprint: "bot X has an indexed product_feed with
  chunks > 0" → prints BOUND.
- `url`: HTTP GET/POST an endpoint and assert a substring. Use only for a genuinely
  schedule/auth-independent reflection endpoint — NOT a scheduled/Origin-gated widget chat path.

A check whose command/url still contains a `<placeholder>` is skipped (unarmed).

    python smoke.py --manifest deploy-manifest.yml [--ssh HOST] [--timeout 20]

Exit 0 = all armed anchors pass; 1 = an anchor failed (caller rolls back); 2 = usage/manifest error.
NEVER prints secret values.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: smoke needs pyyaml", file=sys.stderr)
    sys.exit(2)


def run_command(check: dict, ssh_host: str | None, timeout: int) -> tuple[bool, str]:
    cmd = check["command"]
    if check.get("remote"):
        if not ssh_host:
            return False, "check is remote:true but no --ssh HOST given"
        argv = ["ssh", "-o", "BatchMode=yes", ssh_host, cmd]
    else:
        argv = cmd  # local shell string
    try:
        p = subprocess.run(
            argv,
            shell=not check.get("remote"),
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
        )
    except (subprocess.TimeoutExpired, OSError) as e:
        return False, f"command error: {e}"
    out = (p.stdout + p.stderr).strip()
    if p.returncode != 0:
        return False, f"exit {p.returncode}: {out.splitlines()[-1] if out else ''}"
    want = check.get("expect_substring", "")
    if want and want not in out:
        return False, f"expected {want!r}, got: {out[:120]!r}"
    return True, f"ok ({out[:60]!r})" if out else "ok"


def call_url(check: dict, timeout: int) -> tuple[bool, str]:
    url = check.get("url", "")
    request = check.get("request", "")
    method = (check.get("method") or ("POST" if request else "GET")).upper()
    data = None
    headers = {"Accept": "*/*"}
    for k, v in (check.get("headers") or {}).items():
        headers[k] = v
    if method == "POST":
        field = check.get("payload_field", "message")
        payload = check.get("payload") or {field: request}
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:  # noqa: S310 (trusted deploy URL)
            code, body = resp.getcode(), resp.read().decode("utf-8", errors="replace")
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
        return False, f"anchor missing: {want!r}"
    return True, "anchor present" if want else "200 non-empty"


def _armed(check: dict) -> bool:
    """A check is armed once its command/url no longer holds a <placeholder>."""
    blob = check.get("command") or check.get("url") or ""
    return bool(blob) and "<" not in blob and "<" not in str(check.get("expect_substring", ""))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--manifest", default="deploy-manifest.yml")
    ap.add_argument("--ssh", help="ssh host for remote:true command checks")
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
    all_checks = (manifest.get("classes", {}).get("runtime-behavior", {}) or {}).get("checks", [])
    checks = [c for c in all_checks if _armed(c)]
    if not checks:
        print("smoke: no armed runtime-behavior checks — skipped (fill manifest to enable)")
        return 0

    failed = 0
    for c in checks:
        if c.get("command"):
            ok, detail = run_command(c, args.ssh, args.timeout)
        else:
            ok, detail = call_url(c, args.timeout)
        print(f"  [{'PASS' if ok else 'FAIL'}] {c.get('service', c.get('url') or c.get('command'))}: {detail}")
        failed += 0 if ok else 1
    if failed:
        print(f"SMOKE FAILED: {failed} anchor(s) — deploy will roll back", file=sys.stderr)
        return 1
    print("SMOKE OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
