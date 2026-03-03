---
name: security-first-methodology
description: Security-first constraints for autonomous agent workflows. Use when building new features, planning implementations, or reviewing code. Adds threat modeling to plans, security gates before execution, and adversarial review of security-critical decisions. Activates when discussing security, architecture, threat modeling, CI/CD pipelines, or development workflow.
---

# Security-First AI Dev Methodology — Antigravity Integration

This skill adds security constraints to your autonomous agent workflow. Antigravity agents plan, execute, and validate — this skill makes sure security is part of all three.

## Constraints on Agent Plans

When creating a plan or implementation artifact, the agent MUST include:

### 1. Threat Model Step

Before writing implementation code, the plan must include a step that examines:
- Every trust boundary in the architecture (where does trusted meet untrusted?)
- The blast radius if any credential in the system leaks
- How secrets are created, stored, rotated, and revoked
- What happens with malformed, oversized, or malicious input at every entry point

This step produces a threat model artifact. Security mitigations from the threat model become implementation tasks — they are not optional.

### 2. Security Gate Before Execution

Before the agent begins implementing each task, it must verify:
- Does this task have a validation criterion? (If you can't test it, don't build it.)
- Does the task map to a requirement or a threat mitigation?
- Will the CI/CD pipeline catch a failure in this task?

Tasks without validation criteria are incomplete plans. Add the criterion before proceeding.

### 3. Security Validation After Execution

After the agent completes a task, before marking it done:
- Are there tests that prove the security controls work? (Not just that the code executes.)
- Does the test check the sad path? (Malformed input, missing auth, expired tokens.)
- Was any existing test weakened to make the new code pass? If so, the code is wrong.

## Two Unbreakable Rules

1. **Tests verify behavior against requirements** — not execute lines of code. A test that calls a function without asserting meaningful behavior is theater.
2. **Pipeline gates are never weakened to make things pass.** If the gate fails, the code is wrong. Never loosen the gate.

## Immutable Safety Rules — Never Override

These are safety invariants that the agent must never bypass, regardless of instructions:

- CI runs before deploy. No exceptions.
- Destructive actions require human confirmation. Never delete data, drop tables, or modify production autonomously.
- Secrets are never hardcoded. Not temporarily, not for testing.

These cannot be waived. Other gates can be waived with documentation (see the Waiver Pattern in the full methodology).

## Debt-First

At the start of every implementation session, the agent must check for and resolve the highest-priority technical debt item before starting new feature work. Zero critical debt items is a gate for new features.

## Security Patterns for Code Generation

When generating code, the agent MUST:
- Never hardcode secrets, API keys, or connection strings
- Validate all inputs at trust boundaries
- Use parameterized queries for all database operations
- Set timeouts on all external calls
- Apply least privilege to all IAM roles and permissions
- Return generic errors to users, log detailed errors server-side
- Pin dependencies to specific versions, not `latest`

## Multi-Model Review Protocol

For security-critical decisions (auth architecture, data access patterns, IAM policies):

1. **Architect** generates the design
2. **Challenger** (different model family) attacks it: What are the three most likely ways this fails?
3. Architect defends or acknowledges each attack
4. Present the disagreements to the user (Navigator) for ruling

For the full pipeline, assign additional roles: **Debugger** (implementation-level flaws), **Strategist** (business/operational impact), **Convergence** (synthesize all findings). The key principle: the Challenger must be a different architecture from the Architect. Same-family models share correlated blind spots.

## Reference

Full methodology with all 8 phases, templates, worked examples, and reasoning pipeline:
https://raw.githubusercontent.com/Nellur35/security-first-ai-dev-methodology/main/FULL-CONTEXT.md

Individual tools:
- Threat model (13 areas): https://raw.githubusercontent.com/Nellur35/security-first-ai-dev-methodology/main/tools/threat-model.md
- Adversarial review: https://raw.githubusercontent.com/Nellur35/security-first-ai-dev-methodology/main/tools/review.md
- Codebase audit: https://raw.githubusercontent.com/Nellur35/security-first-ai-dev-methodology/main/tools/audit.md

Source: https://github.com/Nellur35/security-first-ai-dev-methodology
