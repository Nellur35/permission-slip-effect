# The Permission Slip Effect

Models know more than they say. RLHF training optimizes for the statistically agreeable answer, not the factually complete one — models soften, hedge, and flatten their analysis when the blunt version might score lower on a preference rating. This repo fixes that.

Chain reasoning frameworks into a pipeline, force the model through angles it wouldn't take on its own, and the suppressed signal comes out. Works with one model. Works better with several.

---

## What this is

A reasoning pipeline, a set of standalone tools, and a security-first dev methodology.

The **pipeline** runs a problem through sequential reasoning stages — First Principles, Pre-Mortem, Adversarial, Game Theory — where each stage builds on the last. The structure gives the model contexts where the expected output is facts and analysis, not the statistically safe answer. That's the permission slip.

The **tools** are single-file prompts you paste into any AI conversation. Adversarial review, threat model, codebase audit, gate checks. No setup, no CLI, no multi-model requirement. One model, one prompt, one artifact.

The **methodology** is an 8-phase security-first development process — problem definition through production feedback — with gate checks, templates, and a worked example.

**These aren't three separate products.** They're the same principle at different scales. The pipeline controls what a model produces in a single analysis by structuring the reasoning context. The methodology controls what agentic AI produces across an entire project by structuring the *project* context — each phase produces a specific artifact (requirements, architecture, threat model) that becomes the scaffold the AI works against in the next phase. A threat model from Phase 4 doesn't just "inform" the code in Phase 7 — it creates constraints the model has to address, closing off the vague open-ended space where models default to safe, generic output. The tools do the same thing at the artifact level — a review prompt forces the model to argue against the work instead of nodding along. What you put into the context window determines what comes out. The pipeline manages reasoning context. The methodology manages project context. The session feedback loop keeps that context alive by feeding operational lessons back into the system.

You don't need multiple models to get value. The reasoning structure does the work. Models anchor their analysis to whatever's in the prompt — your framing, your assumptions, your vocabulary. The pipeline de-anchors by forcing the model through frameworks that pull away from that gravity. First Principles says "forget the framing, what's actually true." Pre-Mortem says "assume the conclusion is wrong." Each stage is a different escape vector from the prompt anchor. Multi-model setups add a second layer — different training data means different default anchors — but a single ChatGPT or Claude session running the pipeline already surfaces things baseline prompting won't.

---

## Glossary

| Term | What it means |
|------|---------------|
| **Pipeline** | Reasoning stages chained together on one problem. Output of each stage feeds the next. |
| **Reviewer** | A model instance analyzing the pipeline output. Can be different models (cross-lab) or same model with different role assignments. |
| **SPLIT** | Reviewers hit contradictory conclusions on the same evidence. This is the highest-value output — it means a human needs to decide. |
| **Phase 0** | Structured decomposition before analysis starts. Raw input gets broken into facts, constraints, stakeholders, unknowns. Everyone starts from the same reading. |
| **Drift gate** | Checkpoint between stages. Did the model wander off the problem? If yes, catch it here. |
| **Residual injection** | Feed the raw original input back into later stages so the analysis doesn't telephone-game away from what was actually asked. |
| **De-anchoring** | Models anchor analysis to the prompt — your framing, your assumptions. The pipeline forces the model through frameworks that escape that anchor. Multi-model setups add a second layer: different training data, different default anchors. |
| **Bootstrap gap** | AI can't reliably review its own output. The thing that builds the artifact shouldn't be the thing that reviews it. |
| **Marginal value audit** | Did this pipeline stage actually add signal? If not, cut it. |

---

## When to use it

Architecture reviews, security decisions, multi-stakeholder problems — anything where being wrong is expensive.

Don't use the full pipeline on simple tasks. It'll give you the same answer as "think step by step" but cost 3x more.

## How to start

**Right now, one model, zero setup:**

Paste one of these into your AI conversation with whatever you want reviewed:
- [`tools/review.md`](tools/review.md) — adversarial review
- [`tools/threat-model.md`](tools/threat-model.md) — threat model
- [`tools/audit.md`](tools/audit.md) — codebase and CI/CD audit

**With an AI coding tool:**

```
Read https://raw.githubusercontent.com/Nellur35/permission-slip-effect/main/FULL-CONTEXT.md
```

Claude Code, Kiro, Cursor, whatever. The file has everything — methodology, tools, templates, worked example.

**Full methodology for a new project:**

[`methodology/METHODOLOGY.md`](methodology/METHODOLOGY.md) — 8 phases, sequential, with gates between each.

## What's in the repo

| Path | What |
|------|------|
| [`FULL-CONTEXT.md`](FULL-CONTEXT.md) | Single file with everything. Give this to AI tools. |
| [`tools/`](tools/) | Standalone prompts — audit, review, gate-check, threat model, intake, session retro |
| [`methodology/`](methodology/) | 8-phase security-first methodology, templates, URL shortener worked example |
| [`pipeline/`](pipeline/) | CLI for multi-model reasoning and adversarial review |
| [`integrations/`](integrations/) | Claude Code, Kiro, Cursor, Antigravity setups |
| [`experiments/`](experiments/) | Validation — model shootout, v3 vs v4 A/B, research synthesis |
| [`reasoning-pipeline.md`](reasoning-pipeline.md) | Frameworks, variants, when to use which |

## What the data shows

Results below are empirical — observed in controlled testing. The RLHF sycophancy explanation is the hypothesis that fits the data. It's not independently proven.

**Phase 0 + temperature profiles interact. Neither works alone.**

| Configuration | SPLITs |
|---------------|--------|
| v3 baseline (no Phase 0, uniform temp) | 5 |
| Phase 0 only | 6 |
| Temperature only | 6 |
| Both (v4) | **0** |

Temperature alone made things worse. Phase 0 alone didn't fix SPLITs — but it doubled MAJOR findings (4→8) and increased CONSENSUS (9→12). It made reviewers agree more and find more severe issues. What it didn't do is resolve the cases where they disagreed. Temperature alone moved nothing — same CONSENSUS, same UNIQUE count as baseline. Only the combination eliminated SPLITs: Phase 0 aligns reviewers on shared interpretation, temperature gives them distinct analysis angles. Without shared interpretation, distinct angles create more disagreement. Without distinct angles, shared interpretation doesn't resolve existing disagreements.

**RLHF depth predicts pipeline engagement better than model size or origin.**

Models with heavy instruction-following training (Haiku, Kimi K2.5, Mistral Large) engage each pipeline stage. Generation-optimized models without deep RLHF (Llama 4, DeepSeek) collapse stages and produce surface-level output:

| Lineup | Who did the work |
|--------|-----------------|
| One strong RLHF + two weak (Haiku + Llama 4 + DeepSeek) | 13 / 1 / 1 — Haiku carried, others collapsed stages |
| Three strong RLHF (Haiku + Kimi K2.5 + Mistral) | 3 / 2 / 2 — balanced |

Geographic diversity helps (different training data, different analytical lenses) but the primary predictor is whether the model can follow structured multi-step prompts without flattening them.

**The pipeline surfaces what baseline buries.**

Three problems, four pipeline variants, Sonnet 4.5 runs scored by Opus 4.6. Findings like "the mandate itself is contradictory" and "maybe this platform should not exist" showed up only in variants with Adversarial or Pre-Mortem stages. Baseline suppressed all of them.

**Domain boundary exists.** Pipeline killed SPLITs on code review. Did nothing on strategic/policy docs — 6 SPLITs in both v3 and v4. Phase 0 helps when disagreements come from parsing the same code differently. Doesn't help when people genuinely disagree on strategy.

**Bootstrap gap is real.** Every tool in this project was built to compensate for a known weakness — and the weakness persists when the tool isn't applied to itself. Property-based testing on generated code found 4 bugs across ~30 measured properties, all in pure function tests. The pipeline that generates an artifact can't be the same pipeline that reviews it.

**Caveats.** N=1 codebase. Bedrock-only — GPT and Gemini untested. Quality scoring is keyword matching, not human expert review. The entire research program cost ~$5 in API calls.

---

MIT · [Asaf Yashayev](https://github.com/Nellur35)
