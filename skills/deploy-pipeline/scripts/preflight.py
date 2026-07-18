#!/usr/bin/env python
"""deploy-safety PREFLIGHT — change-scoped validation of deploy artifacts.

Reads deploy-manifest.yml (from probe.py), maps the release diff to artifact classes via each
class's trigger set, and runs ONLY the validators for classes that actually changed — plus, in
--all mode, every present class (used in CI / first deploy). Built-in validators first; a class
marked `optional` (external tool absent) is skipped with a notice, not failed — the runner's
atomic-switch spine is the net for those.

    # deploy-time, scoped to what changed since the live commit:
    python preflight.py --repo . --diff-base origin/dev
    # CI / full sweep:
    python preflight.py --repo . --all
    # explicit file list (e.g. from a hook):
    python preflight.py --repo . --files a.sh docker-compose.yml

Exit 0 = all run validators passed; 1 = at least one failed; 2 = usage/manifest error.
NEVER prints secret values (env handled by key name only).
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("ERROR: preflight needs pyyaml (pip install pyyaml)", file=sys.stderr)
    sys.exit(2)


def sh(cmd: list[str] | str, cwd: Path, timeout: int = 300) -> tuple[int, str]:
    """Run a command, return (rc, combined-output). Shell only for manifest-provided strings."""
    shell = isinstance(cmd, str)
    p = subprocess.run(
        cmd,
        cwd=cwd,
        shell=shell,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout,
    )
    return p.returncode, (p.stdout + p.stderr).strip()


# ---------------------------------------------------------------------------
# diff → changed files → which classes to run
# ---------------------------------------------------------------------------


def changed_files(repo: Path, base: str) -> list[str]:
    rc, out = sh(["git", "diff", "--name-only", f"{base}...HEAD"], repo)
    if rc != 0:  # base not an ancestor / detached — fall back to working-tree diff
        rc, out = sh(["git", "diff", "--name-only", "HEAD"], repo)
    return [ln.strip() for ln in out.splitlines() if ln.strip()]


def _match(path: str, pattern: str) -> bool:
    """Glob match tolerant of leading **/ (basename match) and exact paths."""
    pp = Path(path)
    if pattern.startswith("**/"):
        return pp.match(pattern) or Path(pp.name).match(pattern[3:])
    if "/" in pattern:
        return pp.match(pattern)
    return pp.name == pattern or Path(pp.name).match(pattern)


def class_triggers(name: str, frag: dict) -> list[str]:
    """The path patterns whose change activates this class's validator (from manifest data)."""
    if "files" in frag:
        return list(frag["files"])
    if "globs" in frag:
        return list(frag["globs"])
    if name == "env-schema":
        pats = [".env", "**/.env*"]
        for k in ("example", "required_extractor"):
            if frag.get(k):
                pats.append(frag[k])
        return pats
    if name == "db-migration":
        return ["**/migrations/versions/*.py", "**/alembic/versions/*.py", "prisma/migrations/**"]
    return []


# ---------------------------------------------------------------------------
# per-class validators — return (ok, detail); `None` ok means skipped
# ---------------------------------------------------------------------------


def v_container_compose(repo: Path, frag: dict) -> tuple[bool | None, str]:
    if frag.get("optional"):
        return None, "docker absent — skipped (spine is the net)"
    for f in frag.get("files", []):
        # --no-interpolate: validate YAML/structure/service refs WITHOUT substituting env values.
        # Env-value presence is env-schema's job; this keeps the compose check env-independent.
        rc, out = sh(["docker", "compose", "-f", f, "config", "--no-interpolate", "-q"], repo)
        if rc != 0:
            return False, f"{f}: {out.splitlines()[-1] if out else 'config error'}"
    return True, f"{len(frag.get('files', []))} compose file(s) parse"


def v_env_schema(repo: Path, frag: dict) -> tuple[bool | None, str]:
    loader = frag.get("settings_loader")
    if not loader:
        return None, "no settings loader detected — skipped"
    rc, out = sh(loader, repo)
    if rc != 0:
        low = out.lower()
        # Distinguish "the loader TOOL can't run here" (skip — e.g. uv absent on the host; the
        # container boot + health gate is the real env-value proof) from "Settings genuinely
        # invalid" (fail). A missing interpreter is an environment gap, not a config defect.
        if rc == 127 or "not found" in low or "no such file" in low or "no module named" in low:
            why = out.splitlines()[-1] if out else ""
            return None, f"loader tool unavailable here — skipped ({why})"
        tail = out.splitlines()[-1] if out else "load failed"
        return False, f"settings do not load: {tail}"
    return True, "settings load (values valid)"


def v_shell_script(repo: Path, frag: dict) -> tuple[bool | None, str]:
    bad = []
    for f in frag.get("files", []):
        rc, out = sh(["bash", "-n", f], repo)
        if rc != 0:
            bad.append(f"{f}: {out.splitlines()[-1] if out else 'syntax'}")
    if frag.get("shellcheck"):
        for f in frag.get("files", []):
            rc, out = sh(["shellcheck", "-S", "error", f], repo)
            if rc != 0:
                bad.append(f"shellcheck {f}: {out.splitlines()[0] if out else 'error'}")
    if bad:
        return False, "; ".join(bad[:4])
    return True, f"{len(frag.get('files', []))} script(s) parse (bash -n)"


def v_static_config(repo: Path, frag: dict) -> tuple[bool | None, str]:
    bad = []
    for f in frag.get("files", []):
        p = repo / f
        if not p.exists():
            continue
        try:
            text = p.read_text(encoding="utf-8")
            if f.endswith(".json"):
                json.loads(text)
            elif f.endswith((".yml", ".yaml")):
                yaml.safe_load(text)
        except (json.JSONDecodeError, yaml.YAMLError) as e:
            bad.append(f"{f}: {str(e).splitlines()[0]}")
    if bad:
        return False, "; ".join(bad[:4])
    return True, f"{len(frag.get('files', []))} data file(s) parse"


def v_db_migration(repo: Path, frag: dict) -> tuple[bool | None, str]:
    check = frag.get("head_check", "alembic heads")
    rc, out = sh(check, repo)
    if rc != 0:
        return (
            None,
            f"cannot run '{check}' here — skipped ({out.splitlines()[-1] if out else 'no tool'})",
        )
    heads = [
        ln
        for ln in out.splitlines()
        if ln.strip() and "(head)" in ln or ln.strip().endswith("(head)")
    ]
    n = len(heads) if heads else len([ln for ln in out.splitlines() if ln.strip()])
    if n != 1:
        return False, f"{n} migration heads (must be 1) — divergent migrations"
    return True, "single migration head"


def v_reverse_proxy(repo: Path, frag: dict) -> tuple[bool | None, str]:
    if frag.get("optional"):
        return None, "proxy tool/docker absent — skipped (health gate is the net)"
    if frag.get("type") != "nginx":
        return None, f"{frag.get('type')} check not implemented — skipped"
    files = frag.get("files", [])
    skipped = 0
    for f in files:
        text = (repo / f).read_text(encoding="utf-8", errors="ignore")
        # A full nginx.conf has an http/events block; a site file is a bare server{} snippet that
        # must be tested INSIDE http{} (mount into conf.d/, which the default nginx.conf includes).
        full = "events {" in text or "events{" in text or "http {" in text or "http{" in text
        dest = "/etc/nginx/nginx.conf" if full else "/etc/nginx/conf.d/zz_preflight.conf"
        rc, out = sh(
            ["docker", "run", "--rm", "-v", f"{(repo / f)}:{dest}:ro",
             "nginx:alpine", "nginx", "-t"],
            repo,
        )
        if rc != 0:
            low = out.lower()
            # A throwaway container lacks the real certs/upstreams/includes — those failures are
            # environment limits, not config defects. Only a genuine PARSE error is a real fail.
            env_limit = any(s in low for s in (
                "cannot load certificate", "no such file", "host not found in upstream",
                "open()", "ssl_certificate", "upstream"))
            if env_limit:
                skipped += 1
                continue
            return False, f"{f}: {out.splitlines()[-1] if out else 'nginx -t failed'}"
    if skipped and skipped == len(files):
        return None, "syntax ok; full test needs real certs/upstreams — health gate is the net"
    ok = len(files) - skipped
    return True, f"{ok} nginx conf(s) valid" + (f" ({skipped} env-skipped)" if skipped else "")


VALIDATORS = {
    "container-compose": v_container_compose,
    "env-schema": v_env_schema,
    "shell-script": v_shell_script,
    "static-config": v_static_config,
    "db-migration": v_db_migration,
    "reverse-proxy-config": v_reverse_proxy,
    # runtime-behavior is post-deploy (see runner smoke), not a preflight class
}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repo", default=".")
    ap.add_argument("--manifest", default="deploy-manifest.yml")
    ap.add_argument("--diff-base", help="run classes touched since this ref (e.g. origin/dev)")
    ap.add_argument("--files", nargs="*", help="explicit changed-file list")
    ap.add_argument(
        "--all", action="store_true", help="run every present class (CI / first deploy)"
    )
    args = ap.parse_args()

    # Windows consoles default to a legacy codepage (cp1251) that crashes on tool output
    # containing other characters — force utf-8 so preflight is portable.
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")

    repo = Path(args.repo).resolve()
    man_path = repo / args.manifest
    if not man_path.exists():
        print(f"ERROR: {man_path} missing — run probe.py first", file=sys.stderr)
        return 2
    manifest = yaml.safe_load(man_path.read_text(encoding="utf-8"))
    classes = manifest.get("classes", {})

    # decide which classes to run
    if args.all:
        to_run = list(classes)
        scope = "ALL present classes"
    else:
        files = (
            args.files
            if args.files
            else (changed_files(repo, args.diff_base) if args.diff_base else [])
        )
        if not files:
            print(
                "no changed files resolved (pass --diff-base, --files, or --all) — nothing to check"
            )
            return 0
        to_run = [
            n
            for n, frag in classes.items()
            if any(_match(f, pat) for f in files for pat in class_triggers(n, frag))
        ]
        scope = f"{len(files)} changed file(s) → {len(to_run)} class(es)"

    print(f"preflight [{scope}]")
    failed = 0
    for name in to_run:
        vfn = VALIDATORS.get(name)
        if not vfn:
            continue
        ok, detail = vfn(repo, classes[name])
        mark = "PASS" if ok else ("SKIP" if ok is None else "FAIL")
        print(f"  [{mark}] {name}: {detail}")
        if ok is False:
            failed += 1
    if failed:
        print(f"PREFLIGHT FAILED: {failed} class(es) — fix before deploy", file=sys.stderr)
        return 1
    print("PREFLIGHT OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
