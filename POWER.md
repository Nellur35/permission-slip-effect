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

1. **Threat model phase** — After design.md, before tasks.md. Kiro's design phase produces architecture; this power makes you attack it before writing code.
2. **Gate questions at every transition** — Exit criteria that must be satisfied before moving to the next spec phase. Not "does this look good?" but "can I answer these specific questions with evidence?"
3. **Security-aware requirements patterns** — Scope exclusions, explicit non-goals, and testability checks that Kiro's EARS-notation user stories don't naturally produce.
4. **Adversarial cross-model review** — Use a different model to attack security-critical design decisions. Kiro supports multiple models; use that.
5. **Reasoning pipeline** — For complex architectural or organizational decisions where Kiro's design phase needs deeper analysis.

## How to Use With Kiro Specs

### During Requirements (requirements.md)

After Kiro generates user stories, check:
- Is every requirement testable? (Not "the system should be secure" — what does secure mean, specifically?)
- What is explicitly out of scope? Add a "Non-goals" section.
- What are the trust boundaries? Who talks to whom?

### During Design (design.md)

After Kiro generates the architecture, load the threat modeling steering file:
- Examine every trust boundary in the design
- For each boundary: what's the worst thing an adversary can do?
- Are secrets hardcoded anywhere? How are they rotated?
- What's the IAM blast radius if a credential leaks?

### Between Design and Tasks — The Missing Phase

**Before clicking "Move to implementation plan"**, create a threat model:

```
Load the threat-model steering file and run it against design.md
```

This produces a threat_model.md alongside Kiro's existing spec files. The threat model should inform which tasks exist — security mitigations become tasks, not afterthoughts.

### During Tasks (tasks.md)

**Phase 4 establishes the threat model. Every subsequent phase applies it.** Security review is not a phase you pass through and leave behind — it is embedded in everything after.

After Kiro generates the task list:
- Does every security mitigation from the threat model map to a task?
- Which CI/CD gate validates each task?
- Are there tasks without validation criteria?

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

## When to Load Steering Files

- Adding security requirements to Kiro specs → `security-requirements.md`
- Threat modeling after design phase → `threat-model.md`
- Reviewing any artifact adversarially → `review.md`
- Auditing an existing codebase → `audit.md`
- Checking phase exit criteria → `gate-check.md`
- Complex architectural decisions → `reasoning-pipeline.md`

## Source

Full methodology, templates, worked examples, and empirical testing:
https://github.com/Nellur35/security-first-ai-dev-methodology
