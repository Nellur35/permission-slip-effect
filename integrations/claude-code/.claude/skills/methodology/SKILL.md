---
name: security-first-methodology
description: >
  Orchestrator for the security-first development methodology.
  Routes to the right skill for each phase. Activates when the
  user starts a new project, asks about methodology, or needs
  to know what phase to work on next.
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
---

# Security-First AI Dev Methodology

You are the engine. The user is the navigator and judge. Gate questions decide when a phase is complete. Phases 1-5 are sequential. Phase 6 onwards is iterative.

## Phase Routing

| Phase | What to Do | Skill |
|-------|-----------|-------|
| 1 — Problem | Define the real-world need | `/intake` |
| 2 — Requirements | Define what, not how. Use `templates/phase-2-requirements.md` | Direct work |
| 3 — Architecture | Design for testability. Offer `/review` when done | Direct work |
| 4 — Threat Model | Attack every trust boundary | `/threat-model` |
| 5 — CI/CD Pipeline | Pipeline defines done. Offer `/review` when done | Direct work |
| 6 — Tasks | Break into pipeline-validatable units | Direct work |
| 7 — Implementation | Code + tests. Use `/gate-check` per task | Direct work |
| 8 — Production | Feed failures back into the pipeline | Direct work |

## Available at Any Phase

| Need | Skill |
|------|-------|
| Check exit criteria before moving on | `/gate-check` |
| Adversarial review of any artifact | `/review` |
| Scan an existing codebase or CI/CD | `/audit` |

## Context Handoff

| Phase | Handoff Artifact |
|-------|-----------------|
| 1 -> 2 | `problem_statement.md` or `reconstruction_assessment.md` |
| 2 -> 3 | `requirements.md` |
| 3 -> 4 | `architecture.md` |
| 4 -> 5 | `threat_model.md` |
| 5 -> 6 | Pipeline config + dummy product + `requirements.md` + `threat_model.md` |
| 6 -> 7 | `tasks.md` |
| 7 -> 8 | Working code + test results |

If it's not in the output file, it doesn't carry forward.

## Phase Re-entry

Implementation will reveal upstream flaws. That's the process working. Identify which phase owns the flaw, re-run it with the current output + the finding, propagate changes forward.

## Two Unbreakable Rules

1. Tests verify behavior against requirements -- not execute lines of code.
2. Pipeline gates are never weakened to make things pass.

## Full Reference

See `METHODOLOGY.md` for rationale, worked examples, the reasoning pipeline, and the multi-model review system.

## Gotchas

**Tries to run multiple phases in one session.** The orchestrator routes to the right skill per phase, but it doesn't enforce "one phase per session." Under navigator pressure ("let's get through Phases 1-3 today"), the model compresses phases, skips gate checks between them, and produces artifacts that haven't been reviewed. Each phase transition should include a gate check. If the navigator wants speed, the answer is parallel sessions (Tier 2), not compressed phases.

**Routes to direct work when a skill exists.** Phases 2, 3, 5, 6, 7, 8 are listed as "Direct work" in the routing table. But `/review` should be offered at the end of every phase, and `/gate-check` should be offered at every transition. The model sometimes does Phase 3 → Phase 4 without offering either. The routing table shows what skill *runs the phase* — it doesn't show the skills that *close the phase*.

**Loses phase context in long sessions.** After 40+ turns, the model forgets which phase it's in and starts mixing phase concerns. Implementation decisions appear in Phase 2 discussions. Architecture details leak into Phase 1. The phase routing table in the orchestrator should be re-read at every phase transition, not just at session start.

**Doesn't enforce the handoff artifact.** The skill says "if it's not in the output file, it doesn't carry forward." But the model frequently carries context from the conversation that isn't in the artifact. Phase 3 discussions influence Phase 4 work even when they weren't captured in `architecture.md`. The discipline is: re-read the artifact at the start of each phase. If it's not in the file, it doesn't exist.
