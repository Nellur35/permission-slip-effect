# Experiments & Evidence

Empirical validation of the reasoning pipeline and Permission Slip Effect.

## Research Synthesis

**[research-synthesis.md](research-synthesis.md)** — What the data actually shows across all experiments. Six findings, the complete build-measure-diagnose-fix-verify loop, and a $5 total research cost. The headline: the interaction effect (Phase 0 + temperature profiles) is the strongest quantitative finding, and SPLIT disagreements are where all the value lives — 100% ACTED rate vs ~0% for consensus findings.

## Model Shootout

**[model-shootout.md](model-shootout.md)** — Multi-model benchmark on Amazon Bedrock proving that role-based model assignment (Challenger / Architect / Debugger) produces balanced insight distribution vs. single-model dominance. Key result: switching from a homogeneous lineup to a geographically diverse lineup shifted unique insight distribution from **13/1/1** to **3/2/2**.

## v3 vs v4 Pipeline A/B Comparison

**[v3-vs-v4-comparison.md](v3-vs-v4-comparison.md)** — A/B testing of v4 improvements against v3 baseline on real production code, strategic documents, and simple utilities, with full mechanism isolation. The headline finding: **Phase 0 and temperature profiles are necessary counterbalances** — temperature alone is actively harmful (increases disagreement), Phase 0 alone is inert, but together they produce zero SPLITs on code reviews for $0.09 more per run. Also validated: v4 over-analyzes simple code (needs complexity gating), and Phase 0 doesn't fix genuine opinion disagreements on strategic documents.

## v4 Pipeline Architecture

**[v4-architecture.md](v4-architecture.md)** — The improved pipeline design: Phase 0 (structured decomposition), tiered parallel execution, residual injection, drift gates, per-stage temperature profiles, and marginal value audit. Includes complete flow diagrams and CLI implementation specs.

## LLM Principles Analysis

**[llm-principles-analysis.md](llm-principles-analysis.md)** — Graph of Thoughts analysis that mapped 9 structural principles from LLM architecture onto the reasoning pipeline, identified 6 gaps and 1 validated strength (the Permission Slip Effect), and produced the v4 design. The key convergence: three of the gaps (input representation, residual connection, drift constraint) turned out to be the same fix from three angles.

## Pipeline Validation

Cross-model testing (Sonnet 4.5 generation, Opus 4.6 evaluation) across three complexity levels showed that pipeline variants with Adversarial and Pre-Mortem stages consistently surface insights that baseline prompting ("think step by step") suppresses entirely. See [reasoning-pipeline.md](../reasoning-pipeline.md) for detailed results.

## External Validation

Gemini Deep Research independently assessed the pipeline as:
- *"A robust mechanism for extracting 'System 2' performance from 'System 1' models"*
- *"Highly useful, specifically for 'Wicked Problems'"*
- *"Moderately novel — the specific integration constitutes a novel 'Cognitive Macro'"*

## Run Your Own Tests

1. Pick a problem you've already solved (so you can evaluate quality).
2. Run Prompt A: `Think through this step by step and recommend what to do. Problem: [your problem]`
3. Run Prompt B: Use the standard pipeline prompt from [reasoning-pipeline.md](../reasoning-pipeline.md)
4. Compare: Did the pipeline surface something the baseline missed?

If you run experiments, consider opening a PR with results.
