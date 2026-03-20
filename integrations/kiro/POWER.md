---
name: "security-first-dev"
displayName: "Security-First AI Dev Methodology"
description: "Adds security phases to Kiro's spec-driven workflow. Threat modeling between design and tasks, gate questions at every phase transition, adversarial cross-model review, and structured security requirements patterns."
keywords: ["security", "threat model", "threat modeling", "devsecops", "secure", "vulnerability", "iam", "trust boundary", "blast radius", "adversarial review", "gate check", "pipeline", "ci/cd", "architecture review", "audit", "security review", "supply chain", "secrets", "owasp"]
---

# Security-First AI Dev Methodology — Kiro Integration

This power extends Kiro's spec-driven workflow (requirements → design → tasks) with security phases that spec-driven development doesn't cover.

## What This Adds to Kiro's Workflow

Kiro already handles requirements, design, and task planning well. This power fills the gaps:

1. **Threat model phase** — After design.md, before tasks.md. Kiro's design phase produces architecture; this power adds adversarial security analysis before any code is written.
2. **Gate questions at every transition** — Exit criteria that must be satisfied before moving to the next spec phase. Not "does this look good?" but "can I answer these specific questions with evidence?"
3. **Security-aware requirements patterns** — Scope exclusions, explicit non-goals, and testability checks that Kiro's EARS-notation user stories don't naturally produce.
4. **Adversarial cross-model review** — A different model attacks security-critical design decisions. Kiro supports multiple models; the power uses that.
5. **Reasoning pipeline** — For complex architectural or organizational decisions where Kiro's design phase needs deeper analysis.
6. **Automated pipeline CLI** — Run `python pipeline.py review design.md` for multi-model adversarial review from the command line.

## How to Use With Kiro Specs

### During Requirements (requirements.md)

After Kiro generates user stories, load the security-requirements steering file:

```
Load the security-requirements steering file and apply it to requirements.md
```

Kiro will add testability checks, explicit scope exclusions, trust boundary identification, and non-goals. Review the additions — confirm what's in scope and what's not.

### During Design (design.md)

After Kiro generates the architecture, load the threat modeling steering file:

```
Load the threat-model steering file and run it against design.md
```

Kiro will examine every trust boundary, map IAM blast radius, check for hardcoded secrets, and analyze data flows. Review the findings — challenge anything that looks too optimistic.

### Between Design and Tasks — The Missing Phase

**Before clicking "Move to implementation plan"**, generate a threat model:

```
Load the threat-model steering file and produce threat_model.md from design.md
```

Kiro produces `threat_model.md` alongside the existing spec files. The threat model informs which tasks exist — security mitigations become tasks, not afterthoughts. Review the threat model before proceeding.

Or run from the command line for multi-model review:

```bash
python pipeline.py review design.md --cheap -o threat-review.json
```

### During Tasks (tasks.md)

**Phase 4 establishes the threat model. Every subsequent phase applies it.** Security review is not a phase you pass through and leave behind — it is embedded in everything after.

After Kiro generates the task list, load the gate-check steering file:

```
Load the gate-check steering file and verify tasks.md against threat_model.md
```

Kiro will check that every security mitigation maps to a task, every task has a validation criterion, and CI/CD gates cover the threat model findings. Review any gaps it identifies.

## The Pipeline CLI

For automated multi-model review without manual copy-paste between models:

```bash
# Adversarial review of any artifact
python pipeline.py review design.md

# Full reasoning pipeline on a complex decision
python pipeline.py reason --pipeline standard "Should we migrate auth to OAuth2?"

# Cheap mode — analysis on Haiku/Flash, convergence on Sonnet
python pipeline.py review architecture.md --cheap

# Skip confirmation for CI integration
python pipeline.py review threat_model.md --yes -o results.json
```

The pipeline automates the Architect → Challenger → Convergence flow. You run a command, the AI argues with itself, you read the JSON output. See `pipeline/README.md` for full documentation.

## Two Unbreakable Rules

1. Tests verify behavior against requirements — not execute lines of code.
2. Pipeline gates are never weakened to make things pass.

## Immutable Safety Rules — Never Waivable

These are load-bearing safety invariants. The Waiver Pattern does not apply to them:

- CI runs before deploy. No exceptions.
- Destructive actions require human confirmation.
- Secrets are never hardcoded. Not temporarily, not for testing.

Other gates can be waived with documentation. These cannot.

## Debt-First

At the start of every implementation session, check for and resolve the highest-priority technical debt item before new feature work. Zero critical debt items is a gate for new features.

## Artifact Currency

At the start of every session and at every phase transition: verify that upstream artifacts (requirements, architecture, threat model) still reflect current decisions. If any artifact contradicts what you're about to build, update it first. Stale artifacts poison every downstream phase silently.

## The Multi-Model Review

For security-critical design decisions, use different models in assigned roles:

| Role | Mandate |
|------|---------|
| Architect | Design the solution, defend structural decisions |
| Challenger | Attack every assumption, find failure modes (must be different model family) |
| Debugger | Find implementation-level flaws, race conditions, edge cases |
| Strategist | Evaluate business/operational impact, cost, timeline |
| Convergence | Synthesize all findings into final recommendation |

Kiro supports multiple models — use that. The minimum viable version:

1. Primary model (Architect) produces the design
2. Switch model (Challenger) — ask it to attack the design
3. Switch back (Architect) — defend or acknowledge
4. You (Navigator) rule on disagreements

The genuine disagreements between models are where the real signal lives.

## Session Feedback Loop

**Trigger:** When the session is ending or a task is completed, offer to run the feedback loop. If the navigator declines, respect that. If work was done, the offer happens — every time.

**Quick filter:** Did this session involve a decision with tradeoffs, something surprising, or a pattern you have seen before? If yes → full loop. If it was routine execution → one-line summary: "What happened. Anything surprising: [yes/no]. Lesson: [one line or none]." Append to `diary.md` and close.

**Full loop — three stages, strictly sequential:**

**1. Root Cause Analysis**
For each significant event this session:
- What happened? (factual, no judgment)
- What caused it? (5 Whys to structural root)
- What enabled the cause? (process, tooling, knowledge, environment — if this is a restatement of the event, go deeper)
- Where was the decision point?
- First time or recurring pattern? (check `diary.md` for history)

**2. Retrospective**
Read the RCA outputs. Answer — with equal rigor for successes and problems:
- What worked well and why? What structural condition to protect?
- What patterns are repeating — within this session and across previous sessions?
- Where did reality diverge from the plan?
- What do you understand now that you didn't before?
- Where did friction exist?

**3. Lessons Learned**
For each finding from the retrospective:
- Every lesson must be executable: "add check X to gate Y" — not "be more careful about X"
- If you cannot name a specific target file or rule, it is a strategic finding — log it and schedule it
- **Conflict check:** Before applying, does this lesson contradict an existing rule, gate, or constraint? If yes — do not apply, do not waive. Escalate to a Graph of Thoughts analysis against `diary.md`. Map the dependency structure of both the rule and the lesson. The resolution comes from the shared root, not from picking one.
- **Scope:** tactical (apply in under 2 minutes) or strategic (informs future planning)
- **Priority:** do now (tactical only) | next session | backlog
- **"Do now" tactical lessons get applied before the session ends.** Update the steering file, the power, the spec, or the methodology artifact immediately.

**Diary:** After each run (full or quick), append a diary entry to `diary.md` (the same diary used for agent emergence analysis): date, one-line description, key finding, lessons applied, strategic findings logged, any escalated conflicts. Do not create a separate file.

**Where lessons go:** Update the relevant steering file, power section, or methodology artifact directly. The lesson is not done until the target file is changed.

## When to Load Steering Files

- Adding security requirements to Kiro specs → `security-requirements.md`
- Threat modeling after design phase → `threat-model.md`
- Reviewing any artifact adversarially → `review.md`
- Auditing an existing codebase → `audit.md`
- Checking phase exit criteria → `gate-check.md`
- Complex architectural decisions → `reasoning-pipeline.md`
- Session feedback loop → `tools/session-retro.md`

## Source

Full methodology, templates, worked examples, and empirical testing:
https://github.com/Nellur35/permission-slip-effect
