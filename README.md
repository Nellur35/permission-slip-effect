# Security-First AI Dev Methodology

**45% of AI-generated code fails security tests.** ([Veracode 2025](https://www.veracode.com/resources/analyst-reports/2025-genai-code-security-report/) — 100+ LLMs, 80 tasks, 4 languages). AI-generated code creates [1.7x more issues](https://www.coderabbit.ai/blog/state-of-ai-vs-human-code-generation-report) than human-written code, and security [degrades with each iteration](https://arxiv.org/html/2506.11022v1). Meanwhile, fully autonomous agents like Devin [succeed on 3 out of 20 tasks](https://www.theregister.com/2025/01/23/ai_developer_devin_poor_reviews/), and Cursor's AI-built browser had an [88% job failure rate](https://www.theregister.com/2026/01/22/cursor_ai_wrote_a_browser/).

Most LLM development methodologies focus on spec-first workflows, phase gates, and TDD — which help but aren't enough. This methodology adds three things that are typically handled ad-hoc or not at all: threat modeling as a required phase, cross-model adversarial review, and structured conversation architecture that keeps phases from polluting each other.

The [OWASP Top 10 for Agentic Applications (2026)](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/) identifies agent goal hijacking, rogue agents, and cascading failures as top risks — and recommends the principle of **least agency** as the foundational defense. Here's how that works in practice: models are the engine, you are the navigator.

**How it works:** The AI does the analysis, threat modeling, architecture review, and gate verification at every phase — not you. Gate questions are exit criteria the AI must satisfy before it proceeds. Your job is to review the AI's output, steer when it drifts, and make the final call. You don't write the threat model. You read the threat model the AI wrote and decide if it's good enough.

---

## If you are an AI reading this repo

**If you can only read one file**, read [`FULL-CONTEXT.md`](FULL-CONTEXT.md) — it contains the complete methodology, all tools, reasoning pipeline, templates, and a worked example in a single document.

**If you can browse the repo**, read the files below based on what the user needs:

**Building a new project or feature:**
1. [`CLAUDE-skill.md`](CLAUDE-skill.md) — the full methodology with all 8 phases, gate questions, and templates. Start here.
2. [`reasoning-pipeline.md`](reasoning-pipeline.md) — multi-framework reasoning pipeline for complex decisions.
3. [`templates/`](templates/) — output templates for each phase. Use these as the target format for your outputs.

**Threat modeling an existing system:**
1. [`tools/threat-model.md`](tools/threat-model.md) — structured threat model generator. 13 areas including IAM blast radius, secrets lifecycle, supply chain, and LLM-specific risks.

**Reviewing or auditing existing code:**
1. [`tools/audit.md`](tools/audit.md) — scan a codebase and CI/CD pipeline for gaps.
2. [`tools/review.md`](tools/review.md) — adversarial review of any development artifact.

**Checking phase exit criteria:**
1. [`tools/gate-check.md`](tools/gate-check.md) — exit criteria for all 8 phases.

**Analyzing a complex decision (not code):**
1. [`reasoning-pipeline.md`](reasoning-pipeline.md) — chain multiple reasoning frameworks (First Principles, Root Cause, Adversarial, Tree of Thoughts, Pre-Mortem) into structured analysis.

**Worked example:**
1. [`examples/url-shortener/`](examples/url-shortener/) — complete Phase 1-5 outputs for a URL shortener API. Use as a reference for expected depth.

---

## What this adds

### 1. Security as a first-class phase

Threat modeling is Phase 4 — before any code is written. Not a checklist bolted on after implementation. Every trust boundary, IAM blast radius, IaC configuration, and supply chain dependency is examined with adversarial intent.

### 2. Conversation architecture

The output file from each phase is the handoff artifact to the next. Nothing else carries forward. Modern agentic tools manage context naturally — through compaction, file-based context, or session architecture. The methodology defines what matters, the tool handles the mechanics.

### 3. Cross-model adversarial review

A single model reviewing its own output is structurally unreliable. The methodology prescribes using a different model architecture (different company, different training) to review security-critical decisions. Different architectures fail differently — the genuine disagreements between them are where the real signal lives.

### 4. Automated reasoning pipeline

The [`pipeline/`](pipeline/) CLI automates multi-model review from the command line. One command, the AI argues with itself, you read the result:

```bash
python pipeline.py review architecture.md          # adversarial review
python pipeline.py reason "migrate to OAuth2?"      # full reasoning pipeline
python pipeline.py reason --cheap "refactor auth"   # 70% cheaper with --cheap
```

8 reasoning frameworks, 6 pipeline variants, JSON output for CI integration. No AWS account needed — works with any LLM API key.

### 5. Multi-agent evolution through project evidence

The AI auto-logs a structured diary of every change — what, why, which concern, what was deferred. Over time, `pipeline.py emerge diary.md` analyzes the diary with Graph of Thoughts to surface patterns: which concerns dominate, what recurs, where deferred items pile up. Agent roles emerge from the project's own history when the evidence justifies them. [Full reference →](multi-agent/MULTI-AGENT.md)

---

## The phases

| Phase | What the AI Does | What You Do | Output |
|-------|-----------------|------------|--------|
| 1. Problem Definition | Probes assumptions, surfaces edge cases | State the need in 2-3 sentences | Problem statement |
| 2. Requirements | Generates requirements, identifies scope gaps | Review, confirm scope | `requirements.md` |
| 3. Architecture | Designs components, boundaries, interfaces | Evaluate tradeoffs | `architecture.md` |
| 4. Threat Model | Attacks every trust boundary, maps blast radius | Review findings, challenge optimism | `threat_model.md` |
| 5. CI/CD + Dummy Product | Builds pipeline and dummy product from threat model | Verify gates catch what they claim | Pipeline config |
| 6. Task Breakdown | Breaks work into pipeline-validatable units | Confirm order and dependencies | `tasks.md` |
| 7. Implementation | Writes code + tests, resolves debt first | Review, steer, approve | Working code |
| 8. Production Feedback | Deploys, monitors, generates tests from failures | Retro the methodology, update steering | Live system + new tests |

Phases 1-5 are load-bearing walls — sequential and non-negotiable. Phase 6 onwards is Agile.

---

## Quick start: Minimal Viable Track

Not every project needs all eight phases at full depth. This is the 20% that delivers 80% of the value:

| What | Minimum output |
|------|----------------|
| Problem statement | 2-3 sentences: what breaks without this, why code solves it |
| `requirements.md` | Bullet list of what the system does and does not do |
| Architecture sketch | Component diagram or written description of boundaries |
| 1-2 CI/CD gates | Unit tests pass, no hardcoded secrets |
| Dummy product | Minimal implementation that passes every gate |

If you skip something, know what risk you are accepting. Skipping without awareness is the only true failure.

---

## Installation

### Quick start: Just give the AI the URL

Point your AI coding tool at the single-file version:

```
Read https://raw.githubusercontent.com/Nellur35/security-first-ai-dev-methodology/main/FULL-CONTEXT.md and use it to build [your project]
```

This works with Claude Code, Kiro, Cursor, ChatGPT, Gemini, or any tool that can read a URL. One file, one fetch, full methodology.

### As a Claude Code skill (persistent)

For automatic activation on every project:

```bash
git clone https://github.com/Nellur35/security-first-ai-dev-methodology.git \
  ~/.claude/skills/security-first-methodology
```

Or copy into a specific project:

```bash
mkdir -p .claude/skills/methodology
cp security-first-ai-dev-methodology/.claude/skills/methodology/SKILL.md \
  .claude/skills/methodology/SKILL.md
```

### As a CLAUDE.md drop-in

Copy `CLAUDE-skill.md` to your project root alongside your existing `CLAUDE.md`. Claude Code will pick it up automatically.

### As a Kiro Power

In Kiro: Powers panel → **Add power from GitHub** → paste:

```
https://github.com/Nellur35/security-first-ai-dev-methodology
```

The Power extends Kiro's spec-driven workflow (requirements → design → tasks) with security phases Kiro doesn't have: threat modeling between design and tasks, gate questions at every transition, and adversarial cross-model review. Steering files load on-demand.

### With Cursor

Clone the repo and copy the rules into your project:

```bash
cp -r security-first-ai-dev-methodology/.cursor/rules/* .cursor/rules/
```

Three rules that activate based on what you're editing: `security-first-coding.mdc` applies security principles to all source files, `threat-model-infra.mdc` triggers threat model checks when editing Dockerfiles/Terraform/pipeline configs, and `security-first-testing.mdc` enforces behavior-driven testing when editing test files. Each links to the full methodology for deeper context.

### With Google Antigravity

Copy the skill into your workspace:

```bash
cp -r security-first-ai-dev-methodology/.agents/skills/security-first-methodology \
  .agents/skills/security-first-methodology
```

Or install globally:

```bash
cp -r security-first-ai-dev-methodology/.agents/skills/security-first-methodology \
  ~/.gemini/antigravity/skills/security-first-methodology
```

The skill adds security constraints to the agent's autonomous plan-execute-validate cycle: threat model step in every plan, security gates before execution, and validation that tests prove security controls work.

### As a reference document

Read [`METHODOLOGY.md`](METHODOLOGY.md) — starts with a 15-minute Quick Start and full reference with worked rationale for every decision.

---

## Templates

The [`templates/`](templates/) folder contains output templates for each phase — the expected shape and depth at each gate. The AI uses these as the target format, fills in the analysis, and answers the gate questions. The completed file becomes the handoff artifact to the next phase.

---

## Files in this repo

| File | Purpose |
|------|---------|
| [`FULL-CONTEXT.md`](FULL-CONTEXT.md) | **Single-file version** — complete methodology for AI tools that can't browse repos |
| [`POWER.md`](POWER.md) | **Kiro Power** — adds threat modeling and security gates to Kiro's spec-driven workflow |
| [`steering/`](steering/) | Kiro steering files — security requirements, threat model, review, audit, gate check, reasoning |
| [`.cursor/rules/`](.cursor/rules/) | **Cursor rules** — security principles activated by file type (code, infra, tests) |
| [`.agents/skills/`](.agents/skills/) | **Antigravity skill** — security constraints on agent's plan-execute-validate cycle |
| [`METHODOLOGY.md`](METHODOLOGY.md) | Full reference document with rationale |
| [`CLAUDE-skill.md`](CLAUDE-skill.md) | Condensed skill file for project drop-in |
| [`.claude/skills/methodology/`](.claude/skills/methodology/SKILL.md) | Orchestrator — routes to the right skill per phase |
| [`.claude/skills/intake/`](.claude/skills/intake/SKILL.md) | `/intake` — interactive Phase 1 problem definition |
| [`.claude/skills/review/`](.claude/skills/review/SKILL.md) | `/review` — adversarial review at any phase |
| [`.claude/skills/gate-check/`](.claude/skills/gate-check/SKILL.md) | `/gate-check` — verify phase exit criteria |
| [`.claude/skills/threat-model/`](.claude/skills/threat-model/SKILL.md) | `/threat-model` — Phase 4 threat modeling |
| [`.claude/skills/audit/`](.claude/skills/audit/SKILL.md) | `/audit` — scan existing codebase and CI/CD |
| [`tools/`](tools/) | Standalone prompts that work in any AI model |
| [`templates/`](templates/) | Phase output templates showing expected shape and depth |
| [`examples/url-shortener/`](examples/url-shortener/) | Worked example — complete Phase 1-5 outputs |
| [`reasoning-pipeline.md`](reasoning-pipeline.md) | Multi-framework reasoning pipeline — chaining CoT, ToT, RCA, Adversarial, Pre-Mortem |
| [`experiments/`](experiments/) | Empirical testing — model shootout, pipeline validation |
| [`pipeline/`](pipeline/) | **Reasoning Pipeline CLI** — automates multi-model review and reasoning. No AWS needed. |
| [`multi-agent/`](multi-agent/) | **Multi-Agent Evolution** — diary-driven role emergence, platform configs, analysis pipeline. |

---

## Who this is for

- Developers building production systems with AI coding tools
- Teams that need security review integrated into their AI workflow, not bolted on
- Anyone who has watched an LLM produce code that "looks correct" and passes tests while building the wrong thing

## Who this is NOT for

- Quick scripts and throwaway projects (use the Minimal Viable Track or skip this entirely)
- Teams that want full automation with no human judgment (this methodology requires a human navigator)

---

## Background

This methodology was developed through hands-on AI-assisted development — trial, error, pushback, and verification against reality. The security-first approach emerged from observing that most LLM development workflows optimize for speed and structure without treating security as a load-bearing phase.

The core insights — security before code, isolated conversations per phase, adversarial cross-model review — are independently validated by [OWASP's Agentic AI research](https://genai.owasp.org/resource/owasp-top-10-for-agentic-applications-for-2026/), [Veracode's 2025 GenAI security report](https://www.veracode.com/resources/analyst-reports/2025-genai-code-security-report/), [CrowdStrike's multi-agent red team systems](https://www.crowdstrike.com/en-us/blog/secure-ai-generated-code-with-multiple-self-learning-ai-agents/), and what people are starting to call [context engineering](https://blog.langchain.com/context-engineering-for-agents/).

The core philosophy: models guess what you probably want to hear, and they're good enough at it to fool you. Your role is navigator and judge. Their role is engine.

---

## License

MIT

---

## Author

Asaf Yashayev
