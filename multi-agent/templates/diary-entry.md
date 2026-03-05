# Project Diary — Entry Format

**Written by:** the AI, automatically. The steering file instructs the AI to append an entry after each meaningful change. You don't write, edit, or manage this file.

**Location:** `diary.md` at project root (configurable via steering).

**Quality:** Good enough, not perfect. Pattern analysis tolerates noise.

---

## Entry Format

```markdown
### [SESSION-ID] YYYY-MM-DD HH:MM — Brief title

- **Phase:** 1-8 or cross-phase
- **Concern:** security | architecture | correctness | performance | debt | testing | infrastructure | knowledge
- **Action:** created | modified | refactored | fixed | reviewed | deferred | reverted
- **Files:** file1.ts, file2.ts
- **What:** 1-2 sentences — what changed.
- **Why:** 1-2 sentences — the decision or trigger.
- **Deferred:** What was punted, or "none"
```

Every field is factual and verifiable from the diff. The AI isn't reflecting — it's logging what it just did.

---

## Rules for the AI

1. **Write one entry per meaningful change.** A meaningful change is anything that modifies code, documentation, configuration, or project decisions. Don't log file formatting or typo fixes.

2. **Write the entry immediately after the change.** Don't batch entries at session end — context is freshest right after the action.

3. **Concern is the most important field.** This is what pattern analysis clusters on. Pick the primary concern that drove the change. If genuinely split, pick the one that consumed more navigator attention.

4. **Deferred is the second most important field.** Deferred items accumulate into patterns. Every time you punt something, record what and why. This is where agent roles often emerge — from the pile of things that keep getting deferred.

5. **Just log what happened.** Don't editorialize, don't assess quality, don't rate your own confidence. The entry should be reconstructable from the git diff plus a one-line explanation of why.

6. **Use markers when you notice patterns:**
   - `[RECURRING]` — You've seen this type of change before in recent entries
   - `[PATTERN]` — This connects to specific previous entries (reference their IDs)
   - `[BOTTLENECK]` — This consumed disproportionate time relative to its complexity

   These are optional. The analysis pipeline finds patterns regardless. But markers accelerate detection.

7. **Session ID format:** Use whatever the platform provides. If none, use a simple incrementing counter or date-based ID (e.g., `S001`, `S002` or `0315a`, `0315b`).

---

## Example Diary

```markdown
### [S012] 2026-03-15 10:30 — Add rate limiting to API gateway

- **Phase:** 4
- **Concern:** security
- **Action:** created
- **Files:** src/middleware/rate-limiter.ts, tests/rate-limiter.test.ts, threat-model.md
- **What:** Sliding window rate limiter with per-user and per-IP limits. Added to threat model as mitigation for TM-007.
- **Why:** Threat model review found unauthenticated endpoints exposed to abuse.
- **Deferred:** Distributed rate limiting across instances — DEBT-023

### [S012] 2026-03-15 11:15 — Fix flaky auth integration test

- **Phase:** 6
- **Concern:** correctness
- **Action:** fixed
- **Files:** tests/integration/auth-flow.test.ts
- **What:** Replaced hardcoded timeout with event-driven wait. Race condition caused 1-in-5 failures.
- **Why:** CI unreliable, blocking merges. Third occurrence.
- **Deferred:** none
- `[RECURRING]` — similar to S008 flaky test fix

### [S014] 2026-03-18 09:00 — Pin @aws-sdk/client-s3 to resolve version conflict

- **Phase:** 5
- **Concern:** debt
- **Action:** fixed
- **Files:** package.json, package-lock.json
- **What:** Pinned to 3.525.0 to resolve conflict with @aws-sdk/lib-storage.
- **Why:** Same class of conflict as S009 and S011. Different packages, same root cause.
- **Deferred:** Dependency governance policy
- `[RECURRING]` `[PATTERN: S009, S011]`

### [S015] 2026-03-20 14:00 — Restructure src/ into feature modules

- **Phase:** 5
- **Concern:** architecture
- **Action:** refactored
- **Files:** src/auth/*, src/billing/*, src/shared/*, 14 files moved
- **What:** Moved from flat structure to feature-based modules. Auth, billing, shared utilities now isolated.
- **Why:** Navigator decision after retro — flat structure made it hard to scope agent context to one feature area.
- **Deferred:** none

### [S016] 2026-03-22 14:00 — Evaluate Postgres 16 migration

- **Phase:** 3
- **Concern:** architecture
- **Action:** reviewed
- **Files:** docs/adr/ADR-009-postgres-16.md
- **What:** ADR written. Conclusion: defer to Q3, current version adequate.
- **Why:** Navigator asked if new JSON path features simplify query layer. Analysis: marginal benefit vs. migration risk.
- **Deferred:** Full migration plan — revisit at EOL
- `[BOTTLENECK]` — 45 minutes of analysis for a "not yet" conclusion
```

---

## What the Analysis Sees

When `pipeline.py emerge diary.md` runs against this diary:

**Concern distribution:** security 20%, correctness 20%, debt 20%, architecture 25%, other 15%

**Recurring cluster: dependency debt** — S009, S011, S014 all show the same pattern: version conflicts requiring manual pins. Deferred item ("dependency governance policy") appears three times and is never resolved. **Candidate: Dependency Auditor agent** with access to package manifests and debt registry.

**Structural pattern: architecture is changing to support agents** — S015 shows the project restructured to enable scoped agent context. This is the knowledge layer maturing — the project is organizing itself for multi-agent even before multi-agent is activated.

**Bottleneck: architecture reviews** — S016 shows 45 minutes for a deferral decision. If this pattern continues, a pre-screening agent could do initial analysis and present the navigator with a summary instead of requiring deep-dive every time.

**All of this is derived from factual data** — files touched, concern tags, deferred items, recurrence markers. No AI self-assessment required. The diary data drives the recommendation. The navigator makes the call.
