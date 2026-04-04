# Project Context

## Purpose
This file provides high-level project overview for AI agents. Helps agents understand WHAT we're building and WHY.

---

## Project Overview

**Name:** AI-First Development Methodology (Claude Code)

**Description:** Structured spec-driven development framework for Claude Code — 31 methodology skills, agent validators, and templates that form a complete pipeline from requirements to deployed code.

Solo developer tool: the owner uses it daily to build client and personal projects. Every feature goes through a mandatory pipeline: User Spec → Tech Spec → Tasks → Code → Review → Documentation.

---

## Target Audience

**Primary users:** Viktor (solo developer, methodology owner)

**Use case:** Building client and personal projects with Claude Code. The methodology ensures quality and context persistence across multi-session AI-assisted development.

---

## Core Problem

Context is lost between AI sessions, spec discussions get skipped, and code quality degrades without human review at every step. The methodology solves this by enforcing a spec-driven pipeline with automated validators and a persistent knowledge system — so every session starts with full context, and no stage proceeds without explicit approval.

---

## Key Features

- **Spec pipeline** — mandatory User Spec → Tech Spec → Tasks → Code hierarchy with 6 blocking gates; nothing proceeds without user approval
- **Sketch Mode** — lightweight path for prototyping: quick interview → sketch.md → code in one session, then decide: develop or discard
- **Automated validators** — 2–5 parallel validators per pipeline stage (quality, adequacy, security, completeness, reality-check)
- **Unified knowledge system** — triad-based `reasoning-patterns.md` buffer that accumulates lessons from each feature and feeds them back into skills
- **Codex adaptation** — parallel version for OpenAI Codex with same methodology but different platform integration (`.agents/` paths, `spawn_agent` API)

---

## Skill Classification

The repo contains skills from multiple tracks. Only **core methodology** skills are actively maintained and synced to Codex:

**Core methodology** (26 skills + sketch):
- Planning: `user-spec-planning`, `tech-spec-planning`, `task-decomposition`, `project-planning`, `new-user-spec`, `new-tech-spec`, `decompose-tech-spec`
- Execution: `code-writing`, `feature-execution`, `do-feature`, `do-task`, `done`, `write-code`
- Quality: `code-reviewing`, `security-auditor`, `test-master`, `prompt-master`
- QA/Deploy: `pre-deploy-qa`, `post-deploy-qa`, `deploy-pipeline`, `infrastructure-setup`
- Meta: `methodology`, `quick-learning`, `documentation-writing`, `skill-master`, `skill-test-designer`, `skill-tester`, `init-project`, `init-project-knowledge`
- Sketch: `sketch` *(new — lightweight prototyping mode)*

**Separate pipelines** (in this repo but maintained independently):
- `design-*` (9 skills) — design pipeline, separate project track
- `moneymaker-*` (5 skills) — freelance project management pipeline: setup → new → add → expand → finalize. Stores data at `~/.moneymaker/`, independent of methodology storage. Security: billing fields masked in output, `chmod 600 config.yml`, project name validated `^[a-zA-Z0-9_-]+$`, LLM inputs wrapped in isolation tags.

---

## Out of Scope

- Codex repo (`ai-dev-methodology-codex`) — a derived artifact; maintained separately, not the source of truth
- Multi-user / team usage — methodology is designed for solo developer workflow
- Web UI / dashboard — no interface planned; everything runs via Claude Code CLI
