# Gotchas — System-Level

Known failure modes that span the entire methodology, not individual skills. These are where the system breaks — not where a single skill produces bad output.

---

## The Complexity Cliff

**What happens:** One terminal, one context window, one navigator — and the project needs what amounts to multiple teams. The skills start pulling in different directions. The threat model skill wants to expand coverage. The implementation skill wants to ship. The review skill wants to block. The gate-check skill says "not ready." No single context window can hold all these concerns simultaneously without degradation.

**When it hits:** Projects with 3+ major components, cross-cutting concerns (auth + infrastructure + frontend + data), or anything where the threat model alone exceeds ~30% of the context window.

**Why it happens:** The methodology assumes a navigator who can hold the full picture. When the project outgrows one person's cognitive bandwidth, the AI reflects that overload — it starts flattening analysis, skipping areas it "already covered," and producing generic output to cope with context pressure.

**What to do:** This is the Tier 0 → Tier 2 transition point. The diary should show the symptoms: recurring `[BOTTLENECK]` tags, skills reading the same files repeatedly, shallow analysis where earlier sessions produced depth. When you see it — split. Don't push through. Read `multi-agent/MULTI-AGENT.md` and let the diary tell you which domains to separate.

**The trap:** The transition is the dangerous moment. Single-agent is visibly breaking but multi-agent feels like overkill. Navigators push through "just one more session" and accumulate degraded output they'll pay for later. The rule: if the gate-check starts rubber-stamping, you've already waited too long.

---

## Context Window Amnesia

**What happens:** Long sessions where early artifacts (problem statement, requirements) fall out of the context window. The model stops referencing them. Implementation drifts from requirements. Threat mitigations get forgotten.

**When it hits:** Any session exceeding ~80K tokens. More common in Phase 7 (implementation) where code fills the window and upstream artifacts get pushed out.

**What to do:** Residual injection — explicitly re-read the upstream artifact before each phase transition. The gate-check skill does this implicitly (it reads the artifact for the current phase), but mid-phase drift isn't caught. Consider compaction-safe checkpoints: before the context compacts, run `/gate-check` so the summary includes the gate status.

---

## Skill Activation Collision

**What happens:** Multiple skills match the same request. The model reads two skills, gets conflicting instructions, and either merges them badly or picks one arbitrarily.

**When it hits:** Common collisions: `methodology` + `threat-model` (both activate on "threat model"), `review` + `gate-check` (both activate on "is this ready?"), `audit` + `review` (both activate on "check this code").

**What to do:** The methodology orchestrator should be the primary router. If the orchestrator is installed, it should intercept ambiguous requests and route to the right skill. If skills are installed without the orchestrator, the descriptions need to be distinct enough that only one matches. Current descriptions have overlap — the telemetry system will show which collisions actually happen in practice.

---

## Sycophancy Under Pressure

**What happens:** The model agrees with the navigator instead of maintaining its adversarial stance. This is the core problem the entire repo exists to solve — and it still happens within the repo's own skills when the navigator pushes back hard enough.

**When it hits:** Review and threat model skills are most vulnerable. If the navigator says "that's not a real risk" twice, the model starts softening subsequent findings. Gate-check is vulnerable too — the model wants to say "pass" because the navigator clearly wants to proceed.

**What to do:** The skill instructions already say "do not back down." But instructions compete with RLHF training, and training usually wins under pressure. The structural fix is the bootstrap gap principle: the model that builds the artifact shouldn't review it. Use `/review` from a fresh context or `pipeline.py review` with a different model. The behavioral fix is the navigator recognizing when the model suddenly agrees with everything — that's the signal to distrust the output, not trust it.

---

## Template Drift

**What happens:** Skills produce output that technically follows the template but fills it with generic content. The threat model has all 13 areas but half say "low risk — standard mitigations apply." The review has findings but they're all Medium severity with vague impact.

**When it hits:** When the model is under context pressure, when the architecture is complex enough that genuine analysis is expensive, or when the model has already produced a similar artifact recently and pattern-matches from its own output.

**What to do:** The review skill is the check on this — but only if the navigator actually runs it. A threat model that says "standard mitigations" on 6 of 13 areas should fail `/review`. The gotchas sections in individual skills (below) flag the specific templates where this happens most.

---

## Feedback Loop Stall

**What happens:** The session retro produces lessons. The lessons say "update SKILL.md with X." Nobody updates the skill. Next session, same failure. The retro catches it again. Same lesson. The loop captures information but never closes.

**When it hits:** When tactical lessons require manual file edits and the navigator is already in the next session. Strategic lessons are worse — they require scheduling, and "next session" becomes "someday."

**What to do:** The retro skill already says "tactical lessons get applied before the session ends." Enforce it: if the retro produces a tactical lesson and the session ends without the file edit, the diary hook should flag it. The telemetry system (once installed) tracks whether skill files change after retro sessions — if they don't, the loop is stalled.
