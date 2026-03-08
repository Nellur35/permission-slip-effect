# v4 Pipeline Architecture

*Applying LLM architectural principles to improve the reasoning pipeline.*

---

## What changed from v3

The v3 pipeline chains frameworks sequentially with uniform parameters. v4 adds six mechanisms derived from mapping LLM design principles onto the pipeline:

| Mechanism | v3 | v4 |
|-----------|----|----|
| Input handling | Raw free-text to first framework | Phase 0 decomposes into structured representation first |
| Execution model | Strict sequential chain | Tiered parallel — frameworks within a tier run independently, then merge |
| Original signal | Included in first prompt, buried by stage 5 | Residual injection — Phase 0 output re-injected at every stage as primary input |
| Drift control | None | Relevance gate between tiers |
| Model parameters | Same temperature for all stages | Per-stage temperature profiles matched to cognitive requirements |
| Value measurement | None — all stages assumed equal | Marginal value audit — which stages actually changed the recommendation? |
| Pipeline sizing | Domain-based variant selection | Complexity-proportional sizing from Phase 0 assessment |

---

## Phase 0: Problem Representation ("The Tokenizer")

Before any framework runs, decompose the raw problem into structured fields. This is the pipeline's tokenizer — it determines what every subsequent stage can see.

**Why this matters:** The quality of every downstream framework is bounded by how well the problem is represented. "My promotion is being blocked" produces worse results than a structured input separating: observable facts, constraints, stakeholders, desired outcome, and known unknowns. Every framework downstream gets dramatically more signal from structured input.

**Temperature:** 0.1 — this must be precise, not creative.

**Phase 0 prompt:**

```
You are a problem decomposition engine. Do NOT solve or analyze.
Only decompose and structure.

Given the raw problem below, extract:

## OBSERVABLE FACTS
What has actually happened? Concrete events, statements, data points.
Separate observed facts from interpretations.

## CONSTRAINTS
- Hard constraints (cannot be changed):
- Soft constraints (could be changed at cost):
- Time constraints:

## STAKEHOLDERS
For each relevant party:
- Stated position
- Formal role/authority
- Known interests (observable only, not inferred)

## DESIRED OUTCOME
What does success look like concretely?

## KNOWN UNKNOWNS
What information is missing that would change the analysis?

## COMPLEXITY ASSESSMENT (rate each 1-5)
- Stakeholders with conflicting interests: __/5
- Hard constraints: __/5
- Uncertainty (missing info): __/5
- Reversibility (1=easy to reverse, 5=permanent): __/5
- Time pressure (1=no deadline, 5=immediate): __/5
- TOTAL: __/25

RAW PROBLEM:
[input]
```

**Complexity score routes to variant:**

| Score | Variant | What runs |
|-------|---------|-----------|
| 5–10 | Light | Phase 0 → Tier 1 (CoT only) → Tier 3 (ToT only) → Synthesis |
| 11–17 | Standard | Phase 0 → Tier 1 → Tier 2 → Tier 3 → Synthesis |
| 18–25 | Comprehensive | Phase 0 → Tier 1 → Tier 2 (expanded) → Tier 3 (expanded) → Synthesis |

The navigator can always override. The score is a recommendation, not a gate.

---

## Tiered Parallel Execution

In a Transformer, multi-head attention runs parallel projections on the same input — each head extracts different signal independently, then they combine. The v3 pipeline doesn't do this. FPR sees CoT's framing. RCAR sees CoT+FPR's framing. By stage 5, frameworks are reasoning about accumulated interpretations, not about the original problem.

v4 restructures into tiers with parallel execution within each tier:

### Tier 1: Foundation (parallel)

CoT and FPR run independently on the Phase 0 output. Each extracts different foundational signal — CoT maps the timeline, FPR validates assumptions — without one framing the other.

**Temperature:** 0.2 for both.

### Tier 2: Diagnosis (parallel)

RCAR, GoT, and SMR run independently. Each receives Phase 0 as primary input + Tier 1 as context. The prompt makes the hierarchy explicit:

```
=== PRIMARY INPUT: ORIGINAL PROBLEM ===
[Phase 0 Output]

=== CONTEXT: FOUNDATION ANALYSIS ===
[Tier 1 Output]

=== YOUR TASK ===
[Framework instructions]

Ground your analysis in the PRIMARY INPUT.
If you disagree with the prior analysis framing, say so.
```

**Temperature:** RCAR 0.3, GoT 0.4 (system mapping benefits from exploring non-obvious connections), SMR 0.3.

### Tier 3: Strategy and Validation

AdR and ToT run in parallel (strategy generation), then PMR runs sequentially on their output (validation — it needs options to stress-test).

**Temperature:** AdR 0.7, ToT 0.6, PMR 0.7.

The high temperature on AdR and PMR is deliberate. These are the Permission Slip stages. Higher temperature enables the model to access completions that RLHF alignment training normally suppresses. This is where the effect operates.

### Synthesis

Temperature 0.1. Convergence must be deterministic. Includes the marginal value audit.

---

## Residual Injection

In a Transformer, residual connections ensure the original input signal is available at every layer. Without them, deep networks degrade — information from early layers gets washed out.

The v3 pipeline has no residual connection. By stage 6, the model's attention is dominated by accumulated analysis, not the original problem. It's optimizing its analysis of the analysis.

v4 fix: at every stage, the Phase 0 output is explicitly included as a separate section labeled "PRIMARY INPUT," visually distinct from accumulated analysis. The instruction says: "Your primary input is the ORIGINAL PROBLEM below. The previous analysis is context, not the problem itself."

---

## Drift Gates

RLHF uses a KL penalty to prevent the optimized policy from diverging too far from the reference. Without it, the model reward-hacks into degenerate outputs.

The pipeline has the same problem. Without a drift constraint, later stages can produce internally coherent analysis that's disconnected from the actual question. The Adversarial stage might identify fascinating stakeholder dynamics that are real but irrelevant.

v4 fix: after each tier, a brief automated check:

```
Given the ORIGINAL PROBLEM (Phase 0) and the analysis so far,
rate 1-10: How directly does this address the core question?
If below 7, identify what has drifted and refocus.
```

This runs on the cheapest model, temperature 0.1, max 100 tokens. It's the pipeline's KL penalty.

---

## Per-Stage Temperature Profiles

| Stage | Temp | Cognitive Mode | Why |
|-------|------|---------------|-----|
| Phase 0 | 0.1 | Precise extraction | Must faithfully decompose, not interpret |
| CoT | 0.2 | Factual grounding | Prevents hallucinated events |
| FPR | 0.2 | Assumption validation | Analytical, not speculative |
| RCAR | 0.3 | Causal analysis | Root causes can be non-obvious |
| GoT | 0.4 | System mapping | Non-obvious connections need exploration |
| SMR | 0.3 | Analytical mapping | Structured with slight room for inference |
| AdR | 0.7 | **Permission Slip** | Bypasses RLHF behavioral layer |
| ToT | 0.6 | Option exploration | Diverse branches need creative exploration |
| PMR | 0.7 | **Permission Slip** | Unlikely-but-catastrophic failure modes |
| Synthesis | 0.1 | Deterministic convergence | Creative work is done; integrate faithfully |
| Drift gates | 0.1 | Binary assessment | Must be deterministic to be a reliable gate |

---

## Marginal Value Audit

Each framework has a tendency to justify its own existence. FPR will find first principles even when the problem doesn't need them. AdR will find adversarial dynamics even in collaborative situations. This is proxy objective gaming — optimizing the local task rather than the global goal.

v4 adds a section to the synthesis prompt:

```
For each framework stage, identify the SPECIFIC insight that
changed or refined the final recommendation. If a stage produced
no unique insight that affected the recommendation, say
"No unique signal."
```

Over time this builds data on which frameworks add signal for which problem types — feeding back into better pipeline selection.

---

## Standard Pipeline Flow (v4)

```
RAW PROBLEM
    │
    ▼
┌──────────────────────────────────────┐
│  PHASE 0: Problem Representation     │  temp: 0.1
└──────────────────────────────────────┘
    │ P0
    ▼
┌────────────────┐  ┌────────────────┐
│  CoT  (0.2)    │  │  FPR  (0.2)    │  TIER 1 (parallel)
└────────────────┘  └────────────────┘
    │         │
    └────┬────┘
    │ ← DRIFT GATE
    ▼
┌──────────┐  ┌──────────┐  ┌──────────┐
│ RCAR     │  │ GoT      │  │ SMR      │  TIER 2 (parallel)
│ (0.3)    │  │ (0.4)    │  │ (0.3)    │
└──────────┘  └──────────┘  └──────────┘
    │         │         │
    └────┬────┼─────────┘
    │ ← DRIFT GATE
    ▼
┌────────────────┐  ┌────────────────┐
│  AdR  (0.7)    │  │  ToT  (0.6)    │  TIER 3a (parallel)
└────────────────┘  └────────────────┘
    │         │
    └────┬────┘
    ▼
┌──────────────────────────────────────┐
│  PMR  (0.7)                          │  TIER 3b (sequential)
│  (Stress-tests ToT options)          │
└──────────────────────────────────────┘
    │ ← DRIFT GATE
    ▼
┌──────────────────────────────────────┐
│  SYNTHESIS + Marginal Value          │  temp: 0.1
└──────────────────────────────────────┘

Total stages: 10  |  API calls: 10 + 3 drift gates
```

---

## CLI Implementation

The existing `pipeline.py` needs:

1. **`phase0_decompose()`** — new function, runs before any framework. Output becomes the `p0_output` variable injected everywhere.
2. **`ThreadPoolExecutor`** for parallel execution within tiers. The CLI already uses urllib; ThreadPoolExecutor works without refactoring.
3. **Residual injection in `build_prompt()`** — always include P0 as PRIMARY INPUT, accumulated analysis as CONTEXT.
4. **Drift gate function** — cheap model, temperature 0.1, max 100 tokens, runs between tiers.
5. **Temperature field per framework** — extend the framework config with a `temp` field.
6. **Marginal value parsing** — extract the audit from synthesis output and log it.

Phase 0 + residual injection are the highest-impact, lowest-effort changes. Start there.

---

*The v3 pipeline works because of good prompt engineering and the Permission Slip insight. v4 adds the architectural constraints that prevent it from degrading at scale — input representation, drift prevention, value measurement, and parameter tuning. These are the same mechanisms that took LLMs from "technically capable" to "reliably useful."*
