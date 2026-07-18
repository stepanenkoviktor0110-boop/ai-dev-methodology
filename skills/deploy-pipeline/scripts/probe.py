#!/usr/bin/env python
"""deploy-safety PROBE — detect a repo's deploy surface and emit deploy-manifest.yml.

Universal across projects: it runs each artifact-class detector from the registry
(references/artifact-registry.md) against an arbitrary repo and writes a project-local
manifest the runner consumes. Logic is here (once); the manifest is the only project-specific
output. Re-run when the deploy surface changes.

    python probe.py --repo /path/to/repo [--out deploy-manifest.yml] [--force]

Emits `optional: true` for a class whose external validator tool is absent (the runner skips
it with a notice; the atomic-switch spine is the net). NEVER reads secret VALUES — env handling
is by key NAME only (RULE: never leak secrets).
"""

from __future__ import annotations

import argparse
import ast
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# small helpers
# ---------------------------------------------------------------------------

IGNORE_DIRS = {".git", "node_modules", ".venv", "venv", "dist", "build", "__pycache__", ".mypy_cache"}


def _walk(root: Path, patterns: list[str]) -> list[str]:
    """Repo-relative paths matching any glob, skipping vendor/build dirs. Deterministic order."""
    hits: set[str] = set()
    for pat in patterns:
        for p in root.glob(pat):
            if not p.is_file():
                continue
            if any(part in IGNORE_DIRS for part in p.relative_to(root).parts):
                continue
            hits.add(p.relative_to(root).as_posix())
    return sorted(hits)


def _has_tool(name: str) -> bool:
    return shutil.which(name) is not None


def _docker() -> bool:
    return _has_tool("docker")


# ---------------------------------------------------------------------------
# per-class detectors — each returns a manifest fragment or None if the class is absent
# ---------------------------------------------------------------------------


def detect_container_compose(root: Path) -> dict | None:
    files = _walk(root, ["docker-compose*.yml", "docker-compose*.yaml",
                         "compose*.yml", "compose*.yaml",
                         "deploy/docker-compose*.yml", "deploy/compose*.yml"])
    if not files:
        return None
    return {"files": files, "optional": not _docker()}


def detect_env_schema(root: Path) -> dict | None:
    example = _walk(root, [".env.example", "*.env.example", "deploy/*.env.example"])
    # find a pydantic-style Settings module (universal-ish heuristic; extend per stack later)
    loader = None
    required_extractor = None
    for cand in _walk(root, ["**/config.py", "**/settings.py"]):
        text = (root / cand).read_text(encoding="utf-8", errors="ignore")
        if re.search(r"class\s+Settings\b", text) and "BaseSettings" in text:
            module = cand[:-3].replace("/", ".")
            # uv projects need `uv run python` (bare `python` is a stub on Windows / wrong venv)
            py = "uv run python" if (root / "uv.lock").exists() else "python"
            loader = f'{py} -c "import {module} as m; m.Settings()"'
            required_extractor = cand  # runner reuses check-deploy-env.py AST approach on this file
            break
    if not (example or loader):
        return None
    return {
        "example": example[0] if example else None,
        "settings_loader": loader,
        "required_extractor": required_extractor,
        "target_env": "ssh:<host>:/path/to/.env",  # probe leaves a fillable default
    }


def detect_shell_script(root: Path) -> dict | None:
    files = set(_walk(root, ["deploy/*.sh", "docker/*.sh", "scripts/*.sh", "*.sh", "**/*entrypoint*.sh"]))
    # also catch shebang'd files without .sh extension in deploy/scripts dirs
    for cand in _walk(root, ["deploy/*", "scripts/*"]):
        p = root / cand
        try:
            first = p.open("r", encoding="utf-8", errors="ignore").readline()
        except OSError:
            continue
        if re.match(r"#!.*\bsh\b", first):
            files.add(cand)
    if not files:
        return None
    return {"files": sorted(files), "shellcheck": _has_tool("shellcheck")}


def detect_static_config(root: Path) -> dict | None:
    globs = ["**/seed/**/*.json", "**/seed/**/*.yml", "**/seed/**/*.yaml",
             "**/fixtures/**/*.json", "**/seeds/**/*.json"]
    files = _walk(root, globs)
    if not files:
        return None
    return {"globs": sorted({g for g in globs}), "files": files}


def detect_db_migration(root: Path) -> dict | None:
    if _walk(root, ["**/migrations/versions/*.py", "**/alembic/versions/*.py"]):
        return {"tool": "alembic", "head_check": "alembic heads"}
    if _walk(root, ["prisma/migrations/**/*.sql"]):
        return {"tool": "prisma", "head_check": "prisma migrate status"}
    return None


def detect_reverse_proxy(root: Path) -> dict | None:
    nginx = _walk(root, ["deploy/nginx/*.conf", "nginx.conf", "**/nginx/*.conf"])
    if nginx:
        return {"type": "nginx", "files": nginx, "optional": not _docker()}
    caddy = _walk(root, ["Caddyfile", "**/Caddyfile"])
    if caddy:
        return {"type": "caddy", "files": caddy, "optional": not _has_tool("caddy")}
    return None


def detect_runtime_behavior(root: Path) -> dict | None:
    """Services with a health endpoint + best-effort auto-derived anchor tokens.

    Anchors (a substring proving the right data/feed is bound) are auto-derived from seed data
    where possible (registry decision: auto-derive first, interview only as fallback). We surface
    high-signal candidate tokens; each check is marked `derived: true` for a quick human glance.
    """
    # services + health URLs are best pulled from compose; here we emit a skeleton the runner/owner
    # confirms. Auto-derive candidate anchor tokens from seed JSON (prices/SKUs are stable & unique).
    candidates: list[str] = []
    for f in _walk(root, ["**/seed/**/*.json"])[:20]:
        try:
            data = json.loads((root / f).read_text(encoding="utf-8", errors="ignore"))
        except (json.JSONDecodeError, OSError):
            continue
        for tok in _anchor_tokens(data):
            candidates.append(tok)
            if len(candidates) >= 5:
                break
        if len(candidates) >= 5:
            break
    return {
        "checks": [
            {
                "service": "<service>",
                "url": "https://<host>/answer",
                "request": "<a question whose correct answer needs the right feed>",
                "expect_substring": candidates[0] if candidates else "<token proving right data>",
                "derived": bool(candidates),
            }
        ],
        "anchor_candidates": candidates,
    }


def _anchor_tokens(obj: object, _depth: int = 0) -> list[str]:
    """Pull stable, high-signal string/number tokens (SKU/price/id) from nested seed data."""
    out: list[str] = []
    if _depth > 4:
        return out
    if isinstance(obj, dict):
        for k, v in obj.items():
            if re.search(r"(price|sku|article|артикул|цена|id|code)", str(k), re.I) and isinstance(v, (str, int)):
                s = str(v).strip()
                if s and len(s) >= 3:
                    out.append(s)
            out.extend(_anchor_tokens(v, _depth + 1))
    elif isinstance(obj, list):
        for v in obj[:10]:
            out.extend(_anchor_tokens(v, _depth + 1))
    return out


DETECTORS = {
    "container-compose": detect_container_compose,
    "env-schema": detect_env_schema,
    "shell-script": detect_shell_script,
    "static-config": detect_static_config,
    "db-migration": detect_db_migration,
    "reverse-proxy-config": detect_reverse_proxy,
    "runtime-behavior": detect_runtime_behavior,
}


# ---------------------------------------------------------------------------
# manifest emission (YAML written by hand to avoid a pyyaml dependency)
# ---------------------------------------------------------------------------


def _yaml(obj: object, indent: int = 0) -> str:
    pad = "  " * indent
    if isinstance(obj, dict):
        if not obj:
            return " {}\n"
        lines = []
        for k, v in obj.items():
            if isinstance(v, (dict, list)):
                if not v:  # empty collection → inline [] / {} (not a quoted scalar)
                    lines.append(f"{pad}{k}: {'[]' if isinstance(v, list) else '{}'}")
                else:
                    lines.append(f"{pad}{k}:")
                    lines.append(_yaml(v, indent + 1).rstrip("\n"))
            else:
                lines.append(f"{pad}{k}:{_scalar(v)}")
        return "\n".join(lines) + "\n"
    if isinstance(obj, list):
        if not obj:
            return " []\n"
        lines = []
        for item in obj:
            if isinstance(item, dict):
                body = _yaml(item, indent + 1).lstrip()
                lines.append(f"{pad}- {body.rstrip()}")
            else:
                lines.append(f"{pad}-{_scalar(item)}")
        return "\n".join(lines) + "\n"
    return f"{pad}{_scalar(obj)}\n"


def _scalar(v: object) -> str:
    if v is None:
        return " null"
    if isinstance(v, bool):
        return f" {str(v).lower()}"
    if isinstance(v, (int, float)):
        return f" {v}"
    s = str(v)
    if s == "" or re.search(r"[:#\{\}\[\]&*!|>'\"%@`]", s) or s != s.strip():
        return ' "' + s.replace('"', '\\"') + '"'
    return f" {s}"


def build_manifest(root: Path) -> dict:
    classes: dict[str, dict] = {}
    for name, fn in DETECTORS.items():
        frag = fn(root)
        if frag is not None:
            classes[name] = frag
    return {
        "version": 1,
        "note": "generated by deploy-pipeline/scripts/probe.py — edit params, re-run to refresh detection",
        "spine": {
            "health_poll_seconds": 3,
            "health_timeout_seconds": 120,
            "health_consecutive_ok": 2,
            "prev_tag": "prev",
            "backup_cmd": None,  # e.g. "/root/backup.sh" — invoked before build if set
            "services": [],      # fill: services to recreate atomically (probe cannot infer traffic topology)
        },
        "classes": classes,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--repo", required=True, help="repo root to probe")
    ap.add_argument("--out", default="deploy-manifest.yml", help="manifest path (relative to repo)")
    ap.add_argument("--force", action="store_true", help="overwrite an existing manifest")
    args = ap.parse_args()

    root = Path(args.repo).resolve()
    if not root.is_dir():
        print(f"ERROR: {root} is not a directory", file=sys.stderr)
        return 2
    out = root / args.out
    if out.exists() and not args.force:
        print(f"ERROR: {out} exists (use --force to overwrite)", file=sys.stderr)
        return 2

    manifest = build_manifest(root)
    header = "# deploy-manifest — generated by probe.py. Registry: deploy-pipeline/references/artifact-registry.md\n"
    out.write_text(header + _yaml(manifest), encoding="utf-8")

    present = list(manifest["classes"])
    optional = [c for c, f in manifest["classes"].items() if f.get("optional")]
    print(f"probed {root.name}: {len(present)} classes present: {', '.join(present) or '(none)'}")
    if optional:
        print(f"  optional (tool absent, will skip with notice): {', '.join(optional)}")
    print(f"wrote {out}")
    print("NEXT: fill spine.services + runtime-behavior.checks, then wire the runner.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
