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
- **40+ skills** — specialized AI agents for each pipeline stage (planning, coding, review, QA, documentation, retrospective)
- **Automated validators** — 2–5 parallel validators per pipeline stage (quality, adequacy, security, completeness, reality-check)
- **Unified knowledge system** — triad-based `reasoning-patterns.md` buffer that accumulates lessons from each feature and feeds them back into skills
- **Codex adaptation** — parallel version for OpenAI Codex with same methodology but different platform integration (`.agents/` paths, `spawn_agent` API)

---

## Out of Scope

- Design pipeline (`design-*` skills) — maintained as a separate project track, not part of core methodology
- Codex repo (`ai-dev-methodology-codex`) — a derived artifact; maintained separately, not the source of truth
- Multi-user / team usage — methodology is designed for solo developer workflow
- Web UI / dashboard — no interface planned; everything runs via Claude Code CLI
