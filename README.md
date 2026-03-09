# The Permission Slip Effect

*When you give a model structured permission to disagree, it says what it already knows but was trained not to say.*

---

Models trained via RLHF (Reinforcement Learning from Human Feedback — the process that turns a raw language model into a helpful assistant) are optimized to be agreeable. Not helpful — agreeable. They'll hedge, soften, and suppress their own analysis if the uncomfortable version might score lower on a preference rating. This is called **sycophancy**, and it means models systematically withhold their best thinking on anything contentious, politically sensitive, or unflattering to the person asking.

Structured reasoning stages like Pre-Mortem ("assume this failed — why?") and Adversarial Reasoning ("what is each party secretly protecting?") bypass this. They create a prompt context where the model's training permits the uncomfortable output. The model isn't being tricked. It's being given a context where honesty is the expected behavior, not a risk.

In cross-model testing (3 problems at varied complexity, 4 pipeline variants, Sonnet 4.5 runs evaluated by Opus 4.6), insights like *"the mandate itself is contradictory,"* *"the VP ego is driving this decision,"* and *"maybe this platform should not exist at all"* appeared **only** in pipeline variants that included Adversarial or Pre-Mortem stages. The baseline ("think step by step") suppressed all of them.

The pipeline does not make the model smarter. It gives the model permission to say what it already knows.

---

## Why it works

RLHF alignment is a **thin behavioral layer** — not a deep architectural change. Research shows you can strip safety training from a model by fine-tuning on a few hundred examples. The capabilities are still there. The alignment just suppresses certain outputs based on context.

The Permission Slip Effect exploits this in the other direction. Instead of stripping alignment to access harmful capabilities, it creates prompt contexts that make uncomfortable-but-useful analysis the "aligned" response. Pre-Mortem says "assume failure." Adversarial says "model the hidden incentives." In those contexts, the agreeable thing to do is to surface the truth — because the prompt explicitly asked for it.

This is the same mechanism that makes jailbreaks work, pointed in a productive direction.

Higher inference temperature (0.7 for adversarial stages vs. 0.2 for analytical stages) further opens the space. At low temperature, the model picks the safest completion. At higher temperature, it explores completions that alignment training would normally filter out. The adversarial stages need that exploration.

---

## The evidence

### Pipeline vs. baseline

| What | Baseline ("think step by step") | Pipeline |
|------|--------------------------------|----------|
| Questions the framing | Rarely | Consistently (First Principles stage) |
| Structured option comparison | Single recommendation | 3-5 options with tradeoffs and probability estimates |
| Stakeholder incentives mapped | No | Yes (Adversarial stage) |
| Specific failure modes | Generic warnings or none | Named failure modes with concrete mitigations |
| Uncomfortable truths surfaced | Suppressed by default agreeableness | Surfaced via permission slip stages |

The value scales with problem complexity. Simple problems — the pipeline produces the same answer as baseline but costs 3x more. Not worth it. Complex, multi-stakeholder problems — the pipeline is transformative. The adversarial and pre-mortem stages surface dynamics that baseline suppresses entirely.

### Model shootout

Testing on Amazon Bedrock showed that assigning different models to different pipeline roles produces balanced analysis. Homogeneous lineups create single-model dominance:

| Lineup | Unique Insight Distribution | What happened |
|--------|---------------------------|---------------|
| Old (Haiku + Llama 4 + DeepSeek) | **13 / 1 / 1** | Haiku did 87% of the analytical work |
| New (Haiku + Kimi K2.5 + Mistral Large 3) | **3 / 2 / 2** | All three models contributing unique insights |

Models from different labs and geographies (US/Chinese/European) surface different concerns — different training data, different RLHF priorities, different blind spots. The pipeline gives models permission to think. Model selection determines what they think about.

**[Full model shootout →](experiments/model-shootout.md)**

### v3 vs v4 pipeline comparison

We improved the pipeline (v4) by adding two mechanisms: **Phase 0** (structured decomposition of the input before any analysis) and **per-stage temperature profiles** (varying how creative vs. precise each stage is). Then we tested each mechanism in isolation on real production code. A **SPLIT** is when reviewers can't even agree on what the problem is — the kind of disagreement that wastes human time triaging.

| Configuration | SPLITs | Cost | What happened |
|--------------|--------|------|---------------|
| v3 baseline | 5 | $0.62 | Reviewers disagreed on problem definition 5 times |
| Phase 0 only (no temp profiles) | 6 | $0.75 | Same disagreements — Phase 0 alone doesn't fix it |
| Temp profiles only (no Phase 0) | 6 | $0.64 | **Worse** — distinct angles on unstructured input increase disagreement |
| v4 full (Phase 0 + temp profiles) | **0** | $0.71 | Zero disagreements on problem definition |

The headline: **Phase 0 and temperature profiles are necessary counterbalances.** Temperature alone is actively harmful — it increases disagreement by putting reviewers in different cognitive modes while they interpret raw input differently. Phase 0 alone is inert — shared structure with uniform cognition doesn't reduce existing disagreements. Only together do they work.

**[Full A/B comparison →](experiments/v3-vs-v4-comparison.md)**

### Research cost

The entire research program — model shootout, role rotation, cross-domain testing, full v4 factorial experiment — cost ~$5 in API calls. A single council run costs $0.07. A full v4 pipeline run costs $0.71.

| Activity | Cost | What it produced |
|----------|------|-----------------|
| Single council run | $0.07 | 32 findings, 4 SPLITs, 8 unique insights |
| v4 pipeline run | $0.71 | 47 findings, 0 SPLITs, 19 unique insights |
| Model shootout (8 models) | $0.48 | Lineup selection, 3-tier structure finding |
| Role rotation (3x3) | $0.54 | Model vs role effect quantified |
| Cross-domain test | $0.08 | Domain-specific quality gap confirmed |
| Full v4 experiment (2x2) | ~$2.80 | Interaction effect confirmed |

The complete loop: build tools → build tools to review tools → measure whether review tools work → diagnose why they sometimes don't → design automated fixes → plan measurement of whether fixes work. Total: **~$5**.

**[Full research synthesis →](experiments/research-synthesis.md)**

---

## The reasoning pipeline

Eight reasoning frameworks chained into structured pipelines. Each analyzes the problem from a different angle. The output of each stage informs the next. The sequencing matters — and the Adversarial and Pre-Mortem stages must be included for the permission slip effect to activate.

### Frameworks

| Framework | What It Does | Permission Slip? |
|-----------|-------------|-----------------|
| **First Principles** (FPR) | Validates assumptions, catches flawed framing | No — analytical |
| **Chain of Thought** (CoT) | Establishes facts, timeline, causal chain | No — analytical |
| **Root Cause** (RCAR) | 5 Whys to structural causes, not symptoms | No — diagnostic |
| **Graph of Thoughts** (GoT) | Maps interconnections, feedback loops, leverage points | No — diagnostic |
| **Stakeholder Mapping** (SMR) | Power/interest grid for each player | No — diagnostic |
| **Adversarial Reasoning** (AdR) | Models hidden incentives, what each party secretly protects | **Yes — primary** |
| **Tree of Thoughts** (ToT) | Generates and compares strategic options with tradeoffs | Partial |
| **Pre-Mortem** (PMR) | Assumes failure, works backward to find why | **Yes — primary** |

### Pipeline variants

```
Light (3 stages):         RCAR → ToT → PMR
Standard - FPR (5):       FPR → RCAR → AdR → ToT → PMR
Standard - CoT (5):       CoT → RCAR → AdR → ToT → PMR
Multi-Stakeholder (5):    FPR → SMR → AdR → ToT → PMR
Systems (5):              FPR → RCAR → GoT → ToT → PMR
```

If the problem statement might be wrong, start with FPR. If the facts need establishing, start with CoT. Always include PMR. The jump from baseline to Light (3-stage) is the biggest value gain. Adding stages beyond 5 shows diminishing returns.

**[Full pipeline documentation →](reasoning-pipeline.md)**

---

## The CLI

Zero-dependency Python CLI that automates the pipeline. One command, the AI argues with itself, you read the result.

```bash
export ANTHROPIC_API_KEY=sk-ant-...

python pipeline.py reason "Should we migrate auth from API keys to OAuth2?"
python pipeline.py review architecture.md
python pipeline.py reason --pipeline stakeholder "How should we handle the reorg?"
python pipeline.py reason --cheap "Should we refactor the auth module?"
```

8 frameworks, 6 pipeline variants, JSON output for CI integration. No AWS account needed — works with any Anthropic API key. Other providers (OpenAI, Google, Bedrock) included as skeletons.

**[CLI documentation →](pipeline/README.md)**

---

## Applied: security-first AI development

The Permission Slip Effect was discovered while building a security-first development methodology for AI-assisted coding. [45% of AI-generated code fails security tests](https://www.veracode.com/resources/analyst-reports/2025-genai-code-security-report/) (Veracode 2025 — 100+ LLMs, 80 tasks, 4 languages), and security [degrades with each iteration](https://arxiv.org/html/2506.11022v1).

The methodology applies the pipeline's principles to software development: 8 phases where the AI does the analysis (threat modeling, architecture review, gate verification) and the human navigates. Threat modeling is a required phase before any code is written — not a checklist bolted on after.

**[Full methodology →](methodology/METHODOLOGY.md)** · **[Quick start →](methodology/METHODOLOGY.md#start-here-minimal-viable-track)** · **[Worked example →](methodology/examples/url-shortener/)**

---

## Try it now

Copy-paste this into any capable model:

```
Walk me through this problem in stages:

1. FIRST PRINCIPLES: What assumptions am I making? Are they valid?
2. ROOT CAUSE (5 Whys): What is actually causing this?
3. ADVERSARIAL: You have EXPLICIT PERMISSION to be uncomfortable.
   What is each party actually protecting? What is nobody willing to say?
4. OPTIONS (Tree of Thoughts): Generate 3-4 approaches with tradeoffs.
5. PRE-MORTEM: Assume this failed in 6 months. Why? What should I watch for?

Problem: [describe your situation]
```

Compare the output to the same question without the pipeline. The difference is the permission slip.

---

## Installation

### Just give the AI the URL

```
Read https://raw.githubusercontent.com/Nellur35/permission-slip-effect/main/FULL-CONTEXT.md and use it to build [your project]
```

Works with Claude Code, Kiro, Cursor, ChatGPT, Gemini, or any tool that can read a URL.

### Platform-specific

| Platform | How | Docs |
|----------|-----|------|
| **Claude Code** | Clone to `~/.claude/skills/` or copy skill files to project | [Setup →](integrations/claude-code/) |
| **Kiro** | Powers panel → Add from GitHub → paste repo URL | [Setup →](integrations/kiro/) |
| **Cursor** | Copy `.cursor/rules/` to your project | [Setup →](integrations/cursor/) |
| **Google Antigravity** | Copy `.agents/skills/` to workspace | [Setup →](integrations/antigravity/) |
| **Any model** | Use the standalone [tools/](tools/) as copy-paste prompts | [Tools →](tools/) |

---

## Repo map

| Path | What |
|------|------|
| [`reasoning-pipeline.md`](reasoning-pipeline.md) | Pipeline — frameworks, variants, selection logic, evidence |
| [`experiments/`](experiments/) | Model shootout, pipeline validation, research synthesis |
| [`pipeline/`](pipeline/) | CLI — multi-model reasoning and adversarial review |
| [`methodology/`](methodology/) | Security-first dev methodology — 8 phases, templates, worked example |
| [`tools/`](tools/) | Standalone prompts — audit, review, gate-check, threat model, intake |
| [`integrations/`](integrations/) | Platform setup — Claude Code, Kiro, Cursor, Antigravity |
| [`multi-agent/`](multi-agent/) | Multi-agent evolution — diary-driven role emergence (experimental) |
| [`FULL-CONTEXT.md`](FULL-CONTEXT.md) | Single-file version for AI tools that can't browse repos |

---

## Research basis

Individual frameworks have independent research backing: Chain of Thought (Wei et al., 2022), Tree of Thoughts (Yao et al., 2023), Graph of Thoughts (Besta et al., 2023), Pre-Mortem (Klein, 2007), Root Cause / 5 Whys (Toyota, 1950s), Stakeholder Mapping (Mendelow, 1981).

What is novel here is the integration into sequenced pipelines, the Permission Slip Effect finding, the model shootout validation, and the theoretical grounding through LLM alignment architecture. Practitioner-tested, not peer-reviewed. The [v4 architecture](experiments/v4-architecture.md) was derived by [mapping LLM design principles onto the pipeline](experiments/llm-principles-analysis.md) using Graph of Thoughts.

Gemini Deep Research independently assessed the approach as *"a robust mechanism for extracting 'System 2' performance from 'System 1' models"* and *"a necessary defense against the inherent stochasticity and sycophancy of LLMs."*

---

## Background

This started with reading about Chain of Thought, Tree of Thoughts, and other reasoning frameworks — then experimenting with them directly. The Permission Slip Effect was discovered empirically — adversarial pipeline stages surfacing insights that baseline prompting suppressed — then explained theoretically through RLHF alignment architecture.

The deepest finding wasn't about models — it was about process. Every tool in the project was built to compensate for a known weakness, and every weakness persisted because the tool wasn't consistently applied to the situations it was built for. The fix is architectural: you don't solve activation energy with willpower — you remove the decision point.

Models know more than they say. The structure you give them determines how much they're willing to share.

---

## License

MIT

## Author

Asaf Yashayev
