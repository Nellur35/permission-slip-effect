# LLM-Assisted Development

*A Structured Methodology for Building Real Products with AI*

**Asaf Yashayev**

---

## Quick Reference

| Phase | What the AI Does | What You Do | Output | Gate Question |
|-------|-----------------|------------|--------|---------------|
| 1. Problem | Probes assumptions, surfaces edge cases | State the real-world need | Problem statement (2-3 sentences) | What breaks if this isn't built? Why is code the right solution? |
| 2. Requirements | Generates requirements, identifies scope gaps | Review, adjust, confirm scope | `requirements.md` | Is every requirement testable? What is out of scope? |
| 3. Architecture | Designs components, boundaries, interfaces | Evaluate design tradeoffs | `architecture.md` | Can every component be tested in isolation? |
| 3.5 Spike | Builds throwaway test of assumptions (optional) | Read the result, update architecture | Updated `architecture.md` | Was the assumption validated or disproven? |
| 4. Threat Model | Attacks every trust boundary, maps blast radius | Review findings, accept or challenge | `threat_model.md` | What is the worst an adversary can do here? |
| 5. CI/CD | Builds pipeline + dummy product, includes PBT for security logic | Verify gates match threat model | Pipeline config + dummy product | What does a passing pipeline actually prove? |
| 6. Tasks | Breaks work into pipeline-validatable units | Confirm task order and dependencies | `tasks.md` | Which gate validates each task? |
| 7. Implementation | Resolves debt first, writes code + tests | Review, steer, approve | Working code | Does the full pipeline pass? Zero critical debt? |
| 8. Production | Deploys, monitors, generates new tests from failures | Retro the methodology, update steering | Live system + new tests + updated steering | What did production catch? What should the process change? |

Phases 1-5 are sequential and non-negotiable. Phase 6 onwards is Agile. The output file from each phase is the only context that carries forward. Phase re-entry is the norm — going back is the process working, not failing. Some rules are waivable with documentation; safety invariants (CI before deploy, no hardcoded secrets, gates never weakened, destructive actions need human confirmation) are never waivable.

---

## Start Here: Minimal Viable Track

Not every project needs all eight phases at full depth. This is the 20% that delivers 80% of the value.

| What | Why It Cannot Be Skipped | Minimum Output |
|------|--------------------------|----------------|
| Problem Statement | Without this the model optimizes for the wrong thing | 2-3 sentences: what breaks without this, why code solves it |
| `requirements.md` | Without this "done" has no definition | Bullet list of what the system does and does not do |
| Architecture Sketch | Without this the code has no structure to test against | Component diagram or description of boundaries |
| 1-2 CI/CD Gates | Without this "passing" means nothing | Unit tests pass, no hardcoded secrets |
| Dummy Product | Without this the gates are never verified end to end | Minimal implementation that passes every gate |

Skip the rest if you need to. But know what risk you're accepting. Layer in the full methodology as the project grows.

---

## 15-Minute Quick Start

Try the methodology on a trivial project before reading the full document. This proves it works before asking for your time.

**Project:** A URL shortener API. You provide one sentence per phase. The AI does the rest.

**Phase 1 — Problem (1 min):** You say:
> "I need a URL shortener API. Define the problem — what breaks without it, why code is the right solution."

The AI produces a problem statement. You read it, confirm it's right.

**Phase 2 — Requirements (2 min):** You say:
> "Generate requirements.md. Include functional, non-functional, explicit exclusions, definition of done, and Decisions & Rejected Alternatives."

The AI produces `requirements.md`. You review scope and exclusions.

**Phase 3 — Architecture (2 min):** You say:
> "Based on this requirements.md, design the architecture. Every component must be testable in isolation."

The AI produces `architecture.md`. You check the design makes sense.

**Phase 4 — Threat Model (3 min):** You say:
> "Based on this architecture.md, threat model every trust boundary. What's the blast radius? How do you mitigate?"

The AI produces `threat_model.md`. You review findings, challenge anything too optimistic.

**Phase 5 — CI/CD (3 min):** You say:
> "Based on architecture.md and threat_model.md, generate a CI/CD pipeline. Map each gate to a specific threat. Build a dummy product."

The AI produces pipeline config + dummy product. You verify the gates match the threats.

**Result:** Problem statement, requirements, architecture, threat model, pipeline, and dummy product — all in 15 minutes. You wrote 5 sentences. The AI wrote everything else. See [`examples/url-shortener/`](examples/url-shortener/) for what the actual outputs look like.

---

## The Core Philosophy

Models guess what you probably want to hear. They're good at it — good enough to fool you. Left alone, they'll produce code that looks correct, tests that pass, and pipelines that appear green — while building the wrong thing correctly. That's what this methodology is for.

**The AI does the work. You make the decisions.** The AI generates the architecture, writes the threat model, builds the pipeline, produces the code. You review what it produces, steer when it drifts, and rule on disagreements between models. You are the navigator — not the engine. The AI is fast but uncritical. You are slow but have judgment.

This role deepens with practice. Over time you learn to front-load intent ("build X with constraint Y" instead of "build X" then correcting), triage counterexamples yourself before the model surfaces them, and know when to say "change X to Y" versus "investigate this." The methodology accelerates this — each phase teaches you what to look for in the next one. The navigator is not a static role. It is a skill that compounds.

---

## On Methodology, Speed, and the Waterfall Objection

The first objection most people raise: this looks like Waterfall. Sequential phases, artifacts before code, gates before implementation. Everything the Agile movement spent twenty years arguing against.

The objection is wrong, but not for the reason you might expect.

### Foundation First, Sprints After

Phases 1 through 5 are load-bearing walls. You do not sprint your way into a foundation — you pour it once and pour it right. A threat model you iterate on is Swiss cheese. An architecture you discover through sprints is technical debt from day one.

Phase 6 onwards is Agile. Task breakdown is sprint planning. Implementation is sprint execution. The production feedback loop is your retrospective feeding the next cycle. The methodology is sequential where sequencing is load-bearing, and iterative everywhere else. Experienced engineers already do this. They pick the right model for the layer they are working on.

### On Speed

The second objection: this is too slow for modern development.

This confuses the methodology with a human team executing it manually. Two models running in parallel — one generating, one reviewing — compress the foundation phases dramatically. Architecture design with a simultaneous adversarial reviewer takes hours, not weeks. Threat modeling with dual-model review produces a more rigorous output in an afternoon than a human security review that takes a week to schedule.

The real question is whether skipping the foundation is faster in total. It never is. Time saved by skipping architecture is spent debugging. Time saved by skipping threat modeling is spent in incident response.

### On Cost

AI-assisted development costs real money. Context window tokens, API calls, and compute are a budget — not infinite. The methodology should be efficient:

- Max 3 sentences of instruction before code generation. Front-load intent, don't over-explain.
- Don't re-read files the model already has in context. If it just generated the file, it knows what's in it.
- Batch related edits into single requests. Five small fixes cost 5x the tokens of one combined fix.
- Cap fix attempts. If the third attempt doesn't work, the approach is wrong — stop and re-analyze instead of burning more tokens on the same bad path.
- Use the right model tier. Not every task needs the most expensive model. Boilerplate and simple fixes can run on cheaper, faster models.

The methodology's phase structure helps here: clear inputs and gate questions mean less back-and-forth, fewer wasted iterations, and less context pollution.

---

## Phase 1 — Define the Problem

Before any other work, the AI needs a clear problem statement from you. This is the one phase where you provide the primary input — 2-3 sentences about what breaks in the real world and why code solves it. The AI will probe your assumptions, surface edge cases, and help you refine the statement. But the problem itself must come from you.

Two questions must be answered before proceeding:

- What is the actual problem?
- Why does code solve it better than another approach?

Everyone thinks they can skip this. Then the model optimizes beautifully for the wrong objective and you end up with a working product that doesn't solve the real problem.

**Gate questions — do not proceed until answered:**
- What breaks in the real world if this is not built?
- Why is code the right solution and not a process change, a configuration, or an existing tool?

**Output:** A clear problem statement. 2-3 sentences. Defines the real-world need, not the technical solution.

---

## Phase 2 — Product Requirements

The AI generates the requirements document from your problem statement. It covers functional requirements, non-functional requirements, explicit exclusions, and definition of done. Your job: review what it produced, catch missing requirements, and confirm what's in scope vs. out of scope.

Every requirement that is missing or ambiguous becomes a bug later. If requirements are unclear, stop and resolve them before proceeding.

**Gate questions — do not proceed until answered:**
- Is every requirement testable? If you cannot write a test for it, it is not a requirement.
- What is explicitly out of scope?
- What does done look like in reality, not in a CI dashboard?

**Output:** `requirements.md` with a **Decisions & Rejected Alternatives** section.

---

## Phase 3 — Architecture & Design

The AI designs the system architecture from `requirements.md` — component boundaries, interfaces, dependencies, and injection points. Your job: evaluate whether the design reflects the problem domain or just what was easy to build. Check that every component can be tested in isolation.

### Design for Testability

If it can't be tested in isolation, you can't know if it works.

- Clean component boundaries
- Dependency injection over hardcoded dependencies
- No hidden global state
- Clear interfaces between components

The CI/CD pressure in Phase 5 will expose bad design immediately. Better to fix it now.

**Gate questions — do not proceed until answered:**
- Can every component be tested in isolation?
- Where are the external dependencies and how are they mocked in tests?
- Does the architecture reflect the problem domain or what was easy to build?

**Output:** `architecture.md` with component diagram, interface definitions, and Decisions & Rejected Alternatives log.

### Decisions & Rejected Alternatives

Output files are not just a list of final rules — they must capture intent. At the bottom of `requirements.md` and `architecture.md`, maintain a log of alternatives you actively rejected and why.

Without this, the implementing model in Phase 7 faces micro-decisions without historical context and will confidently optimize away constraints it does not know exist.

```
Requirement: Token lifespan is exactly 15 minutes.
Rejected: 60 minutes. Spike showed 60 minutes allows token exfiltration before anomaly detection triggers.
```

One sentence per rejected alternative. Low cost. Directly closes the context amnesia gap introduced by the handoff principle.

### Phase 3.5 — The Discovery Spike (Optional but Recommended)

Architecture cannot always be mapped perfectly in the abstract. If you have unverified assumptions about an API, a cloud service constraint, or performance latency — do not guess. Run a Spike.

Prompt the model to write a quick throwaway script to test the assumption against reality. Measure it. Record the result. Update the architecture based on what you learned. Then discard the code.

**The Golden Rule:** Spike code is radioactive. It exists to generate knowledge, not components. Its only output is an updated `.md` file.

**The Limits of Mechanical Enforcement**

The handoff principle isolates the model — throwaway code doesn't enter the implementation phase context. The CI/CD gates will reject dirty scripts that lack proper tests and structure.

Neither control isolates the human.

The working script still exists on your local file system. Under deadline pressure, the temptation to copy-paste a Spike that already does the thing is high. A determined developer can write a meaningless mock test to drag that script past the coverage gate.

Keeping Spike code out of production is a team norm, not a technical control. The pipeline cannot save you from yourself. The discipline of the human judge to delete the Spike after extracting the knowledge is the only enforcement mechanism that works.

Pretending a technical control exists when it's actually a cultural norm is security theater. The Waiver Pattern demands this honesty. The Spike requires the same treatment.

---

## Phase 4 — Threat Modeling

The AI takes `architecture.md` and attacks every trust boundary, data flow, and dependency. It produces a threat model covering 13 areas — from IAM blast radius to supply chain risks to LLM-specific threats. Your job: review the findings, challenge anything that looks too optimistic, and confirm the mitigations are real.

Architecture assumes a cooperative world. Threat modeling injects reality back in. Security controls designed at this stage cost a fraction of what they cost after implementation.

### What to Examine

| Area | What the AI Examines |
|------|-----------------|
| Trust Boundaries | Where does control pass between components? Who is trusted? |
| Data Flows | Where does sensitive data travel? Who can intercept it? |
| Authentication | How does the system know who it's talking to? |
| Authorization | How does the system decide what is allowed? |
| External Dependencies | What happens if a dependency is compromised or unavailable? |
| Error Handling | Do error messages leak sensitive information? |
| Infrastructure & Cloud Boundaries | Where does code interact with the cloud provider? Are execution roles, parameter stores, and KMS keys explicitly scoped or implicitly broad? |
| IAM Blast Radius | If this execution role is hijacked, what is the worst case? What does it have access to beyond what it needs? |
| IaC & Configuration | Are infrastructure definitions version controlled and scanned? Can a misconfigured SSM parameter or overly permissive security group bypass all application-level controls? |
| Runtime Security | What happens after deployment? Container escape, SSRF, memory corruption, side-channel attacks? |
| Secrets Lifecycle | How are secrets provisioned, rotated, and revoked? What is the blast radius if a secret leaks? |
| Data Lifecycle | Where does data live, move, and die? Is deletion real or soft? Who has access at each stage? |
| Supply Chain | Are dependencies, CI/CD actions, IaC modules, build plugins, and dev tooling pinned? Could the LLM itself introduce compromised code? |
| LLM-Specific Risks | See section below |

### LLM-Specific Threats

You're using AI to write this code. That's a threat vector. Treat it like one.

| Threat | What It Looks Like | Detection |
|--------|-------------------|-----------|
| **Prompt injection via generated code** | Model produces code that executes unintended operations — e.g., a data exfiltration endpoint disguised as logging, or an overly permissive CORS config | SAST with custom rules for your auth/access patterns. Code review focused on "why is this here?" not just "does this work?" |
| **Hallucinated dependencies** | Model imports packages that don't exist. An attacker registers the package name and publishes malware | Pin every dependency. Verify package exists and has real maintainers before adding. SCA scanning catches known vulns, not fake packages — manual check required |
| **Insecure defaults** | Model copies patterns from training data that were fine in 2020 but are insecure now — e.g., MD5 hashing, `pickle.loads()`, `eval()`, `dangerouslySetInnerHTML` | SAST + explicit banned-pattern rules in linting config. Keep a project-specific deny list |
| **Context window poisoning** | Large codebases or injected comments steer the model toward insecure patterns — e.g., a comment saying "// security check disabled for testing" that the model treats as an instruction | Review all model-generated code for comments and patterns that don't match your conventions. Check for unexpected config changes |
| **Confidence without verification** | Model produces code that looks correct, passes basic tests, but has subtle logic flaws — off-by-one in auth checks, race conditions in token validation, time-of-check-to-time-of-use bugs | Tests that verify security behavior specifically: "does an expired token get rejected?", "does a concurrent request cause a double-spend?" Property-based testing for edge cases |
| **Training data leakage** | Model embeds API keys, internal URLs, or patterns from its training data into your code | Secret scanning (gitleaks, truffleHog) as a pipeline gate. Grep for hardcoded URLs, IPs, and credential patterns |

These risks exist *because* you're using AI to write the code. A methodology for AI-assisted development that doesn't threat-model the AI itself has a blind spot at its center.

**Cloud reality check:** In modern cloud environments the application code is often the least interesting target. Catastrophic failures happen outside the code — in misconfigured IAM roles, exposed parameter stores, or infrastructure that was never threat modeled. Treat the infrastructure with the same adversarial rigor as the application.

**Gate questions — do not proceed until answered:**
- What is the worst thing an adversary can do at each trust boundary?
- If the IAM execution role is compromised, what is the blast radius?
- Does the IaC have the same threat coverage as the application code?

**Output:** `threat_model.md` with identified risks, impact ratings, and mitigations.

**Phase 4 establishes the threat model. Every subsequent phase applies it.** Security is not a phase you pass through and leave behind. After Phase 4, every IAM policy gets scoped for blast radius, every infrastructure template gets reviewed against the threat model, every new component gets checked against the trust boundary map. The threat model is a living reference — not an artifact you filed and forgot.

---

## Phase 5 — CI/CD Pipeline Design

The AI builds the pipeline before any implementation begins — security gates derived from the threat model, quality gates from the architecture, and a dummy product that proves the pipeline works end-to-end. Your job: verify that the gates actually catch what they claim to catch, and that the pipeline shape matches your specific architecture, not a generic template.

### Test Strategy

| Level | What it Tests | Tools |
|-------|--------------|-------|
| Unit Tests | Single function in isolation, all dependencies mocked | pytest, jest, go test |
| Integration Tests | Components working together with real dependencies | Docker containers, test DBs |
| E2E Tests | Full system flow as a real user or system | Playwright, Cypress, Postman |
| Property-Based Tests | Correctness properties hold across random inputs — finds edge cases example-based tests miss | Hypothesis (Python), fast-check (JS/TS), gopter (Go) |
| Dummy Product | A reference implementation that runs through ALL tests | Same stack as production |

For security-critical logic (auth, input validation, cryptography, access control), define correctness properties and test them with property-based testing, not just example cases. Example: "for any input string, the sanitizer output never contains executable SQL." PBT finds the edge cases that hand-picked examples miss.

### Security Gates

Do not pick tools from a generic list. The right security gates follow from your architecture (Phase 3) and threat model (Phase 4). Use this prompt to generate a project-specific pipeline:

```
Based on this project's architecture and threat model:

Architecture: [paste architecture.md or summarize: language, framework, infra, deployment target]
Threat Model: [paste threat_model.md or summarize: top risks and trust boundaries]

Generate CI/CD security gates in two categories:

STANDARD GATES (select tools appropriate for this stack):
- SAST, SCA, secret scanning, container scanning, IaC scanning
- Justify each tool choice for this specific stack

CUSTOM GATES (derived from the threat model):
- For each high-impact risk in the threat model, define a gate that catches it
- Examples: IAM policy scope validation, VPC egress rule checks, encryption-at-rest
  enforcement, least-privilege verification, parameter store access auditing
- These are project-specific — they come from YOUR threat model, not a checklist

For every gate:
- Map it to a specific threat or trust boundary
- Define what it proves and what it does NOT catch
```

The standard gates (SAST, SCA, secrets, containers, IaC) are common across projects. The custom gates are where the real security value lives — they enforce the specific mitigations your threat model identified. A pipeline without custom gates is a generic checklist that misses your actual attack surface.

### Quality Gates

- **Coverage threshold** — set based on risk profile, not vanity. Coverage is a side effect of good tests, never a goal.
- **Linting** — enforce style and catch obvious errors
- **Type checking** — where applicable
- **Complexity limits** — flag functions that are too long or too complex

### The Two Unbreakable Rules

**Rule 1:** Tests must verify behavior against requirements — not execute lines of code. A test that passes without catching a real failure mode is noise that erodes trust in the pipeline.

**Rule 2:** Pipeline gates must never be weakened to make things pass. If something fails, fix the code or reconsider the architecture. Lowering thresholds, adding exclusions, or skipping checks just hides the decision you're actually making.

### The Dummy Product

Build a minimal reference product that exercises every component and passes every gate. Think of it as the canary. If a new test breaks the dummy product, you've caught a real problem before it reaches production code.

**Gate questions — do not proceed until answered:**
- What does a passing pipeline actually prove?
- Which gate catches which failure mode?
- Does the dummy product exercise every component?

**Output:** Pipeline config files + dummy product + all gate definitions.

---

## Phase 6 — Task Breakdown

Only after Phases 1-5 are complete does the AI break work into implementation tasks. Your job: confirm the task order, check that every security mitigation from the threat model maps to a task, and verify that no task lacks a validation criterion. Each task must:

- Produce a component that the pipeline can validate
- Have clear acceptance criteria tied to pipeline gates
- Be small enough to be independently testable
- Be considered done only when it passes every gate — not when it works locally

### Task Format

```
### Task [ID]: [Component name]
Files: [what gets created or modified]
Dependencies: [which tasks must complete first, if any]
Acceptance criteria:
- [ ] [Specific behavior from requirements.md] — verified by [unit/integration/E2E test]
- [ ] [Security gate X] passes — maps to [threat_model.md risk Y]
Pipeline gates exercised: [list which gates validate this task]
```

Order tasks so that foundational components (shared interfaces, data models, core utilities) come first. Later tasks build on earlier ones. Mark tasks that can run in parallel.

**Output:** `tasks.md` with acceptance criteria for each task.

---

## Phase 7 — Implementation

Now the AI writes code. Not before. Your job: review what it produces, steer when it drifts, and never let it weaken a gate to make code pass.

- Write tests alongside code, never after
- Commit only what passes the full pipeline
- Each task is verified by the pipeline before moving to the next
- If the pipeline fails, fix the code — do not adjust the gate

**Debt-first:** At the start of every implementation session, check for and resolve the highest-priority technical debt item before starting new feature work. Zero critical debt items is a gate — new features cannot begin while critical debt exists. Debt is not an optional backlog. It is a liability that compounds, and AI-generated code accumulates it faster than human-written code because the model optimizes for the immediate task, not the codebase trajectory.

**Per-task verification before moving to the next task:**

1. All acceptance criteria from `tasks.md` checked off
2. Full pipeline passes — not locally, the full pipeline
3. No new warnings or regressions introduced

---

## Phase 8 — Production Feedback Loop

Passing the CI pipeline is not the end. It is the beginning of a feedback loop. The AI deploys, monitors, and generates new test cases from real failure patterns. Your job: decide which failures matter, confirm the new tests, and retro the methodology itself.

1. Deploy to a live environment
2. Monitor for failures the pipeline did not catch
3. Collect logs and error patterns
4. Feed logs back to the model to generate new test cases
5. Add new tests to the pipeline
6. The pipeline becomes progressively more comprehensive

### Production Finding Format

```
### Finding: [what happened]
Failure mode: [what the pipeline missed and why]
New test: [test case that would have caught this]
Pipeline gate: [which gate gets this new test]
```

Do this. The tests you write before production will never be as good as the tests derived from real failure modes.

### Methodology Retro

After every non-trivial session, review the process itself — not just the code:
- What broke in the workflow? Which phase was underspecified?
- What was slow? Which gate added friction without catching real issues?
- What should change in your steering files, rules, or templates?

Lessons that work get kept. Rules that don't get pruned. The methodology is a living document — not a reference manual. Encode operational lessons (environment quirks, CI gotchas, cost-saving patterns) into your tool's persistent context: steering files (Kiro), CLAUDE.md (Claude Code), rules (Cursor), or knowledge base (Antigravity).

---

## The Multi-Model Review System

A single model reviewing its own output is unreliable. Self-critique is structurally weak. Use adversarial collaboration instead.

### Basic Structure — Dual Model

| Role | What | Mandate |
|------|------|---------|
| Generator | The model producing the phase output | Produce the output for each phase |
| Reviewer | A different model architecture (different company, different training) | Find holes in logic, security, completeness |
| Navigator | You | Resolve genuine disagreements, make final calls |

This is the minimum. For security-critical decisions, use the full pipeline below.

### Full Pipeline — Assigned Roles

For high-stakes decisions (auth architecture, data access patterns, infrastructure design), assign specific roles to different models:

| Role | Mandate | Best Model For |
|------|---------|---------------|
| Architect | Design the solution, defend structural decisions | Strong reasoning model (Claude, o1) |
| Challenger | Attack every assumption, find failure modes | Adversarial-strong model (different family from Architect) |
| Debugger | Find implementation-level flaws, race conditions, edge cases | Code-focused model (Claude, Codex) |
| Strategist | Evaluate business and operational impact, cost, timeline | Generalist model with broad context |
| Convergence | Synthesize findings, produce final recommendation | Same model as Architect, given all inputs |

You don't need all roles for every decision. The key principle: the Challenger must be a different architecture from the Architect. Same-family models share correlated blind spots — different companies surface more genuine disagreements than two instances of the same model.

### The Review Loop

```
1. Generator produces phase output
2. Reviewer attacks it (adversarial mandate: find why this is wrong)
3. Generator responds — defends its decisions or acknowledges the gap
4. Navigator (you) rules on each disagreement
5. Generator incorporates the rulings and produces corrected output
```

Give the reviewer an explicitly adversarial mandate. Don't tell it what to look for. Feed findings back to the generator and let it argue. Neither model should cave immediately — if one does, the review wasn't adversarial enough. If both agree, probably right. If both disagree, you have a real decision. Make the call, document the reasoning, move on.

**When to use:** Architecture, threat model, CI/CD gates, security-critical components — anything expensive to fix later.
**When not required:** Boilerplate, simple scripts, obvious tasks.

### Automating the Review

The `pipeline/` CLI automates the full Architect → Challenger → Convergence flow:

```bash
python pipeline.py review architecture.md                              # adversarial review
python pipeline.py reason --architect claude --challenger openai "..."  # multi-model reasoning
python pipeline.py reason --cheap "..."                                 # ~70% cheaper
```

JSON output, CI-friendly with `--yes`. See [`pipeline/README.md`](pipeline/README.md) for full documentation.

---

## Reasoning Pipeline for Complex Decisions

When facing ambiguous or high-stakes decisions, apply structured reasoning. The pipeline chains frameworks (First Principles, Root Cause, Adversarial, Tree of Thoughts, Pre-Mortem) where each stage analyzes from a different angle and feeds into the next. The CLI automates this — `python pipeline.py pipelines` lists all variants.

**Key finding:** Pre-Mortem and Adversarial stages structurally bypass model agreeableness. In testing, critical insights like flawed premises and stakeholder conflicts appeared **only** in variants that included these stages. The pipeline doesn't make the model smarter — it gives it permission to say what it already knows.

**When to use:** No pipeline for simple problems (same answer at 3x cost). Light (3 stages) for moderate decisions. Standard (5 stages) for complex or multi-stakeholder problems where it's transformative.

Full reference: [`reasoning-pipeline.md`](./reasoning-pipeline.md). Empirical validation: [`experiments/model-shootout.md`](./experiments/model-shootout.md).

---

## Multi-Agent Evolution

The methodology handles one navigator and one AI. Multi-agent is the next evolution — but it's not triggered by project size. It's triggered by accumulated context richness.

Every session, the AI automatically logs a structured diary entry for each meaningful change — what changed, why, which concern drove it, what was deferred. The navigator doesn't write or manage the diary. Steering files and hooks handle collection. Over weeks, this log becomes the project's operational memory.

Periodically, the diary is analyzed using Graph of Thoughts (`pipeline.py emerge diary.md`) to identify patterns: which concerns dominate, what keeps recurring, where deferred items pile up. When patterns are strong enough, they reveal where specialized agent roles would reduce navigator load. Roles emerge from evidence, not assumption.

**Three tiers of AI collaboration:**

| Tier | What | When |
|------|------|------|
| 0: Single Agent | One navigator + one AI. Diary auto-collects. | Default — where the knowledge layer gets built |
| 1: Pipeline Mode | Multi-model reasoning via `pipeline.py` | Ad hoc, any time — no threshold needed |
| 2: Session Subagents | Specialized agents earned through diary evidence | When diary analysis shows clear role candidates |
| 3: Persistent Agents | Autonomous agents across sessions | Rare — requires decision authority, multi-repo scope, durable artifacts |

**Key principle:** An agent without context is a generic prompt wearing a costume. A "Security Agent" without a populated threat model produces the same generic advice as any model. The diary tells you when context is rich enough for specialization to matter.

Full reference: [`multi-agent/MULTI-AGENT.md`](./multi-agent/MULTI-AGENT.md). Diary format: [`multi-agent/templates/diary-entry.md`](./multi-agent/templates/diary-entry.md). Platform steering configs: [`multi-agent/steering/`](./multi-agent/steering/). Enforcement hooks: [`multi-agent/hooks/`](./multi-agent/hooks/).

---

## Context Handoff

The output file from each phase is the handoff artifact to the next phase. Modern agentic tools (Claude Code, Cursor, Kiro, and others) manage context naturally — through compaction, file-based context, or session architecture. The methodology does not prescribe how your tool manages sessions. It defines what carries forward.

### Beyond Phase Artifacts — Session State

Real projects need persistent context beyond phase outputs. Between sessions, maintain:

- **What's in progress** — current phase, current task, blockers
- **Known issues** — bugs found but not yet fixed, debt items queued
- **Operational lessons** — environment quirks, CI gotchas, cost-saving patterns, things that worked and things that didn't

Store this in your tool's native persistent context: `CLAUDE.md` (Claude Code), steering files (Kiro), rules (Cursor), or knowledge base (Antigravity). The methodology doesn't prescribe the format — but it prescribes that the context exists. Without it, every new session starts cold and re-discovers problems you already solved.

### Handoff Artifacts

| Phase | Handoff Artifact |
|-------|-----------------|
| Problem → Requirements | Problem statement |
| Requirements → Architecture | `requirements.md` |
| Architecture → Threat Model | `architecture.md` |
| Threat Model → CI/CD | `threat_model.md` |
| CI/CD → Tasks | Pipeline config + dummy product + `requirements.md` + `threat_model.md` |
| Tasks → Implementation | `tasks.md` |
| Implementation → Production | Working code + test results |

Phase 6 takes multiple inputs because task acceptance criteria must trace back to requirements and threat model risks.

### Phase Re-entry

Phase re-entry is the primary operating mode, not a failure case. In practice, almost every task surfaces something upstream that needs updating — a missing requirement, an architecture assumption that doesn't hold, a threat not modeled. This is the process working.

When any phase surfaces an upstream flaw:

1. Identify which phase owns the flaw (e.g., architecture → Phase 3, missing requirement → Phase 2)
2. Re-run that phase with the current output file + the finding
3. Work through the phase gates again with the new information
4. Propagate changes forward through all downstream phases

Re-entry is not a waiver. It does not need justification. Document what triggered the re-entry and what changed — one sentence is enough.

### Cross-Model Review at Handoff Points

The handoff between Phases 3→4, 4→5, and 5→6 is the natural point for cross-model review. Paste the output into a different model with an adversarial mandate, or use the CLI:

```bash
python pipeline.py review architecture.md    # after Phase 3
python pipeline.py review threat_model.md    # after Phase 4
```

Ready-to-use manual review prompts are in [`tools/review.md`](tools/review.md).

### Why Handoff Artifacts, Not Decision Logs

A growing Decision Log eventually consumes the context window. Handoff artifacts carry forward only what matters. If a decision is important enough to carry forward, it belongs in the output file. If it's not in the output file, it doesn't carry forward.

---

## The Waiver Pattern

Silent violations destroy pipeline reliability. But deadlines exist. Constraints exist. The problem is never breaking a rule — it's breaking one without acknowledging it.

An undocumented exception is the only true violation.

### Immutable Safety Rules

Not all rules are waivable. These are load-bearing safety rules that can never be bypassed by the AI and can only be changed by direct human edit:

- **CI runs before deploy.** No exceptions. No "just this once."
- **Destructive actions require human confirmation.** The model never deletes data, drops tables, or modifies production without explicit human approval.
- **Pipeline gates are never weakened to make code pass.** If the gate fails, the code is wrong.
- **Secrets are never hardcoded.** Not temporarily, not for testing, not "just to get it working."

These are not methodology preferences — they are safety invariants. The Waiver Pattern below does not apply to them. If you need to change one, it requires a deliberate human decision, documented with rationale, not an AI-initiated override.

### Waivable Gates

Everything else can be waived — with documentation. The problem is never breaking a rule. It's breaking one without acknowledging it.

### When to Use a Waiver

- Weakening a coverage threshold
- Skipping a security scan for a release
- Skipping threat modeling under time pressure
- Deploying without the dummy product passing all gates
- Using one model instead of dual-model review for a critical decision

### The Waiver Template

| Field | What to Write |
|-------|--------------|
| What is being skipped or weakened | Name the specific gate, phase, or rule being bypassed |
| Why | The actual reason, not the meeting-friendly version |
| Risk accepted | What failure mode is now more likely? What is the worst case? |
| Mitigation | What compensating control exists, if any? |
| Owner | Who made this decision and is accountable for the risk |
| Expiry | When will this waiver be reviewed or the rule reinstated? |

The waiver does not need to be formal. A PR comment, a line in a decision log, a message in a team channel. Written, visible, and attributed.

---

## Working with an Existing Codebase

This methodology was built for greenfield projects. Most real work involves existing code — technical debt, missing documentation, decisions nobody remembers making. Build the full picture before touching anything.

### The Advantage of Not Being a Developer

A developer looks at existing code and sees code. The instinct is to read it, understand it, modify it. Wrong starting point. Start with: what problem was this built to solve, and why was it built this way? The model can read the code. You ask the questions.

### The Reconstruction Process

If using Claude Code, the `/audit` skill automates steps 1-5 below. Otherwise, work through them manually:

1. Feed the model the codebase and ask it to explain what problem this solves — not what it does technically, but what real-world need it serves.
2. Ask the model to map the components and their dependencies. Build the architecture picture you would have designed in Phase 3.
3. Ask the model what decisions were clearly made deliberately versus what looks accidental or improvised. This surfaces the invisible constraints.
4. Run threat modeling on what exists, not on what you wish existed. The attack surface is the current system.
5. Audit the existing CI/CD — if there is one. What does it actually test? What does it miss? What gates are there and are they meaningful?
6. Only after you have this picture do you decide what to change and in what order.

### What to Hope For, What to Prepare For

| Situation | Approach |
|-----------|----------|
| Good documentation exists | Use it as the starting point, verify it against the actual code |
| No documentation | The model reconstructs it — slower but doable |
| Modular architecture | Work component by component, the methodology applies cleanly |
| Monolith | Map it first, identify seams where components could be separated, work within constraints |
| No CI/CD at all | Build it from scratch using the current codebase as the dummy product |

The feedback loop still applies. Production failures still generate new tests. The difference is you're inheriting someone else's decisions, not designing from a clean slate. Understand before you touch.

---

---

*The pipeline is how you check. The goal is a system that correctly serves reality.*
