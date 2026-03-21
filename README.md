# The Permission Slip Effect

*Structured reasoning that forces AI past its default safe answer — for engineers and analysts making decisions where being wrong is expensive.*

Models know more than they say. RLHF training optimizes for the statistically agreeable answer, not the factually complete one — models soften, hedge, and flatten their analysis when the blunt version might score lower on a preference rating. Chain reasoning frameworks into a pipeline, force the model through angles it wouldn't take on its own, and the suppressed signal comes out.

---

## Try it in 5 minutes

**Paste one of these into any AI conversation** with whatever you want reviewed:

- [`tools/review.md`](tools/review.md) — adversarial review of any artifact
- [`tools/threat-model.md`](tools/threat-model.md) — threat model from architecture
- [`tools/audit.md`](tools/audit.md) — codebase and CI/CD gap analysis

No setup. No CLI. One model, one prompt, one artifact.

**With an AI coding tool** (Claude Code, Kiro, Cursor, anything):

```
Read https://raw.githubusercontent.com/Nellur35/permission-slip-effect/main/FULL-CONTEXT.md
```

That single file has everything — methodology, tools, templates, worked example. The AI reads it and has the full system.

**Starting a new project from scratch:**

[`methodology/METHODOLOGY.md`](methodology/METHODOLOGY.md) — 8 phases, sequential, with gate checks between each.

---

## What this is

One idea at three zoom levels.

The **pipeline** chains reasoning frameworks — First Principles, Pre-Mortem, Adversarial, Game Theory — on a single problem. Each stage builds on the last. The structure creates contexts where the expected output is facts and analysis, not the statistically safe answer. That's the permission slip.

The **tools** are single-file prompts you paste into any AI conversation. Adversarial review, threat model, codebase audit, gate checks. No multi-model requirement.

The **methodology** is an 8-phase security-first development process — problem definition through production feedback — with gate checks, templates, and a worked example.

Pipeline manages reasoning context. Methodology manages project context. Tools work at the artifact level. Same principle, different scale.

---

## When to use it — and when not to

**Use it for:** Architecture reviews, security decisions, multi-stakeholder problems, complex decisions with ambiguity, anything where being wrong is expensive.

**Don't use it for:** Simple well-defined tasks, time-sensitive decisions where speed beats depth, problems where the path forward is already clear. The pipeline gives you the same answer as "think step by step" on easy problems — but costs 3x more.

---

## What the data shows

Results are empirical — observed in controlled testing. Caveats upfront: N=1 codebase, Bedrock-only (GPT and Gemini untested), quality scoring is keyword matching not human expert review, the entire research program cost ~$5 in API calls. The RLHF sycophancy explanation is the hypothesis that fits the data. It's not independently proven.

**The pipeline surfaces what baseline buries.** Three problems, four pipeline variants, Sonnet 4.5 runs scored by Opus 4.6. Findings like "the mandate itself is contradictory" and "maybe this platform should not exist" showed up only in variants with Adversarial or Pre-Mortem stages. Baseline suppressed all of them.

**Phase 0 + temperature profiles interact. Neither works alone.**

| Configuration | SPLITs |
|---------------|--------|
| v3 baseline (no Phase 0, uniform temp) | 5 |
| Phase 0 only | 6 |
| Temperature only | 6 |
| Both (v4) | **0** |

Temperature alone made things worse. Phase 0 alone didn't fix SPLITs — but it doubled MAJOR findings (4→8) and increased CONSENSUS (9→12). Only the combination eliminated SPLITs: Phase 0 aligns reviewers on shared interpretation, temperature gives them distinct analysis angles. Without shared interpretation, distinct angles create more disagreement. Without distinct angles, shared interpretation doesn't resolve existing disagreements.

**RLHF depth predicts pipeline engagement better than model size or origin.** Models with heavy instruction-following training (Haiku, Kimi K2.5, Mistral Large) engage each pipeline stage. Generation-optimized models without deep RLHF (Llama 4, DeepSeek) collapse stages and produce surface-level output. The primary predictor is whether the model can follow structured multi-step prompts without flattening them.

**Domain boundary exists.** Pipeline killed SPLITs on code review. Did nothing on strategic/policy docs — 6 SPLITs in both v3 and v4. This is a real limitation: Phase 0 helps when disagreements come from parsing the same code differently. It doesn't help when people genuinely disagree on strategy.

**Bootstrap gap is real.** The pipeline that generates an artifact can't be the same pipeline that reviews it. Property-based testing on generated code found 4 bugs across ~30 measured properties. Every tool in this project was built to compensate for a known weakness — and the weakness persists when the tool isn't applied to itself.

Full experiment data: [`experiments/`](experiments/) — model shootout, v3 vs v4 A/B comparison, v4 architecture, research synthesis.

---

## What's in the repo

**Start here:**

| Path | What |
|------|------|
| [`FULL-CONTEXT.md`](FULL-CONTEXT.md) | Single file with everything. Give this to AI tools. |
| [`tools/`](tools/) | Standalone prompts — paste and go. Audit, review, gate-check, threat model, intake, session retro |
| [`methodology/`](methodology/) | 8-phase security-first methodology, templates, URL shortener worked example |

**Go deeper:**

| Path | What |
|------|------|
| [`pipeline/`](pipeline/) | CLI for multi-model reasoning and adversarial review |
| [`integrations/`](integrations/) | Claude Code, Kiro, Cursor, Antigravity setups |
| [`multi-agent/`](multi-agent/) | Earned multi-agent emergence — diary, hooks, telemetry, domain-split sessions |
| [`gotchas/`](gotchas/) | Known failure modes — system-level and per-skill. Where Claude breaks and how to catch it |
| [`experiments/`](experiments/) | Validation data — model shootout, v3 vs v4 A/B, research synthesis |
| [`reasoning-pipeline.md`](reasoning-pipeline.md) | Framework reference — variants, selection logic, when to use which |

Not sure where to start? See [`START-HERE.md`](START-HERE.md).

---

## How it works (theory)

The pipeline doesn't make models smarter. It changes what they're willing to say.

Models anchor their analysis to the prompt — your framing, your assumptions, your vocabulary. The pipeline de-anchors by forcing the model through frameworks that pull away from that gravity. First Principles says "forget the framing, what's actually true." Pre-Mortem says "assume the conclusion is wrong." Each stage is a different escape vector from the prompt anchor.

These aren't three separate products. They're the same principle applied at different scales. The methodology structures *project* context — each phase produces a specific artifact that becomes the scaffold the AI works against in the next phase. A threat model from Phase 4 creates constraints the model has to address in Phase 7, closing off the vague open-ended space where models default to safe, generic output. The tools do the same thing at the artifact level — a review prompt forces the model to argue against the work instead of nodding along. The session feedback loop keeps context alive by feeding operational lessons back into the system.

Multi-model setups add a second layer — different training data means different default anchors — but a single ChatGPT or Claude session running the pipeline already surfaces things baseline prompting won't.

**Key concepts:**

| Term | What it means |
|------|---------------|
| **SPLIT** | Reviewers hit contradictory conclusions on the same evidence. Highest-value output — means a human needs to decide. |
| **Phase 0** | Structured decomposition before analysis. Facts, constraints, stakeholders, unknowns. Everyone starts from the same reading. |
| **De-anchoring** | Forcing the model past the prompt anchor through framework rotation. |
| **Bootstrap gap** | AI can't reliably review its own output. The builder shouldn't be the reviewer. |
| **Residual injection** | Raw original input fed back into later stages so analysis doesn't drift. |
| **Drift gate** | Checkpoint between stages — did the model wander off the problem? |
| **Marginal value audit** | Did this pipeline stage actually add signal? If not, cut it. |

---

MIT · [Asaf Yashayev](https://github.com/Nellur35) · Security hobbyist
