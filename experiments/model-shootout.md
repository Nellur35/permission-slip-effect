# Multi-Model Reasoning Pipeline: Model Shootout

*Testing which models perform best in chained reasoning pipelines — and proving that role-based model assignment produces better results than homogeneous lineups.*

---

## Background

The [reasoning pipeline](../reasoning-pipeline.md) chains multiple analytical frameworks (CoT → RCA → Adversarial → ToT → Pre-Mortem) into a single structured analysis. Early testing used a single model for all stages. This experiment tests whether **assigning different models to different roles** in the pipeline improves output quality.

The hypothesis: models trained with heavy instruction-following (RLHF) will outperform generation-optimized models on structured multi-step prompts, and different models will contribute different analytical perspectives based on their training biases.

---

## Experiment Setup

**Platform:** Amazon Bedrock (all models accessed via Bedrock APIs)

**Test problem:** A security architecture review prompt requiring the pipeline to identify vulnerabilities, architectural gaps, and operational risks across IAM, deployment, encryption, and resilience dimensions.

**Pipeline structure:** Three-role assignment:
- **Challenger** — Probes assumptions, finds security gaps
- **Architect** — Evaluates structural and deployment-level issues
- **Debugger** — Identifies operational failure modes and resilience gaps

**Evaluation criteria:**
- Total findings generated
- Number of SPLITs (cases where models contributed different implementation approaches to the same finding)
- UNIQUE_INSIGHTs (findings surfaced by only one model that others missed entirely)
- Quality of unique insights (specificity, actionability)

---

## Phase 1: Token Output Benchmark

First, a raw benchmark of how much reasoning output each Bedrock model produces when given the same chained reasoning prompt.

| Rank | Model | Origin | Tokens | Latency | Verdict |
|------|-------|--------|--------|---------|---------|
| 1 | Kimi K2.5 | Moonshot/Chinese | 1428 | 14s | Top tier |
| 2 | Mistral Large 3 | Mistral/EU | 1401 | 10s | Top tier, faster |
| 3 | Qwen3 Next 80B | Qwen/Chinese | 1367 | 29s | Top tier, slow |
| 4 | GLM 4.7 | Z.AI/Chinese | 850 | 10s | Mid tier |
| 5 | Magistral Small | Mistral/EU | 804 | 15s | Mid tier |
| 6 | DeepSeek V3.2 | DeepSeek/Chinese | 556 | 12s | Low tier |
| 7 | Llama 4 Maverick | Meta/US | 511 | 3s | Low tier |
| 8 | Nova Premier | Amazon/US | 496 | 10s | Low tier |
| - | Kimi K2 Thinking | Moonshot | FAIL | - | Response format issue |
| - | MiniMax M2.1 | MiniMax | FAIL | - | Response format issue |

**Key finding:** The top 3 models produce 2.5-3x more tokens than the bottom tier. In a chained reasoning context, higher token counts correlate with the model engaging each pipeline stage rather than collapsing them into surface-level summaries. Two models failed entirely — the pipeline's structured output requirements act as a capability filter.

**Haiku 4.5** (Anthropic/US) was benchmarked separately at **3279 tokens** — the highest output of any model tested — and was selected as the Challenger based on proven performance from earlier pipeline testing.

---

## Phase 2: Old Lineup (Baseline)

**Configuration:**
- Challenger: Haiku 4.5 (Anthropic/US)
- Architect: Llama 4 Maverick (Meta/US)
- Debugger: DeepSeek V3.2 (DeepSeek/Chinese)

**Results:**
- 20 total findings
- Unique insights distribution: **13 / 1 / 1** (Haiku / Llama / DeepSeek)

**Problem:** Haiku was doing 87% of the analytical work. Llama 4 and DeepSeek contributed almost nothing unique — they were generating tokens but not differentiated analysis. The pipeline was effectively single-model with extra steps.

---

## Phase 3: New Lineup

Based on the token benchmark, models were selected for:
1. High token output (engagement with structured prompts)
2. Geographic/training diversity (different analytical biases)
3. Bedrock availability

**Configuration:**
- Challenger: Haiku 4.5 (Anthropic/US) — **3279 tokens**, proven, kept
- Architect: Kimi K2.5 (Moonshot/Chinese) — **1428 tokens**, top benchmark performer
- Debugger: Mistral Large 3 (Mistral/EU) — **1401 tokens**, best efficiency (tokens/latency)

**Results:**
- **23 total findings** (vs 20 with old lineup)
- **3 SPLITs** — all three models contributing different implementation approaches (not just Haiku dominating)
- **7 UNIQUE_INSIGHTs** distributed across all three models:
  - Challenger (Haiku): 3 — IAM architecture, prompt injection, encryption
  - Architect (Kimi K2.5): 2 — deployment IAM coupling, S3 link validation
  - Debugger (Mistral Large 3): 2 — circuit breakers, single-region limitation

**Unique insights distribution: 3 / 2 / 2** (balanced)

---

## Quality Assessment

Token counts and finding counts are proxies. The real test is whether the unique insights are **specific and actionable**:

**Kimi K2.5 (Architect) — "Deployment IAM coupling enforcement":**
> Specific recommendation: add CloudTrail permissions to Lambda role, implement deployment gate that validates permissions against OpenAPI spec.

This is not a generic "check your IAM" finding — it identifies the exact coupling between deployment and runtime permissions and prescribes a concrete gate.

**Mistral Large 3 (Debugger) — "Circuit breakers for external dependencies":**
> Specific recommendation: exponential backoff, 3 attempts, 5s timeout.

Concrete operational parameters, not abstract advice about resilience.

Both of these findings were absent from the old lineup entirely.

---

## Analysis

### Why the new lineup works

The shift from 13/1/1 to 3/2/2 on unique insights is the core proof. It demonstrates that:

1. **Model selection matters as much as pipeline design.** The same pipeline with different models produced fundamentally different insight distributions.
2. **Training diversity produces analytical diversity.** US (Anthropic), Chinese (Moonshot), and EU (Mistral) models surface different concerns — likely reflecting different training data distributions and RLHF priorities.
3. **Token output is a useful but imperfect proxy.** Models producing 500 tokens on structured prompts are likely skipping or collapsing stages. Models producing 1400+ are engaging with each stage. But engagement alone doesn't guarantee unique insights — you also need training diversity.

### The RLHF hypothesis

The top performers (Anthropic, Kimi, Mistral Large) are all known for heavy instruction-following training. The bottom performers (Llama 4, DeepSeek, Nova) are strong at generation but weaker at following structured multi-step prompts. This suggests that **RLHF intensity is a predictor of pipeline compatibility**.

### Missing models

OpenAI (GPT series) and Google (Gemini) were not tested due to Bedrock availability. If Bedrock adds them, they'd likely be Tier 1 candidates given their RLHF investment. The current lineup provides US/Chinese/European diversity with all three pulling their weight.

---

## Recommendations

### For practitioners using this pipeline:

1. **Don't use the same model for all roles.** The whole point is perspective diversity.
2. **Select models with 1000+ tokens on structured prompts.** Below that threshold, models are collapsing pipeline stages.
3. **Prioritize training diversity** — models from different labs/geographies surface different concerns.
4. **The Challenger role needs the highest-output model.** This is where assumption-challenging happens, and it requires the most engagement.
5. **Re-benchmark when new models launch.** Model capabilities shift rapidly; the optimal lineup in March 2026 won't be the optimal lineup in June 2026.

### Current recommended Bedrock lineup (March 2026):

| Role | Model | Origin | Why |
|------|-------|--------|-----|
| Challenger | Haiku 4.5 | Anthropic/US | Highest output (3279 tokens), strongest instruction-following |
| Architect | Kimi K2.5 | Moonshot/Chinese | Top benchmark (1428 tokens), actionable infrastructure insights |
| Debugger | Mistral Large 3 | Mistral/EU | Best efficiency (1401 tokens @ 10s), strong operational findings |

---

## Limitations

- Single test problem (security architecture review). Results may vary across domains.
- Token count is a proxy metric, not a direct quality measure.
- Bedrock inference times vary by region and load — latency numbers are point-in-time.
- Kimi K2.5 has [known Converse API issues on Bedrock](https://github.com/anomalyco/opencode/issues/14221) — tool call tokens leak into text output. Does not affect completion-based pipeline calls, but relevant if extending to agentic workflows.
- No formal statistical significance testing — this is practitioner-level validation, not peer-reviewed research.

---

*The pipeline gives the model permission to think. Model selection determines what it thinks about.*
