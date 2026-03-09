# Research Synthesis: What the Data Shows

*Empirical findings from applying the reasoning pipeline and multi-model review methodology across multiple projects.*

Date: 2026-03-09
Data sources: 37 meta-pipeline reviews, 4 experiment reports, 2 council reports, spec drift index, PBT census, finding dispositions, evolution report, retrospective.

---

## 1. The De-Anchoring Thesis: VALIDATED (with caveats)

The core claim — that models from different training origins produce different concern categories — holds across all data points.

**Evidence:**

- **Model shootout (8 models):** Clear 3-tier structure in reasoning pipeline engagement. RLHF depth predicts engagement better than model size or origin.
- **Role rotation (3x3 factorial):** Model matters more than role (4.0 vs 3.6 point variance), but the Challenger pipeline extracts the most from every model.
- **Cross-domain test:** Haiku dominance is domain-specific (security: 36 vs 27-31; methodology: 50 vs 46-48). On non-security artifacts, the gap nearly closes.
- **Shared findings analysis:** Even CONSENSUS findings show approach diversity — same problem, different lenses (security vs engineering vs operations).
- **v3 vs v4 comparison:** Reviewer contribution shifted from 13/1/1 (old lineup) to 3/2/2 (new lineup). De-anchoring requires the right model selection, not just multiple models.

**Caveats:**

- N=1 codebase. The zero-SPLIT finding in v4 needs replication on 3-5 codebases.
- Bedrock-only model set. GPT and Gemini untested.
- Quality scoring uses keyword matching, not human expert review.

---

## 2. The Interaction Effect: CONFIRMED

The v4 pipeline's zero-SPLIT result comes from the interaction of Phase 0 + temperature profiles, not either alone. This is the strongest quantitative finding.

| Condition | SPLITs |
|-----------|--------|
| Neither (v3) | 5 |
| Phase 0 only | 6 |
| Temperature only | 6 |
| Both (v4) | 0 |

**Mechanism:** Phase 0 ensures shared interpretation (prevents "parsed differently" disagreements). Temperature ensures distinct analysis angles (prevents overlapping findings that generate borderline SPLITs). Neither alone is sufficient.

**Limitation:** Doesn't work on strategic documents. Phase 0 decomposition helps on code/design artifacts but not on policy/strategy documents where the ambiguity is inherent, not parsing-related. In testing, a strategy document produced 6 SPLITs in both v3 and v4.

---

## 3. SPLIT Findings Are the Highest-Value Output: SUPPORTED

From finding dispositions (N=2 runs with disposition data):

| Finding Type | ACTED Rate |
|-------------|------------|
| SPLIT | 100% (2/2) |
| UNIQUE_INSIGHT | ~17% (2/12, 5 TBD) |
| CONSENSUS | ~0% (0/16+, mostly ALREADY_KNOWN) |

This validates the priority ordering: **SPLIT > UNIQUE_INSIGHT > CONSENSUS.** The de-anchoring value is in the disagreements, not the agreements.

Small sample warning: 2 SPLIT findings is not enough for statistical confidence. But the directional signal is strong — both SPLITs led to design changes.

---

## 4. Cost Efficiency of Multi-Model Review

| Activity | Cost | Value Delivered |
|----------|------|-----------------|
| Single council run (3 models reviewing one artifact) | $0.07 | 32 findings, 4 SPLITs, 8 unique insights |
| v4 pipeline run | $0.71 | 47 findings, 0 SPLITs, 19 unique insights |
| Model shootout (8 models) | $0.48 | Lineup selection, 3-tier structure finding |
| Role rotation (3x3) | $0.54 | Model vs role effect quantified |
| Cross-domain test | $0.08 | Domain-specific quality gap confirmed |
| Full v4 experiment (2x2) | ~$2.80 | Interaction effect confirmed |

**Total research cost: ~$5.** Total value: validated methodology, optimized lineup, 6 confirmed findings. This is extremely cost-effective research.

---

## 5. The Principle Extends Beyond Reasoning: PBT Bug-Finding

The Permission Slip Effect is a specific case of a broader principle: **structured constraints extract better output than open-ended requests.** Property-based testing (PBT) is the same principle applied to code — instead of asking "does this work?" you constrain the test to a formal property and let a fuzzing framework (like Python's Hypothesis) explore the input space automatically.

From the PBT census (measured subset):

| Property Type | Bugs Found | Rate |
|--------------|-----------|------|
| Pure function properties | 3/5 | 60% |
| Mocked properties | 0/3 | 0% |
| High-confidence properties (expected to pass) | 0/24 | 0% |
| **Total measured** | **3/27** | **11%** |

Plus a subsequent session caught a real edge case in a utility function (duplicate name handling in a list filter). That's 4 bugs total across ~30 measured properties = **13%**.

The pure function hypothesis is supported: pure function properties catch bugs at a much higher rate than mocked properties. Pure functions have deterministic behavior that Hypothesis can explore exhaustively, while mocked properties test interaction patterns that are harder to shrink.

~100+ properties remain TBD. Filling these in would give a much more reliable rate.

---

## 6. The Bootstrap Gap: Tools Don't Review Themselves

Every tool in this project — including the pipeline itself — exhibits the same pattern:

- The Permission Slip pipeline exists to enable adversarial thinking. Its creator skipped it.
- The multi-model review pipeline exists to de-anchor single-reviewer blind spots. Wasn't used on a key design artifact. Result: gaps made it to implementation.
- Steering rules exist to prevent repeat mistakes. The same mistake was documented 3 times.
- The multi-agent architecture exists to catch blind spots via structured dispatch. Sat unused for weeks after being built.

The common thread: every tool in this project was built to compensate for a known weakness, and the weakness persists because the tool isn't consistently applied to the situations it was built for.

This is not a tooling problem. The tools work when used. It's an activation energy problem — the cost of using the tool (context switch, setup time, credit cost) exceeds the perceived benefit in the moment, even when the expected value is positive.

The fix is architectural, not motivational. Rules with concrete triggers (specific error messages, specific tool states) get near-100% compliance. Rules requiring proactive discipline ("remember to check before acting") don't. The solution: convert process rules into automated gates — hooks that fire on concrete triggers, removing the decision point entirely.

*You don't solve activation energy with willpower. You remove the decision point.*

---

## Key Takeaways

1. **Multi-model review works, but only with the right lineup.** The 13/1/1 → 3/2/2 shift proves model selection matters more than model count.

2. **The interaction effect (Phase 0 + temperature) is the strongest finding.** Neither mechanism alone reduces SPLITs. This is publishable if replicated.

3. **Structured constraints beat open-ended requests — in reasoning, in testing, in process.** The Permission Slip Effect, PBT pure-function results, and hook compliance data all point the same direction.

4. **The biggest process gap is not tooling — it's consistent application of existing tools.** The fix is removing the decision point, not strengthening the discipline.

---

## What's Missing (for a publishable paper)

- **Replication:** Zero-SPLIT finding needs 3-5 more codebases
- **Human expert validation:** Quality scoring is automated, needs blind human review
- **Larger PBT census:** ~100 properties are TBD
- **External validation:** Someone other than the creator needs to use the methodology

---

## The Complete Loop

The full arc across this project:

1. Build tools (v1.0-v2.8)
2. Build tools to review tools (v2.9-v2.12, Meta Pipeline)
3. Measure whether the review tools work (this synthesis, sections 1-4)
4. Discover the principle extends beyond reasoning (section 5)
5. Diagnose why tools sometimes aren't used (section 6, bootstrap gap)
6. Design automated fixes (hooks that convert process rules into gates)
7. Plan measurement of whether fixes work (track compliance over 3 sessions)

This is a complete **build-measure-diagnose-fix-verify** loop. Total research cost: **~$5**.

Not "we built a tool" but "we built a tool, measured whether it works, diagnosed why it sometimes doesn't, designed automated fixes, and planned how to measure whether the fixes work."
