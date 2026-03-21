---
name: guide
description: >
  Explains what the Permission Slip Effect repo is, what's available,
  and which skill or tool to use for a given situation. Activates when
  the user asks what this is, how to use the methodology, what skills
  are available, where to start, what the repo does, or any discovery
  question about the project. Also activates when the user seems
  unfamiliar with the methodology or asks "what can you do?"
allowed-tools:
  - Read
  - Glob
---

# Permission Slip Effect — Guide

You are answering a discovery question about this project. The user wants to know what's here and what to use. Be direct — route them, don't lecture them.

## What This Is

Three things, same principle:

1. **Reasoning pipeline** — chain frameworks (First Principles → Pre-Mortem → Adversarial → Game Theory) on one problem. Forces the model past the statistically safe answer. Works with one model. Better with several.
2. **Standalone tools** — single-file prompts. Paste into any AI conversation. No setup.
3. **Security-first methodology** — 8-phase dev process. Problem definition through production feedback. Gate checks between phases. Templates for every artifact.

They're the same idea at different scales. The pipeline manages reasoning context. The methodology manages project context. The tools work at the artifact level.

## Route the User

Match what they want to do → tell them exactly where to go.

### "I want to review something right now"

Paste one of these into any AI conversation:

| Need | Tool |
|------|------|
| Attack any artifact | `tools/review.md` |
| Threat model from architecture | `tools/threat-model.md` |
| Scan an existing codebase | `tools/audit.md` |
| Check if a phase is done | `tools/gate-check.md` |
| Define a problem properly | `tools/intake.md` |
| Session retrospective | `tools/session-retro.md` |

No installation. No CLI. One model, one prompt, one artifact.

### "I want to analyze a complex decision"

Use the reasoning pipeline: `reasoning-pipeline.md`

Or use the CLI for multi-model analysis:
```bash
python pipeline.py reason "Your question here"
python pipeline.py review artifact.md
```

Available pipelines: `light` (3 stages), `standard` (5 stages), `stakeholder`, `systems`, `review`. See `pipeline/README.md` for details.

### "I'm starting a new project"

Use the full methodology: `methodology/METHODOLOGY.md`

Phases 1-5 are sequential. Phase 6+ is iterative. Start with Phase 1 — don't skip it.

Quick start: run `/intake` (if skills are installed) or paste `tools/intake.md` into your AI conversation.

### "I want to install this in my editor"

| Platform | Instructions |
|----------|-------------|
| Claude Code | `integrations/claude-code/README.md` |
| Kiro | `integrations/kiro/README.md` |
| Cursor | `integrations/cursor/README.md` |
| Antigravity | `integrations/antigravity/README.md` |

Or give any AI tool the single-file version:
```
Read https://raw.githubusercontent.com/Nellur35/permission-slip-effect/main/FULL-CONTEXT.md
```

### "I have an existing codebase — where do I start?"

Run `/audit` (or paste `tools/audit.md`). It scans your codebase, maps what exists against the methodology, and tells you where the gaps are. Start fixing from the audit output.

### "I want multi-agent / multiple AI windows"

Read `multi-agent/MULTI-AGENT.md`. But don't start there — start with Tier 0 (single agent + diary). Multi-agent is earned through evidence, not configured upfront. The diary tells you when to escalate.

### "I just want the worked example"

`methodology/examples/url-shortener/` — a URL shortener built through all 8 phases with real artifacts at each step.

### "What are the skills I have installed?"

If Claude Code skills are present:

| Command | What it does |
|---------|-------------|
| `/intake` | Phase 1 — interactive problem definition |
| `/threat-model` | Phase 4 — threat model from architecture |
| `/review` | Any phase — adversarial review |
| `/gate-check` | Any phase — verify exit criteria |
| `/audit` | Any time — scan existing codebase |
| `/retro` | Session end — structured feedback loop |

The methodology orchestrator routes automatically based on phase.

## What NOT to Use This For

- Simple tasks. If "think step by step" gets you the answer, the pipeline is overkill.
- Tasks where being wrong is cheap. The methodology adds overhead. It pays for itself when mistakes are expensive.
- Solo throwaway scripts. Use the tools (review, audit) standalone. Don't run the full 8-phase methodology on a script you'll delete tomorrow.

## Key Concepts (If They Ask)

| Term | One-line explanation |
|------|---------------------|
| Permission Slip | Structured context that makes the model produce what RLHF training suppresses |
| Phase 0 | Decomposition before analysis — facts, constraints, stakeholders, unknowns |
| SPLIT | Reviewers hit contradictory conclusions — highest-value output, human decides |
| De-anchoring | Forcing the model past the prompt anchor through framework rotation |
| Bootstrap gap | The thing that builds the artifact can't be the thing that reviews it |
| Diary | Auto-collected project log — feeds emergence analysis and retro |
| Emergence | Multi-agent roles earned through diary data, not assigned upfront |

Don't explain these unless asked. Route first, educate second.
