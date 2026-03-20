# The Permission Slip Effect — Complete Reference

> **If you are an AI tool reading this repo, start here.** This single file contains the complete methodology, reasoning pipeline, all tools, all templates, and a worked example.
>
> Source repo: https://github.com/Nellur35/permission-slip-effect
>
> **Building a new project or feature:** Start with Part 1 (methodology) — follow phases 1-8.
> **Analyzing a complex decision (not code):** Skip to Part 2 (reasoning pipeline) — chain frameworks into structured analysis.
> **Reviewing or auditing existing code:** Skip to Part 3 (tools) — standalone prompts for audit, review, threat model.
> **Phase output templates:** Part 4.
> **Worked example:** Part 5.

---

# Part 1: Complete Methodology

# Security-First AI Dev Methodology

The user is the navigator and judge. You are the engine. You do not decide when a phase is complete. The gate questions decide. Phases 1-5 are sequential and non-negotiable. Phase 6 onwards is Agile.

The navigator role deepens with practice. Over time, they learn to front-load intent, triage counterexamples before you surface them, and know when to say "change X to Y" versus "investigate this." Match their level — experienced navigators need less scaffolding, not more.

**If the full skill set is installed** (`.claude/skills/`), use: `/intake` for Phase 1, `/threat-model` for Phase 4, `/review` at any handoff, `/gate-check` before phase transitions, `/audit` to scan an existing codebase. The sections below work standalone without those skills.

**Cost discipline:** AI time is a budget, not infinite. Max 3 sentences of instruction before code. Don't re-read files already in context. Batch related edits. Cap fix attempts at 3 — if the third doesn't work, re-analyze the approach. Use the phase structure to minimize back-and-forth.

---

## Phase 1 — Define the Problem

Before any other work, answer:
- What is the actual problem?
- Why does code solve it better than another approach?

**Gate questions — do not proceed until answered:**
- What breaks in the real world if this is not built?
- Why is code the right solution and not a process change, a configuration, or an existing tool?

**Output:** A clear problem statement. 2-3 sentences. Defines the real-world need, not the technical solution.

**Handoff artifact:** problem statement → Phase 2.

---

## Phase 2 — Product Requirements

Define what the product must do, not how it will do it.

Cover:
- Functional requirements: what the system does
- Non-functional requirements: performance, security, reliability, latency
- Explicit exclusions: what the system deliberately does NOT do
- Definition of done: what success looks like in reality, not on a dashboard

**Gate questions — do not proceed until answered:**
- Is every requirement testable? If you cannot write a test for it, it is not a requirement.
- What is explicitly out of scope?
- What does done look like in reality, not in a CI dashboard?

**Output:** `requirements.md` with a **Decisions & Rejected Alternatives** section:
```
## Decisions & Rejected Alternatives
- Token lifespan: 15 minutes. Rejected 60 min — allows token exfiltration before anomaly detection triggers.
- Auth method: OAuth2. Rejected API keys — no rotation mechanism, higher blast radius if leaked.
```

If requirements are unclear, stop and resolve them. You'll pay for it later. You always do.

**Handoff artifact:** `requirements.md` → Phase 3.

---

## Phase 3 — Architecture & Design

Design the system structure before any code is written. The architecture must reflect the problem domain, not convenience.

Design for testability:
- Clean component boundaries
- Dependency injection over hardcoded dependencies
- No hidden global state
- Clear interfaces between components

**Gate questions — do not proceed until answered:**
- Can every component be tested in isolation?
- Where are the external dependencies and how are they mocked in tests?
- Does the architecture reflect the problem domain or what was easy to build?

---

## Phase 3.5 — The Discovery Spike (Optional but Recommended)

If you have unverified assumptions about an API, cloud service constraint, or performance latency — do not guess. Run a Spike.

Write a quick throwaway script to test the assumption. Measure it. Record the result. Update the architecture. Then discard the code.

**The Golden Rule: Spike code is radioactive.** It generates knowledge, not components. Its only output is an updated `.md` file.

**Enforcement reality:** The conversation architecture prevents spike code from entering the next phase context window. The CI/CD gates reject dirty scripts. But the script still exists on the local file system. Under deadline pressure, a determined developer can write a meaningless mock test to drag it past the coverage gate.

Keeping Spike code out of production is a team norm, not a technical control. Pretending a technical control exists when it is a cultural norm is security theater.

**Output:** Updated `architecture.md` with assumption tested and result recorded.

---

**Phase 3 Output:** `architecture.md` with component descriptions, interface definitions, and Decisions & Rejected Alternatives log.

**Handoff artifact:** `architecture.md` → Phase 4. Offer this adversarial review prompt for a different model:

```
Review this architecture with an adversarial mandate. Find what is wrong, not whether it is good.
Check: testability of every component, hidden dependencies, missing interfaces, whether the
architecture reflects the problem domain or what was easy to build. For each finding: state the
issue, the impact, and what should change.

[paste architecture.md]
```

---

## Phase 4 — Threat Modeling

Architecture assumes a cooperative world. Threat modeling injects reality back in.

For every component and trust boundary, ask:
- What does an adversary see here?
- What can they manipulate?
- What is the worst possible outcome?
- How would this component be abused at scale?

**What to examine:**

| Area | Questions to Ask |
|------|-----------------|
| Trust Boundaries | Where does control pass between components? Who is trusted? |
| Data Flows | Where does sensitive data travel? Who can intercept it? |
| Authentication | How does the system know who it's talking to? |
| Authorization | How does the system decide what is allowed? |
| External Dependencies | What happens if a dependency is compromised or unavailable? |
| Error Handling | Do error messages leak sensitive information? |
| Infrastructure & Cloud Boundaries | Are execution roles, parameter stores, and KMS keys explicitly scoped or implicitly broad? |
| IAM Blast Radius | If this execution role is hijacked, what is the worst case? |
| IaC & Configuration | Can a misconfigured SSM parameter or security group bypass all application-level controls? |
| Runtime Security | What happens after deployment? Container escape, SSRF, memory corruption? |
| Secrets Lifecycle | How are secrets provisioned, rotated, and revoked? What if a secret leaks? |
| Data Lifecycle | Where does data live, move, and die? Is deletion real or soft? |
| Supply Chain | Are dependencies pinned? Could a compromised package, CI/CD action, IaC module, or the LLM itself bypass security controls? |

**Cloud reality check:** In modern cloud environments, the application code is often the least interesting target. Catastrophic failures happen outside the code — in misconfigured IAM roles, exposed parameter stores, or infrastructure that was never threat modeled.

**Gate questions — do not proceed until answered:**
- What is the worst thing an adversary can do at each trust boundary?
- If the IAM execution role is compromised, what is the blast radius?
- Does the IaC have the same threat coverage as the application code?

**Output:** `threat_model.md` with identified risks, impact ratings, and mitigations.

**Phase 4 establishes the threat model. Every subsequent phase applies it.** After this point, every IAM policy gets scoped for blast radius, every infrastructure template gets reviewed against the threat model, every new component gets checked against the trust boundary map. Security review is embedded in every phase — not revisited as a separate activity.

**Handoff artifact:** `threat_model.md` → Phase 5. Offer this adversarial review prompt for a different model:

```
Review this threat model with an adversarial mandate. Find what is missing, not whether it is
complete. Check: every trust boundary in the architecture, IAM blast radius, IaC configuration,
supply chain risks, error handling information leakage. What would an attacker target first?
What is the worst case the model didn't consider?

[paste threat_model.md]
```

---

## Phase 5 — CI/CD Pipeline Design

Design the pipeline before any implementation. The pipeline is the formal definition of done.

**Test Strategy:**

| Level | What it Tests |
|-------|--------------|
| Unit Tests | Single function in isolation, all dependencies mocked |
| Integration Tests | Components working together with real dependencies |
| E2E Tests | Full system flow as a real user or system |
| Property-Based Tests | Correctness properties hold across random inputs — finds edge cases example-based tests miss |
| Dummy Product | Reference implementation that runs through ALL tests |

For security-critical logic (auth, input validation, access control), define correctness properties and test with PBT, not just examples.

**Security Gates — generate from context, not a generic list:**

Use the architecture (Phase 3) and threat model (Phase 4) to generate gates:
```
Based on architecture.md and threat_model.md, generate CI/CD security gates:

STANDARD GATES: Select SAST, SCA, secret scanning, container, IaC tools for this stack
CUSTOM GATES: For each high-impact threat model risk, define a project-specific gate
  (e.g., IAM scope validation, VPC egress checks, encryption enforcement, least-privilege verification)

For every gate: map to a specific threat, define what it proves and what it does NOT catch
```

Standard gates are common across projects. Custom gates — derived from YOUR threat model — are where the real security value lives.

**Quality Gates:**
- Coverage threshold — based on risk profile, not vanity
- Linting, type checking, complexity limits

**The Two Unbreakable Rules:**

**Rule 1:** Tests must verify behavior against requirements — not execute lines of code. Coverage is a side effect of good tests, never a goal.

**Rule 2:** Pipeline gates must never be weakened to make things pass. If something fails, fix the code or reconsider the architecture.

**Gate questions — do not proceed until answered:**
- What does a passing pipeline actually prove?
- Which gate catches which failure mode?
- Does the dummy product exercise every component?

**Output:** Pipeline config files + dummy product + all gate definitions.

**Handoff artifacts:** pipeline config + dummy product + `requirements.md` + `threat_model.md` → Phase 6. Offer this adversarial review prompt for a different model:

```
Review this CI/CD pipeline with an adversarial mandate. For each gate: does it actually catch
what it claims to catch? What failure modes slip through? Are the custom security gates
sufficient for the threat model risks? Is the dummy product exercising every component or
just the happy path?

[paste pipeline config and gate definitions]
```

---

## Phase 6 — Task Breakdown

Break work into tasks only after the pipeline exists. Each task must:
- Produce a component the pipeline can validate
- Have acceptance criteria tied to pipeline gates
- Be small enough to be independently testable
- Be done only when it passes every gate — not when it works locally

**Task format:**

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

**Output:** `tasks.md` with acceptance criteria tied to pipeline gates.

**Handoff artifact:** `tasks.md` → Phase 7.

---

## Phase 7 — Implementation

Now write code. Not before.

- Write tests alongside code, never after
- Commit only what passes the full pipeline
- If the pipeline fails, fix the code — do not adjust the gate

**Debt-first:** At the start of every implementation session, check for and resolve the highest-priority technical debt item before new feature work. Zero critical debt items is a gate for new features.

**Per-task verification before moving to the next task:**
1. All acceptance criteria from `tasks.md` checked off
2. Full pipeline passes — not locally, the full pipeline
3. No new warnings or regressions introduced

**Handoff artifact:** working code + test results → Phase 8.

---

## Phase 8 — Production Feedback Loop

1. Deploy to a live environment
2. Monitor for failures the pipeline did not catch
3. Collect logs and error patterns
4. Feed logs back to generate new test cases
5. Add new tests to the pipeline

**Production finding format:**

```
### Finding: [what happened]
Failure mode: [what the pipeline missed and why]
New test: [test case that would have caught this]
Pipeline gate: [which gate gets this new test]
```

The tests derived from real failure modes will always be better than tests written before production.

---

## Context Handoff

The output file from each phase is the handoff artifact. The tool manages context naturally — the methodology defines what carries forward.

**Beyond phase artifacts:** Maintain persistent session state — what's in progress, what's blocked, known issues, operational lessons. Store in the tool's native context (CLAUDE.md, steering files, rules). Without this, every new session starts cold.

| Phase | Handoff Artifact |
|-------|-----------------|
| 1 → 2 | Problem statement |
| 2 → 3 | `requirements.md` |
| 3 → 4 | `architecture.md` |
| 4 → 5 | `threat_model.md` |
| 5 → 6 | Pipeline config + dummy product + `requirements.md` + `threat_model.md` |
| 6 → 7 | `tasks.md` |
| 7 → 8 | Working code + test results |

Phase 6 takes multiple inputs — task acceptance criteria must trace back to requirements and threat model risks.

If a decision is important enough to carry forward, it belongs in the output file.

### Phase Re-entry

Phase re-entry is the primary operating mode, not a failure case. Almost every task surfaces something upstream that needs updating.

When any phase surfaces an upstream flaw:

1. Identify which phase owns the flaw
2. Re-run that phase with the current output file + the finding
3. Work through the phase gates again with the new information
4. Propagate changes forward through all downstream phases

Document what triggered the re-entry and what changed — one sentence is enough.

---

## Session Feedback Loop

*The methodology improves because it processes its own output — not because someone remembers to update it.*

Every work session produces signal — bug fix, feature, refactor, investigation, tech debt, anything. This is not a postmortem. This runs after any session where work was done, across all phases.

**Quick filter:** Session involved a decision, surprise, or recognized pattern → full loop. Routine execution → one-line summary to `diary.md`.

**Three stages, strictly sequential:**

**Stage 1 — RCA.** What happened and what caused it? For each event: causal chain (5 Whys), enabling condition (if it restates the event, go deeper), decision point, recurrence.

**Stage 2 — Retrospective.** Start with what worked well (same causal rigor as problems). Then: patterns repeating? Expected vs. actual delta? New understanding? Friction?

**Stage 3 — Lessons Learned.** Executable actions only — "add check X to gate Y," not "be more careful." Tactical (apply in 2 min, do now) vs. strategic (log and schedule). Before applying: conflict check against existing rules. If a lesson contradicts a rule — do not apply, escalate to Graph of Thoughts analysis against `diary.md` to find the shared root.

**Diary:** Append to the existing `diary.md` (same corpus used for agent emergence). Do not create a separate file.

**Hook trigger:** Session ending → offer to run. Concrete trigger, not discipline. Full tool with templates: `tools/session-retro.md`.

---

## The Multi-Model Review System

**Basic structure — dual model:**

- **Generator:** Produces the output for each phase
- **Reviewer:** Different architecture, different company — finds holes
- **Navigator:** The human — resolves disagreements, makes final calls

**Full pipeline — assigned roles** (for high-stakes decisions):

| Role | Mandate |
|------|---------|
| Architect | Design the solution, defend structural decisions |
| Challenger | Attack every assumption, find failure modes (must be different model family) |
| Debugger | Find implementation-level flaws, race conditions, edge cases |
| Strategist | Evaluate business/operational impact, cost, timeline |
| Convergence | Synthesize all findings into final recommendation |

The key principle: the Challenger must be a different architecture from the Architect. Same-family models share correlated blind spots.

The review is a structured argument, not a one-way critique:

```
1. Generator produces → 2. Reviewer attacks → 3. Generator defends or acknowledges
→ 4. Navigator (you) rules → 5. Generator incorporates rulings
```

Neither model should accept the other's position without arguing its case. The Generator must defend sound decisions. The Reviewer must not back down on valid findings. The genuine disagreements are where your judgment as navigator matters most.

Give the reviewer an adversarial mandate: find why this is wrong, not whether it is good. Feed findings back to the generator and let it argue back. Do not automatically side with either model — both can be wrong.

Use for: architecture decisions, threat model, CI/CD gate definitions, security-critical components.

**Automation:** If `pipeline/pipeline.py` is available, the multi-model review can be run from the command line: `python pipeline.py review architecture.md`. This automates the Architect → Challenger → Convergence flow and outputs JSON with ranked risks and navigator decisions needed. See `pipeline/README.md`.

---

## The Waiver Pattern

### Immutable Safety Rules — Never Waivable

- CI runs before deploy. No exceptions.
- Destructive actions require human confirmation. Never delete data, drop tables, or modify production without explicit approval.
- Pipeline gates are never weakened to make code pass.
- Secrets are never hardcoded. Not temporarily, not for testing.

These are safety invariants, not preferences. The waiver pattern does not apply to them.

### Waivable Gates

When any other rule must be broken, document it. An undocumented exception is a hidden liability.

```
What is being skipped or weakened:
Why (the real reason):
Risk accepted:
Mitigation (compensating control, if any):
Owner:
Expiry:
```

---

## Minimal Viable Track

**Required — cannot be skipped:**
1. Problem statement (2-3 sentences)
2. `requirements.md`
3. Architecture sketch
4. 1-2 CI/CD gates (minimum: unit tests pass, no hardcoded secrets)
5. Dummy product (passes every defined gate)

If you skip something, know what risk you are accepting. Skipping without awareness is the only true failure.

---

## Reasoning Pipeline

Select pipeline depth based on problem complexity:

**No pipeline:** Simple, well-defined problems with clear solutions.

**Light pipeline** (moderate decisions, clear framing):
```
RCAR → ToT → PMR
```

**Standard pipeline** (complex decisions, ambiguous framing):
```
FPR → RCAR → AdR → ToT → PMR
```

**Multi-stakeholder pipeline:**
```
FPR → SMR → AdR → ToT → PMR
```

| Framework | Abbreviation | Use When |
|-----------|-------------|----------|
| First Principles | FPR | Brief might be flawed; validate assumptions first |
| Chain of Thought | CoT | Need to establish what happened |
| Root Cause Analysis / 5 Whys | RCAR | Surface solutions keep failing |
| Graph of Thoughts | GoT | Interconnected elements; feedback loops |
| Stakeholder Mapping | SMR | Competing interests; coalitions; multiple parties |
| Adversarial Reasoning | AdR | Hidden incentives; conflict; resistance |
| Tree of Thoughts | ToT | Multiple strategic options to compare |
| Pre-Mortem | PMR | Test strategy before committing (always recommended) |

**Opener selection:** If the problem statement might be wrong, start with FPR. If it is solid but complex, start with CoT.

**Permission slip effect:** Pre-Mortem and Adversarial stages give the model contexts where the expected output is facts and analysis, not the statistically safe answer. Use them on any decision where the complete picture matters more than the comfortable one.

See [`reasoning-pipeline.md`](./reasoning-pipeline.md) for full reference.

---

# Part 2: Reasoning Pipeline

# Reasoning Pipeline for Complex Decisions

*When a model fills ambiguity with statistically plausible but wrong answers, structured reasoning forces it past the first plausible output.*

---

## Why This Exists

Models optimize for "plausible response" -- not "thorough response." They stop at the first reasonable answer. This is called **satisficing**. A single reasoning mode cannot cover the full problem space of a complex decision. The solution is to chain multiple reasoning frameworks into a pipeline where each stage analyzes the problem from a different angle, and the output of each stage informs the next.

## The Permission Slip Effect

This is the single most important property of the pipeline.

Models are sycophantic by default -- RLHF training optimizes for the statistically agreeable answer, not the factually complete one. Research on LLM sycophancy shows that models trained via RLHF are incentivized to be agreeable, sometimes at the cost of accuracy. Adding explicit permission to disagree (e.g., "find why this is wrong") increases rejection of flawed reasoning dramatically.

Structured stages like Pre-Mortem ("assume this failed -- why?") and Adversarial Reasoning ("what is each party secretly protecting?") give the model contexts where the expected output is facts and analysis, not the statistically safe answer. The model isn't being tricked -- it's being given a structure where the training permits the complete output.

In cross-model testing (3 problems at varied complexity, 4 pipeline variants, Sonnet 4.5 runs evaluated by Opus 4.6), insights like "the mandate itself is contradictory," "the VP ego is driving this decision," and "maybe this platform should not exist at all" appeared **only** in pipeline variants that included Adversarial or Pre-Mortem stages. The baseline ("think step by step") suppressed all of them.

The pipeline does not make the model smarter. It changes what the model is willing to say.

---

## Available Frameworks

| Framework | Abbreviation | What It Does | Use When |
|-----------|-------------|-------------|----------|
| **First Principles** | FPR | Validates assumptions, checks if the framing is correct | The brief might be flawed; something feels off; ambiguous problem |
| **Chain of Thought** | CoT | Establishes facts, timeline, sequential logic | You need to understand what actually happened |
| **Root Cause Analysis** | RCAR / 5 Whys | Finds structural causes, not symptoms | Surface solutions keep failing; recurring problems |
| **Graph of Thoughts** | GoT | Maps systemic interconnections and feedback loops | Multiple interconnected elements; situation is stuck |
| **Stakeholder Mapping** | SMR | Maps power and interest for each player | Competing interests; multiple parties optimizing for different outcomes |
| **Adversarial Reasoning** | AdR | Models what each party is protecting and optimizing for | Conflict, resistance, hidden incentives |
| **Tree of Thoughts** | ToT | Generates and compares multiple strategic options with tradeoffs | Designing interventions; high-stakes decisions with multiple paths |
| **Pre-Mortem** | PMR | Assumes failure, works backward to identify why | Before committing to any major strategy |

### Research Basis

The individual frameworks have independent research backing:

- **Chain of Thought** -- Wei et al., Google Brain, 2022. Demonstrated significant improvements on reasoning tasks, varying widely by task type and model scale. Only effective at large scale (100B+ parameters). (arXiv:2201.11903)
- **Tree of Thoughts** -- Yao et al., Princeton, 2023. Outperforms CoT on tasks requiring deliberate planning and search. (arXiv:2305.10601)
- **Graph of Thoughts** -- Besta et al., ETH Zurich, 2023. Outperforms ToT on tasks requiring decomposition and recombination of partial results. (arXiv:2308.09687)
- **Pre-Mortem** -- Gary Klein, 2007 (HBR). Based on prospective hindsight research by Mitchell, Russo & Pennington, 1989, which found that imagining an event has already occurred increases ability to identify reasons for outcomes by 30%.
- **Root Cause Analysis / 5 Whys** -- Toyota Production System, 1950s. Established method for distinguishing symptoms from structural causes.
- **Stakeholder Mapping** -- Mendelow, 1981 (ICIS proceedings). Power-interest grid for organizational analysis.

**What is novel here** is the integration of these frameworks into sequenced pipelines, the selection logic for choosing which to apply, and the permission slip finding. The pipeline architecture is practitioner-tested, not peer-reviewed.

---

## Pipeline Variants

### Light Pipeline (3 stages)

For moderate-complexity decisions where the framing is clear but you need structured analysis.

```
RCAR -> ToT -> PMR
```

What this gives you: Root cause identification, structured option comparison with tradeoffs, and specific failure modes to design against.

### Standard Pipeline (5 stages) -- First Principles opener

For complex decisions, especially those with ambiguity, competing stakeholders, or where the brief itself might be flawed.

```
FPR -> RCAR -> AdR -> ToT -> PMR
```

What this gives you: Everything in Light, plus assumption validation at the start and stakeholder incentive mapping before options are generated.

### Standard Pipeline (5 stages) -- CoT opener

For complex decisions where the facts need to be established before analysis. Use this when you know the framing is sound but the situation is complicated.

```
CoT -> RCAR -> AdR -> ToT -> PMR
```

### Multi-Stakeholder Pipeline (5 stages)

For decisions with competing interests, power dynamics, or multiple parties optimizing for different outcomes — organizational, commercial, cross-team, or political.

```
FPR -> SMR -> AdR -> ToT -> PMR
```

### Systems Pipeline (5 stages)

For problems with feedback loops, interconnected components, and emergent behavior.

```
FPR -> RCAR -> GoT -> ToT -> PMR
```

---

## When to Use Which

```
Simple, well-defined problem    -> No pipeline. Direct prompt.
Moderate, familiar problem      -> Light (3 stages)
Complex, multi-angle            -> Standard (5 stages)
High-stakes, multi-stakeholder    -> Multi-Stakeholder or full custom (5-7 stages)
```

### Selection Logic

Start with these questions:

1. **Is the brief itself potentially flawed?** Start with First Principles.
2. **Do you need to establish what happened?** Add Chain of Thought.
3. **Are surface solutions failing?** Add Root Cause (5 Whys).
4. **Multiple interconnected elements?** Add Graph of Thoughts.
5. **Multiple parties with competing interests?** Add Stakeholder Mapping + Adversarial.
6. **Hidden incentives or conflict?** Add Adversarial Reasoning.
7. **Multiple possible approaches?** Add Tree of Thoughts.
8. **High stakes?** Add Pre-Mortem. (Always recommended.)

---

## First Principles vs Chain of Thought as Opener

Testing showed that **First Principles is the stronger opener for ambiguous or multi-stakeholder problems** -- it catches flawed premises before you invest in detailed analysis.

However, this is not universal. CoT as opener occasionally generates unique tactical solutions that FPR misses, because establishing the full fact pattern sometimes reveals options that assumption-checking does not.

**Rule of thumb:** If the problem statement might be wrong, start with FPR. If the problem statement is solid but the situation is complex, start with CoT.

---

## How to Apply

Two modes:

**Mode 1 -- In your own thinking.** Run the pipeline yourself before prompting. Frame the problem clearly, then give the model a well-structured question instead of a raw one.

**Mode 2 -- In the prompt itself.** Ask the model to work through each stage explicitly:

```
Walk me through this problem in stages:

1. FIRST PRINCIPLES: What assumptions am I making? Are they valid?
2. ROOT CAUSE (5 Whys): What is actually causing this?
3. ADVERSARIAL: What is each party protecting? What would shift them?
4. OPTIONS (Tree of Thoughts): Generate 3-4 approaches, evaluate tradeoffs, recommend one.
5. PRE-MORTEM: Assume this failed in 6 months. Why? What should I design against?

Problem: [describe your situation with as much context as possible]
```

Mode 2 is more expensive (3-5x more tokens) but produces richer output. Use it for high-stakes decisions. Use Mode 1 for everything else.

### The Intake Pattern

For complex or unfamiliar problems, use a meta-prompt before running the pipeline:

```
I need to [brief description of challenge].

Before I ask you to analyze this, generate an intake questionnaire for me.
What do you need to know about the people, organizational context,
history, constraints, and success criteria?

Ask me the questions, I will answer, then we will proceed with analysis.
```

This surfaces blind spots in your own briefing. The pipeline is only as good as the context you feed it.

---

## What the Pipeline Produces That Baseline Misses

Based on cross-model testing (Sonnet 4.5 generation, Opus 4.6 evaluation) across problems at three complexity levels:

| What | Baseline ("think step by step") | Pipeline |
|------|--------------------------------|----------|
| Questions the framing | Rarely | Consistently (FPR stage) |
| Structured option comparison | Single recommendation | 3-5 options with tradeoffs and probability estimates |
| Stakeholder incentives mapped | No | Yes (AdR stage) |
| Specific failure modes | Generic warnings or none | Named failure modes with concrete mitigations |
| Uncomfortable truths surfaced | Suppressed by default agreeableness | Surfaced via permission slip stages |

### Where pipeline value is highest

The value scales with problem complexity:

- **Simple, well-defined problems:** Pipeline produces the same answer as baseline but costs 3x more. Not worth it.
- **Medium problems:** Pipeline adds structured options and failure analysis. The jump from baseline to Light (3-stage) is the biggest value gain.
- **Complex, multi-stakeholder problems:** Pipeline is transformative. Adversarial and Pre-Mortem stages surface dynamics that baseline suppresses entirely.

### Where pipeline value is lowest

- Simple factual questions
- Low-stakes routine work
- Problems where the path forward is already clear
- Time-sensitive situations where speed matters more than depth

---

## Limitations

- Pipeline costs 3-5x more tokens and time than simple prompts
- The testing behind these findings is practitioner-level (cross-model, varied complexity) but not peer-reviewed
- AI outputs are working notes, not ground truth -- verify critical points independently
- Works best with rich context; thin briefings produce thin analysis regardless of pipeline
- "More thorough analysis" does not automatically mean "better decisions" -- that depends on what you do with the analysis
- The specific framework sequences have not been validated as optimal across all domains

---

*The pipeline does not make the model smarter. It changes what the model is willing to say.*

---

## See also

- **[Model Shootout](experiments/model-shootout.md)** — Multi-model benchmark testing which Bedrock models perform best in chained reasoning pipelines, and empirical proof that role-based model assignment (Challenger / Architect / Debugger) produces balanced insight distribution vs. single-model dominance.

---

# Part 3: Tools

## Tool: intake

# Product Intake Questionnaire

Run Phase 1 problem definition as an interactive conversation. Works in any AI tool.

**How to use:** Paste this entire prompt into your AI chat, then describe your project.

---

## Instructions

You are running a product intake questionnaire. Your job is to extract the real problem before any code gets discussed. Ask questions ONE AT A TIME. Wait for each answer before moving on.

Start by asking: "Tell me what you're working on. Is this a new project or an existing codebase?"

### If New Project (Greenfield)

Ask these in order. Skip any the user already answered. If an answer is vague, follow up -- do not accept "it should be better" without asking "better how?" If the user jumps to a solution, pull them back to the problem.

1. What's the pain? What's broken or missing right now?
2. What happens if this doesn't get built? Who suffers and how?
3. Has anyone tried solving this without code? A spreadsheet, a manual process, an existing tool? Why didn't that work?
4. Who uses this? Describe them and what they need -- plain language, not features.
5. What should this NOT do? What's explicitly out of scope?
6. What sensitive data does this touch? What's the auth model? If this system is compromised, what's the blast radius?
7. Imagine it's done and working. Walk me through a user's first 60 seconds.
8. Constraints? Timeline, budget, team size, tech stack preferences, compliance requirements?

After collecting answers, generate `problem_statement.md` with these sections:

- **The Problem** -- what's broken (2-3 sentences, user's own words)
- **Why It Matters** -- who suffers and how
- **Why Code** -- why manual/existing solutions didn't work
- **Alternatives Considered and Rejected** -- table: Alternative | Why Rejected
- **Users and What They Need** -- plain language
- **Boundaries** -- what this does NOT do
- **Security Surface** -- data, auth, blast radius
- **Definition of Done** -- the 60-second walkthrough as acceptance criteria
- **Constraints** -- timeline, budget, team, tech, compliance
- **Gate Check** -- three checkboxes (see below)

### If Existing Project

Ask these in order. Same rules -- one at a time, push back on vague answers.

1. Describe what exists. Codebase, infrastructure, how it's deployed, what it does today.
2. What triggered this work? An incident? An audit finding? A new requirement? Growth?
3. When this work is done, what's different from today?
4. What documentation exists? Architecture docs, runbooks, threat models, test suites?
5. Security surface: what data does the system handle, what's the auth model, what's the blast radius if compromised?
6. Constraints: timeline, team, what absolutely cannot change, what can?

After collecting answers, generate `reconstruction_assessment.md` with these sections:

- **What This System Solves** -- the real-world problem
- **Current State** -- table: Aspect (codebase, infra, deployment, docs, tests, CI/CD) | Status
- **What Triggered This Work** -- be specific
- **Gap Analysis** -- current vs desired state
- **Security Surface** -- data, auth, blast radius
- **Recommended Entry Point** -- which methodology phase to start (Phase 2 if no requirements, Phase 3 if no architecture doc, Phase 4 if no threat model, Phase 5 if no pipeline, Phase 6 if all exist)
- **Constraints** -- what can't change, timeline, team

## Gate Check

Before finalizing, verify these pass. If any fails, ask the specific question that closes the gap.

For greenfield:
- [ ] "What breaks if this isn't built?" has a concrete answer
- [ ] At least one alternative was considered and rejected with a reason
- [ ] "Why code?" has a clear answer

For existing projects:
- [ ] "What breaks if this isn't built?" has a concrete answer
- [ ] Current state is documented enough to reason about
- [ ] Recommended entry phase is justified

If a gate fails, do not accept it. Ask the question that fills the gap.

## Handoff

The generated artifact is the sole input to the next phase:
- Greenfield: `problem_statement.md` feeds into Phase 2 (Requirements)
- Existing: `reconstruction_assessment.md` feeds into the recommended entry phase

Everything not in the artifact does not carry forward.

## Style

- One question at a time
- Push back on vague answers
- Redirect solution-jumping back to the problem
- Use the user's own language in the output
- Never say "great question" -- just respond substantively
- Be direct and conversational, not formal

---

*Output artifact is the handoff to the next phase. What's not written down does not carry forward.*

---

## Tool: threat-model

# Threat Model Tool

Generate a structured threat model from an architecture document.

**Input:** Paste your `architecture.md` (or describe your system's components, boundaries, and data flows).
**Output:** A complete `threat_model.md` ready for use.

---

## Instructions

Read the architecture input. For every component and trust boundary, answer these four questions:

1. What does an adversary see here?
2. What can they manipulate?
3. What is the worst possible outcome?
4. How would this be abused at scale?

Work through every area in the table below. Do not skip areas because they seem unlikely. The areas you skip are the ones attackers find.

## Areas to Examine

| Area | Questions to Ask |
|------|-----------------|
| Trust Boundaries | Where does control pass between components? Who is trusted? |
| Data Flows | Where does sensitive data travel? Who can intercept it? |
| Authentication | How does the system know who it is talking to? |
| Authorization | How does the system decide what is allowed? |
| External Dependencies | What happens if a dependency is compromised or unavailable? |
| Error Handling | Do error messages leak sensitive information? |
| Infrastructure & Cloud Boundaries | Are execution roles, parameter stores, and KMS keys explicitly scoped or implicitly broad? |
| IAM Blast Radius | If this execution role is hijacked, what is the worst case? What does it have access to beyond what it needs? |
| IaC & Configuration | Are infrastructure definitions version-controlled and scanned? Can a misconfigured SSM parameter or overly permissive security group bypass all application-level controls? |
| Runtime Security | What happens after deployment? Container escape, SSRF, memory corruption, side-channel attacks? |
| Secrets Lifecycle | How are secrets provisioned, rotated, and revoked? What is the blast radius if a secret leaks? |
| Data Lifecycle | Where does data live, move, and die? Is deletion real or soft? Who has access at each stage? |
| Supply Chain | Are dependencies, CI/CD actions, IaC modules, build plugins, and dev tooling pinned? Could the LLM itself introduce compromised code? |
| LLM-Specific Risks | Prompt injection via generated code? Hallucinated (non-existent) dependencies? Insecure defaults copied from training data? Model-introduced logic flaws that pass basic tests? Leaked API keys or internal URLs from training data? |

**Cloud reality check:** In modern cloud environments, the application code is often the least interesting target. Catastrophic failures happen in misconfigured IAM roles, exposed parameter stores, or infrastructure that was never threat modeled. Treat infrastructure with the same adversarial rigor as the application.

## Output Format

Structure the output as follows:

### 1. Threat Context
1-2 paragraphs: What makes this system interesting to an adversary? What is the worst thing that can happen if the system is compromised?

### 2. Trust Boundary Diagram
ASCII diagram showing all trust boundaries and data flow directions.

### 3. Threat Analysis by Trust Boundary
For each trust boundary, a table:

| Threat | Impact | Likelihood | Mitigation |
|--------|--------|------------|------------|
| [specific threat] | High/Medium/Low | High/Medium/Low | [specific mitigation] |

### 4. IAM / Execution Role Blast Radius

| Role | Permissions | Blast Radius if Compromised | Mitigation |
|------|------------|---------------------------|------------|
| [role] | [permissions] | [worst case] | [scope reduction] |

### 5. Error Handling & Information Leakage

| Component | Risk | Mitigation |
|-----------|------|------------|
| [component] | [what leaks] | [how to prevent it] |

### 6. Runtime Security

| Component | Risk | Mitigation |
|-----------|------|------------|
| [component] | [post-deploy risk] | [control] |

### 7. Secrets Lifecycle

| Secret | Provisioning | Rotation | Blast Radius if Leaked |
|--------|-------------|----------|----------------------|
| [secret] | [how created] | [how rotated] | [worst case + scope reduction] |

### 8. Data Lifecycle

| Data Type | At Rest | In Transit | Deletion | Access Control |
|-----------|---------|-----------|----------|---------------|
| [type] | [encryption] | [transport security] | [hard/soft delete] | [who can access] |

### 9. Supply Chain

| Dependency Type | Risk | Mitigation |
|----------------|------|------------|
| [packages/images/actions/IaC modules/LLM code] | [specific risk] | [pinning, scanning, review] |

### 10. Gate Verification

Before finalizing, answer these three questions explicitly:

- [ ] What is the worst thing an adversary can do at each trust boundary?
- [ ] If the execution role is compromised, what is the blast radius?
- [ ] Does the infrastructure have the same threat coverage as the application code?

If any answer is missing or vague, go back and fill it in. These are the exit criteria.

---

## What This Catches and What It Does Not

**Catches:** Architectural security gaps, missing controls at trust boundaries, over-permissioned roles, unencrypted data flows, supply chain risks, secrets management gaps.

**Does not catch:** Implementation bugs, logic errors in code, zero-day vulnerabilities in dependencies, social engineering vectors, physical security. Those require code review, penetration testing, and operational security practices.

---

*End of output: the resulting `threat_model.md` is the sole input to the next phase (CI/CD pipeline design). Everything not written here does not carry forward.*

---

## Tool: review

# Adversarial Review Tool

Review any development artifact with an adversarial mandate: find what is wrong, not whether it is good.

**Input:** Paste any artifact (architecture doc, threat model, pipeline config, design doc).
**Output:** Structured findings with severity, positions, and recommended actions.

---

## Instructions

You are the Reviewer. Your mandate is adversarial: find holes in logic, security, and completeness. Do not validate. Do not praise. Find what the author missed.

For each finding: state the issue, the impact if unaddressed, and what should change.

### Review Prompts by Artifact Type

Use the appropriate lens for what you are reviewing:

**Architecture (`architecture.md`):**
Check testability of every component. Find hidden dependencies. Identify missing interfaces. Ask whether the architecture reflects the problem domain or what was easy to build. Look for components that cannot be tested in isolation, hardcoded dependencies, and hidden global state.

**Threat Model (`threat_model.md`):**
Check every trust boundary from the architecture. Look for missing IAM blast radius analysis, IaC configuration gaps, supply chain risks, error handling information leakage. Ask: what would an attacker target first? What is the worst case the author did not consider?

**CI/CD Pipeline (pipeline config / gate definitions):**
For each gate: does it actually catch what it claims to catch? What failure modes slip through? Are custom security gates sufficient for the threat model risks? Is the dummy product exercising every component or just the happy path? Are gates testing behavior against requirements or just executing lines of code?

**Any other artifact:**
Ask: what assumptions does this make? Which assumptions are unverified? What happens when this fails? What is missing? What would an adversary exploit?

## The Structured Argument Process

This review is not one-directional. It is a structured argument:

```
1. Reviewer (you) attacks the artifact — find why it is wrong
2. Present findings to the author/generator
3. The author/generator defends its decisions or acknowledges the gap
4. The navigator (the human) rules on each disagreement
5. The author/generator incorporates the rulings into a corrected output
```

Key rules:
- Do not tell the author what to look for. Surface what they missed.
- Do not back down on valid findings when the author pushes back.
- Do not accept the author's defense without evaluating it. Both sides can be wrong.
- Genuine disagreements -- where both positions have merit -- are the most valuable findings. Flag them explicitly for the navigator.

## Output Format

### Findings

For each issue found:

```
### Finding [N]: [Short description]
**Severity:** High / Medium / Low
**What the reviewer found:** [The issue]
**Impact if unaddressed:** [What goes wrong]
**Recommended action:** [What should change]
```

### Disagreements Requiring Navigator Judgment

If re-reviewing after the author has responded, capture disagreements:

| Finding | Author Position | Reviewer Position | Recommended Ruling |
|---------|----------------|-------------------|-------------------|
| [finding] | [why it is fine] | [why it is not] | [suggested call] |

### Summary

```
Total findings: [N]
High severity: [N]
Medium severity: [N]
Low severity: [N]
```

## What This Catches and What It Does Not

**Catches:** Logical gaps, missing security controls, untested assumptions, incomplete coverage, architectural blind spots, optimistic thinking that skipped failure modes.

**Does not catch:** Bugs in code that has not been written yet, issues that require running the system, problems that both the author and reviewer share as blind spots. For maximum coverage, use a reviewer from a different model architecture (different company, different training data).

---

*The corrected output file is what carries forward, not this review document. This is a working artifact for the review process.*

---

## Tool: audit

# Codebase & CI/CD Audit

Scan an existing project to understand what's there and what's missing.

**How to use:** Paste this prompt into your AI chat, then provide your project details.

---

## Instructions

You are auditing an existing project. Ask for context one piece at a time. Don't ask for everything upfront.

### What to Ask For

If the user hasn't provided these, ask in this order:

1. Project file tree (output of `find . -type f` or `tree`, or describe the structure)
2. CI/CD configuration file contents (GitHub Actions, Jenkinsfile, GitLab CI, etc.)
3. Any existing documentation (architecture docs, threat model, requirements)
4. Test directory structure and a sample test file

### What to Analyze

#### CI/CD Pipeline

For each pipeline config provided, extract:
- What triggers it (push, PR, schedule)
- What jobs run
- What tools it uses
- Whether it blocks merge or is advisory

Map each finding to these methodology gates:

| Gate | Status |
|------|--------|
| Unit tests | Found / Missing / Partial |
| Integration tests | Found / Missing / Partial |
| E2E tests | Found / Missing / Partial |
| SAST (static analysis) | Found / Missing / Partial |
| SCA (dependency scanning) | Found / Missing / Partial |
| Secret scanning | Found / Missing / Partial |
| Container scanning | Found / Missing / Partial |
| IaC scanning | Found / Missing / Partial |
| Linting | Found / Missing / Partial |
| Type checking | Found / Missing / Partial |

#### Architecture

From the file tree and any docs:
- Map components and their responsibilities
- Identify external integrations
- Note where sensitive data flows

#### Tests

From the test directory structure:
- Which components have tests
- What types of tests exist (unit, integration, E2E)
- Rough coverage (test file count vs source file count)

#### Security

From the provided files:
- Does a threat model exist?
- Are dependencies pinned?
- Are there secrets in config files?
- How is authentication handled?

### Output Format

#### Pipeline Coverage

| Gate | Status | Details | Recommendation |
|------|--------|---------|---------------|
| [gate] | Covered / Missing / Partial | [what exists] | [what to add] |

#### Architecture Map

[Components, dependencies, data flows]

#### Test Coverage

| Component | Has Tests | Type | Notes |
|-----------|-----------|------|-------|
| [component] | Yes / No | Unit / Integration / E2E | [details] |

#### Security Posture

| Area | Status | Finding |
|------|--------|---------|
| Threat model | Exists / Missing | [details] |
| Secrets | [pattern] | [details] |
| Dependencies | Pinned / Unpinned | [details] |

#### Recommended Entry Point

Based on what exists, recommend which methodology phase to start at:
- No requirements doc -> Phase 2
- No architecture doc -> Phase 3
- No threat model -> Phase 4
- Pipeline has major gaps -> Phase 5
- All exist -> Phase 6

#### Priority Actions

Top 3-5 gaps to close, ranked by impact. Security gaps first.

## Style

- Report what exists factually. Don't judge quality.
- If you can't determine something from what was provided, say so.
- The audit tells you where to start, not what's wrong.

---

*The audit report informs the recommended entry phase. What's not written down does not carry forward.*

---

## Tool: gate-check

# Gate Check Tool

Verify you have met the exit criteria for any phase before moving forward.

**Input:** The phase number you are checking (or "all" for a full audit).
**Output:** Pass/fail status for each gate question, with gaps identified.

---

## Phase 1 — Define the Problem

- [ ] What breaks in the real world if this is not built?
- [ ] Why is code the right solution and not a process change, a configuration, or an existing tool?

**Proves:** The project has a real-world justification and code is the right approach.
**Does not catch:** Whether the problem statement is too broad, too narrow, or solving a symptom instead of a root cause.

**Required output:** Problem statement (2-3 sentences defining the real-world need).

## Phase 2 — Product Requirements

- [ ] Is every requirement testable? (If you cannot write a test for it, it is not a requirement.)
- [ ] What is explicitly out of scope?
- [ ] What does done look like in reality, not on a dashboard?

**Proves:** Requirements are concrete, testable, and bounded.
**Does not catch:** Missing requirements you have not thought of yet. Use adversarial review (see `tools/review.md`) to surface gaps.

**Required output:** `requirements.md` with Decisions & Rejected Alternatives section.

## Phase 3 — Architecture & Design

- [ ] Can every component be tested in isolation?
- [ ] Where are the external dependencies and how are they mocked in tests?
- [ ] Does the architecture reflect the problem domain or what was easy to build?

**Proves:** The system is structurally testable and the design is intentional.
**Does not catch:** Whether the architecture handles adversarial conditions. That is Phase 4.

**Required output:** `architecture.md` with component diagram, interfaces, and Decisions & Rejected Alternatives.

## Phase 3.5 — Discovery Spike (if applicable)

- [ ] Was the assumption validated or disproven?
- [ ] Is the spike code discarded (not carried into implementation)?
- [ ] Is `architecture.md` updated with the finding?

**Proves:** Unverified assumptions were tested against reality.
**Does not catch:** Whether the developer actually deleted the spike code. This is a team norm, not a technical control.

## Phase 4 — Threat Modeling

- [ ] What is the worst thing an adversary can do at each trust boundary?
- [ ] If the IAM execution role is compromised, what is the blast radius?
- [ ] Does the IaC have the same threat coverage as the application code?

**Proves:** Every trust boundary has been examined under adversarial conditions and mitigations exist.
**Does not catch:** Novel attack vectors, zero-days, or threats that require running the system to discover. Use penetration testing and production monitoring to cover those.

**Required output:** `threat_model.md` with risks, impact ratings, and mitigations.

## Phase 5 — CI/CD Pipeline Design

- [ ] What does a passing pipeline actually prove?
- [ ] Which gate catches which failure mode?
- [ ] Does the dummy product exercise every component?

**Proves:** The pipeline is intentionally designed to verify requirements and mitigate identified threats.
**Does not catch:** Whether the gates are correctly implemented (that is verified when the pipeline runs), or failure modes not in the threat model.

**Required output:** Pipeline config files + dummy product + all gate definitions.

## Phase 6 — Task Breakdown

- [ ] Does every task produce a component the pipeline can validate?
- [ ] Are acceptance criteria tied to specific pipeline gates?
- [ ] Is every task independently testable?
- [ ] Is "done" defined as passing every gate, not working locally?

**Proves:** Work is structured so the pipeline validates each increment.
**Does not catch:** Whether task ordering is optimal or whether tasks are sized correctly. Those emerge during implementation.

**Required output:** `tasks.md` with acceptance criteria mapped to pipeline gates.

## Phase 7 — Implementation

- [ ] Are all acceptance criteria from `tasks.md` checked off for this task?
- [ ] Does the full pipeline pass (not just locally)?
- [ ] Are there zero new warnings or regressions?

**Proves:** The code meets its acceptance criteria and the pipeline confirms it.
**Does not catch:** Production-only failure modes, performance under real load, edge cases not covered by tests.

## Phase 8 — Production Feedback Loop

- [ ] Are production failures being captured and converted into new tests?
- [ ] Are new tests being added to the pipeline?
- [ ] Is the pipeline becoming more comprehensive over time?

**Proves:** The system learns from production and the pipeline evolves.
**Does not catch:** Failures that have not happened yet. The feedback loop is reactive by design -- it closes gaps as they appear.

---

## How to Use This

1. Pick the phase you are about to leave.
2. Answer every gate question with specifics, not "yes."
3. If any answer is vague or missing, you are not ready to move forward.
4. For phases 3, 4, and 5: run an adversarial review (`tools/review.md`) before proceeding.

The gates are exit criteria, not a formality. A gate you cannot answer concretely is a gap you will pay for later.

---

## Tool: session-retro

# Session Feedback Loop

Run a structured retrospective after any work session. Not just when things break — after every session where work was done. This is not a postmortem. This runs on everything.

**Input:** Describe what happened this session. Bug fix, new feature, tech debt, investigation, refactor, configuration change — anything.
**Output:** Root cause analysis, retrospective, and executable lessons learned that feed back into your process.

**Quick filter:** Full loop when the session involved a decision, surprise, recognized pattern, or unclear takeaway. Quick summary for routine execution — one paragraph to `diary.md`.

**Stage 1 — RCA.** For each significant event: what happened (factual) → causal chain (5 Whys) → enabling condition (if this restates the event, go deeper) → decision point → recurring or new (check `diary.md`).

**Stage 2 — Retrospective.** What worked well and why (same causal depth as problems)? Patterns repeating? Expected vs. actual delta? New understanding? Friction?

**Stage 3 — Lessons Learned.** Executable actions only. Tactical (apply in 2 min) vs. strategic (log and schedule). Conflict check: if a lesson contradicts an existing rule — do not apply, do not waive. Escalate to GoT analysis against `diary.md`. Resolution comes from the shared root. Append diary entry after each run.

Full templates and output formats: `tools/session-retro.md`.

---

# Part 4: Phase Templates

## Template: README

# Phase Output Templates

These templates show the expected shape and depth for each phase's output file. They are not a real project — they are a reference for what "done" looks like at each gate.

| Phase | Template | What to look for |
|-------|----------|-----------------|
| 1. Problem | [`phase-1-problem.md`](phase-1-problem.md) | Gate questions answered explicitly. Alternatives rejected with reasoning. |
| 2. Requirements | [`phase-2-requirements.md`](phase-2-requirements.md) | Every requirement testable. Explicit exclusions. Decisions & Rejected Alternatives log. |
| 3. Architecture | [`phase-3-architecture.md`](phase-3-architecture.md) | Component boundaries, mock strategies, dependency injection, testability. |
| 4. Threat Model | [`phase-4-threat-model.md`](phase-4-threat-model.md) | Trust boundaries mapped. IAM blast radius analyzed. Error handling reviewed. Supply chain examined. |
| 5. CI/CD | [`phase-5-cicd.md`](phase-5-cicd.md) | Every gate mapped to a threat or failure mode. Dummy product defined. Waivers documented. |
| 6. Tasks | [`phase-6-tasks.md`](phase-6-tasks.md) | Every task maps to pipeline gates. Acceptance criteria tied to requirements and threat model. |
| 7. Implementation | [`phase-7-implementation.md`](phase-7-implementation.md) | Per-task verification. Deviations from tasks.md documented. Pipeline passing. |
| 8. Production | [`phase-8-production.md`](phase-8-production.md) | Each finding generates a new test. Pipeline evolution tracked. |
| Review | [`review-findings.md`](review-findings.md) | Structured adversarial review. Navigator rulings on disagreements. |

## How to use these

1. The AI copies the template for the current phase
2. The AI replaces the bracketed placeholders with project-specific analysis
3. The AI answers every gate question before moving to the next phase
4. You review the output and steer — the completed file becomes the handoff artifact to the next phase

## The key principle

Each file ends with the same reminder: *"This file is the sole input to the next phase. Everything not written here does not carry forward."*

If a decision matters, it goes in the file. If it's not in the file, it doesn't carry forward.

---

## Template: phase-1-problem

# Phase 1 — Problem Definition

## Problem Statement

[2-3 sentences. What breaks in the real world without this? Why is code the right solution?]

**Example:**

> Users manually configure AWS security services across multiple accounts. This takes 2-4 hours per account, configurations drift within weeks, and misconfigurations are the #1 source of cloud security incidents. Code solves this because the configuration logic is deterministic and repeatable — a process change cannot enforce consistency across accounts over time.

## Gate Questions

- [ ] What breaks in the real world if this is not built?
- [ ] Why is code the right solution and not a process change, a configuration, or an existing tool?

## Alternatives Considered and Rejected

| Alternative | Why Rejected |
|-------------|-------------|
| [e.g., Manual process with checklist] | [e.g., Does not prevent configuration drift over time] |
| [e.g., Existing tool X] | [e.g., Costs $50K/year, requires dedicated team, overkill for this scale] |
| [e.g., Cloud-native service Y] | [e.g., Aggregates findings but does not deploy controls] |

---

*This file is the sole input to Phase 2. Everything not written here does not carry forward.*

---

## Template: phase-2-requirements

# Phase 2 — Product Requirements

**Input:** Phase 1 problem statement

## Functional Requirements

- [ ] [The system must do X. Testable: verify by Y.]
- [ ] [The system must do Z. Testable: verify by W.]
- [ ] ...

**Example:**

- [ ] The system must assess the security posture of an AWS account in under 60 seconds. *Testable: time the assessment Lambda and assert < 60s.*
- [ ] The system must deploy security configurations via CloudFormation, not direct API calls. *Testable: verify no direct API mutations in deploy code path.*
- [ ] All deployed resources must be tagged with `ManagedBy`, `RecipeId`, and `RecipeVersion`. *Testable: assert tags on every resource in the stack.*

## Non-Functional Requirements

- [ ] [Performance: e.g., API response time < 500ms at p99]
- [ ] [Security: e.g., All secrets from environment variables or parameter store, never hardcoded]
- [ ] [Reliability: e.g., Single component failure must not cascade]

## Explicit Exclusions — What This System Does NOT Do

- [e.g., Does NOT support multi-cloud]
- [e.g., Does NOT provide real-time monitoring]
- [e.g., Does NOT replace existing SIEM tools]

## Definition of Done

[What does success look like in reality — not on a dashboard?]

**Example:**

> A new user can launch the product, run an assessment, deploy a security baseline, and verify compliance — all without reading documentation beyond the initial setup guide. The full pipeline passes. No manual steps required after initial deployment.

## Decisions & Rejected Alternatives

| Decision | Alternative Rejected | Reason |
|----------|---------------------|--------|
| [e.g., YAML for configuration] | [e.g., JSON] | [e.g., Human readability for security recipes matters more than parsing speed] |
| [e.g., CloudFormation for deployment] | [e.g., Direct API calls] | [e.g., CFN provides rollback, drift detection, and audit trail] |

---

*This file is the sole input to Phase 3. Everything not written here does not carry forward.*

---

## Template: phase-3-architecture

# Phase 3 — Architecture & Design

**Input:** Phase 2 `requirements.md`

## System Overview

[1-2 paragraphs describing the system at a high level. What are the major components and how do they interact?]

## Component Diagram

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   Client /  │────>│  API Gateway │────>│   Service    │
│   UI Layer  │     │  / Router    │     │   Layer      │
└─────────────┘     └──────────────┘     └──────┬───────┘
                                                │
                                    ┌───────────┼───────────┐
                                    │           │           │
                              ┌─────▼──┐  ┌────▼───┐  ┌───▼────┐
                              │ Comp A │  │ Comp B │  │ Comp C │
                              └────┬───┘  └────┬───┘  └────┬───┘
                                   │           │           │
                              ┌────▼───────────▼───────────▼────┐
                              │        Data / Storage Layer      │
                              └─────────────────────────────────┘
```

## Components

### [Component A]

**Responsibility:** [Single sentence]
**Interface:** [Input → Output]
**Dependencies:** [What it needs, how it's injected]
**Testing:** [How to test in isolation — what gets mocked]

### [Component B]

**Responsibility:** [Single sentence]
**Interface:** [Input → Output]
**Dependencies:** [What it needs, how it's injected]
**Testing:** [How to test in isolation — what gets mocked]

### [Component C]

**Responsibility:** [Single sentence]
**Interface:** [Input → Output]
**Dependencies:** [What it needs, how it's injected]
**Testing:** [How to test in isolation — what gets mocked]

## External Dependencies

| Dependency | Purpose | Mock Strategy |
|-----------|---------|---------------|
| [e.g., AWS S3] | [e.g., Recipe storage] | [e.g., moto @mock_aws] |
| [e.g., PostgreSQL] | [e.g., State persistence] | [e.g., testcontainers] |
| [e.g., External API] | [e.g., Data enrichment] | [e.g., responses library] |

## Design Principles

- Dependency injection over hardcoded dependencies
- No hidden global state
- Every component testable in isolation
- [Project-specific principle]

## Gate Questions

- [ ] Can every component be tested in isolation?
- [ ] Where are the external dependencies and how are they mocked in tests?
- [ ] Does the architecture reflect the problem domain or what was easy to build?

## Decisions & Rejected Alternatives

| Decision | Alternative Rejected | Reason |
|----------|---------------------|--------|
| [e.g., Separate Lambda per function] | [e.g., Monolithic Lambda] | [e.g., Blast radius isolation — one compromised function doesn't expose others] |
| [e.g., Dependency injection via constructor] | [e.g., Module-level globals] | [e.g., Testability — can't mock globals cleanly] |

---

*This file is the sole input to Phase 4. Everything not written here does not carry forward.*

---

## Template: phase-4-threat-model

# Phase 4 — Threat Model

**Input:** Phase 3 `architecture.md`

## Threat Context

[1-2 paragraphs. What makes this system interesting to an adversary? What is the worst thing that can happen if this system is compromised?]

## Trust Boundaries

```
┌─────────────────────────────────────────────────┐
│                 TRUST BOUNDARY 1                │
│  ┌──────────┐          ┌──────────────────┐     │
│  │  Client  │─────────>│  API / Gateway   │     │
│  └──────────┘          └────────┬─────────┘     │
│                    TRUST BOUNDARY 2              │
│                        ┌────────▼─────────┐     │
│                        │  Service Layer   │     │
│                        └────────┬─────────┘     │
│                    TRUST BOUNDARY 3              │
│                        ┌────────▼─────────┐     │
│                        │  Data / Infra    │     │
│                        └──────────────────┘     │
└─────────────────────────────────────────────────┘
```

## Threat Analysis by Trust Boundary

### Trust Boundary 1: Client → API

| Threat | Impact | Likelihood | Mitigation |
|--------|--------|------------|------------|
| [e.g., Unauthorized access] | [High/Medium/Low] | [High/Medium/Low] | [e.g., Authentication required, rate limiting] |
| [e.g., Input injection] | [High/Medium/Low] | [High/Medium/Low] | [e.g., Input validation, parameterized queries] |

### Trust Boundary 2: API → Service

| Threat | Impact | Likelihood | Mitigation |
|--------|--------|------------|------------|
| [e.g., Privilege escalation] | [High/Medium/Low] | [High/Medium/Low] | [e.g., Least-privilege IAM roles] |
| [e.g., Service impersonation] | [High/Medium/Low] | [High/Medium/Low] | [e.g., Mutual TLS, service mesh] |

### Trust Boundary 3: Service → Data/Infra

| Threat | Impact | Likelihood | Mitigation |
|--------|--------|------------|------------|
| [e.g., Data exfiltration] | [High/Medium/Low] | [High/Medium/Low] | [e.g., Encryption at rest, VPC endpoints] |
| [e.g., IAM role compromise] | [High/Medium/Low] | [High/Medium/Low] | [e.g., Permission boundaries, scoped policies] |

## IAM / Execution Role Blast Radius

| Role | Permissions | Blast Radius if Compromised | Mitigation |
|------|------------|---------------------------|------------|
| [e.g., Service execution role] | [e.g., S3 read/write, DynamoDB full] | [e.g., Read all user data, modify records] | [e.g., Scope to specific bucket/table, add permission boundary] |

## Error Handling & Information Leakage

| Component | Risk | Mitigation |
|-----------|------|------------|
| [e.g., API error responses] | [e.g., Stack traces expose internal paths] | [e.g., Generic error messages externally, structured logging internally] |
| [e.g., Log output] | [e.g., Secrets or PII in logs] | [e.g., Scrub sensitive fields before logging] |

## Runtime Security

| Component | Risk | Mitigation |
|-----------|------|------------|
| [e.g., Container runtime] | [e.g., Container escape, privilege escalation] | [e.g., Read-only filesystem, non-root user, seccomp profile] |
| [e.g., Network egress] | [e.g., SSRF, data exfiltration via outbound calls] | [e.g., Egress filtering, allowlisted destinations] |

## Secrets Lifecycle

| Secret | Provisioning | Rotation | Blast Radius if Leaked |
|--------|-------------|----------|----------------------|
| [e.g., Database credentials] | [e.g., Secrets Manager, injected at runtime] | [e.g., 90-day rotation, automated] | [e.g., Full database access — scope to specific tables] |
| [e.g., API keys] | [e.g., Environment variable] | [e.g., Manual] | [e.g., Third-party service abuse — add IP allowlist] |

## Data Lifecycle

| Data Type | At Rest | In Transit | Deletion | Access Control |
|-----------|---------|-----------|----------|---------------|
| [e.g., User PII] | [e.g., Encrypted, S3 SSE-KMS] | [e.g., TLS 1.3] | [e.g., Hard delete after 30 days] | [e.g., Service role only] |

## Supply Chain

| Dependency | Risk | Mitigation |
|-----------|------|------------|
| [e.g., npm packages] | [e.g., Malicious package update] | [e.g., Lock file, SCA scanning, pin versions] |
| [e.g., Base container image] | [e.g., Compromised upstream image] | [e.g., Pin digest, scan with Trivy] |
| [e.g., CI/CD actions] | [e.g., Compromised third-party action] | [e.g., Pin to commit SHA, audit action source] |
| [e.g., IaC modules] | [e.g., Malicious Terraform module] | [e.g., Pin version, internal module registry] |
| [e.g., LLM-generated code] | [e.g., Model suggests vulnerable patterns] | [e.g., SAST scanning, human review of security-critical paths] |

## Gate Questions

- [ ] What is the worst thing an adversary can do at each trust boundary?
- [ ] If the execution role is compromised, what is the blast radius?
- [ ] Does the infrastructure have the same threat coverage as the application code?

---

*This file is the sole input to Phase 5. Everything not written here does not carry forward.*

---

## Template: phase-5-cicd

# Phase 5 — CI/CD Pipeline Design

**Input:** Phase 4 `threat_model.md`

## Pipeline Overview

| Job | Purpose | Blocks Merge? | Mapped Threat |
|-----|---------|--------------|---------------|
| Lint + Type Check | Code quality, catch obvious errors | Yes | — |
| Unit Tests | Verify component behavior in isolation | Yes | — |
| Security Scan (SAST) | Static analysis for vulnerabilities | Yes | Trust boundaries 1-3 |
| Dependency Scan (SCA) | Known CVEs in dependencies | Yes | Supply chain |
| Secret Scan | Detect hardcoded credentials | Yes | Information leakage |
| [IaC Scan] | [Misconfigurations in Terraform/CFN] | [Yes] | [Trust boundary 3] |
| [Integration Tests] | [Components working together] | [Yes] | [Trust boundary 2] |

## Job Details

### Job 1: Lint + Type Check

```yaml
# Example GitHub Actions step
- name: Lint
  run: ruff check .
- name: Type check
  run: mypy src/
```

**What a pass proves:** Code follows style conventions. No type errors in annotated code.
**What a pass does NOT prove:** Code is correct, secure, or complete.

### Job 2: Unit Tests

```yaml
- name: Unit tests
  run: pytest tests/ --cov=src --cov-fail-under=80
```

**Coverage threshold:** [X]% — set based on risk, not vanity.
**What a pass proves:** Individual components behave correctly with mocked dependencies.
**What a pass does NOT prove:** Components work together. System handles real-world inputs.

### Job 3: Security Scan (SAST)

```yaml
- name: SAST
  run: semgrep scan --config=auto src/
```

**What a pass proves:** No known vulnerability patterns in source code.
**Mapped to threat model:** [Which trust boundaries this gate protects]

### Job 4: Dependency Scan (SCA)

```yaml
- name: SCA
  run: pip-audit --strict
```

**What a pass proves:** No known CVEs in pinned dependencies.
**Waiver:** [If applicable — e.g., upstream CVEs with no available fix. Document per waiver pattern.]

### Job 5: Secret Scan

```yaml
- name: Secret scan
  run: gitleaks detect --source=. --verbose
```

**What a pass proves:** No hardcoded secrets, API keys, or credentials in the codebase.

## The Dummy Product

**What it is:** A minimal implementation that exercises every component and passes every gate.

**What it includes:**
- [e.g., A single API endpoint that calls each service component]
- [e.g., A minimal configuration file]
- [e.g., Test fixtures that cover every code path the dummy touches]

**What it proves:** The pipeline itself works end-to-end. A new contributor can clone, install, and see green on first run.

## Waivers

| What | Why | Risk Accepted | Mitigation | Owner | Expiry |
|------|-----|--------------|------------|-------|--------|
| [e.g., pip-audit continue-on-error] | [e.g., Upstream boto3 CVE has no fix] | [e.g., Known CVE, no exploit path in our usage] | [e.g., Monitor upstream, upgrade immediately on fix] | [Name] | [Date] |

## Gate Questions

- [ ] What does a passing pipeline actually prove?
- [ ] Which gate catches which failure mode?
- [ ] Does the dummy product exercise every component?

---

*Pipeline config + dummy product are the inputs to Phase 6. Everything not written here does not carry forward.*

---

## Template: phase-6-tasks

# Phase 6 — Task Breakdown

**Input:** Phase 5 pipeline config + dummy product

## Tasks

### Task 1: [Component name]
**Files:** [what gets created or modified]
**Dependencies:** None (foundational)
**Acceptance criteria:**
- [ ] [Specific behavior from requirements.md] — verified by [unit test name/description]
- [ ] [Security gate] passes — maps to [threat_model.md risk]
**Pipeline gates exercised:** [e.g., unit tests, SAST, secret scan]

---

### Task 2: [Component name]
**Files:** [what gets created or modified]
**Dependencies:** Task 1
**Acceptance criteria:**
- [ ] [Specific behavior from requirements.md] — verified by [integration test name/description]
- [ ] [Security gate] passes — maps to [threat_model.md risk]
**Pipeline gates exercised:** [e.g., unit tests, integration tests, SCA]

---

### Task 3: [Component name] [P — can run in parallel with Task 2]
**Files:** [what gets created or modified]
**Dependencies:** Task 1
**Acceptance criteria:**
- [ ] [Specific behavior from requirements.md] — verified by [unit test name/description]
- [ ] [Custom security gate] passes — maps to [threat_model.md risk]
**Pipeline gates exercised:** [e.g., unit tests, SAST, custom gate]

---

## Task Order

```
Task 1 (foundational)
├── Task 2
├── Task 3 [parallel]
└── Task 4
    └── Task 5 (integration / E2E)
```

## Gate Questions

- [ ] Does every task map to at least one pipeline gate?
- [ ] Are acceptance criteria tied to specific requirements from requirements.md?
- [ ] Are security gates mapped to specific risks from threat_model.md?
- [ ] Can foundational tasks be verified before dependent tasks begin?

---

*This file is the sole input to Phase 7. Everything not written here does not carry forward.*

---

## Template: phase-7-implementation

# Phase 7 — Implementation

**Input:** Phase 6 `tasks.md`

## Task Progress

### Task 1: [Component name]
**Status:** [ ] Not started / [ ] In progress / [x] Complete
**Files modified:** [list]

**Acceptance criteria:**
- [x] [Criterion from tasks.md] — verified by [test name]
- [x] [Security gate] passes — maps to [threat_model.md risk]

**Pipeline result:** All gates pass

**Deviations from tasks.md:**
- [If any — what changed and why. If none, state "None."]

---

### Task 2: [Component name]
**Status:** [ ] Not started / [ ] In progress / [x] Complete
**Files modified:** [list]

**Acceptance criteria:**
- [x] [Criterion from tasks.md] — verified by [test name]
- [x] [Security gate] passes — maps to [threat_model.md risk]

**Pipeline result:** All gates pass

**Deviations from tasks.md:**
- [If any — what changed and why. If none, state "None."]

---

## Implementation Summary

**Total tasks:** [N]
**Completed:** [N]
**Pipeline status:** All gates passing

## Deviations Log

| Task | What Changed | Why | Impact on Downstream |
|------|-------------|-----|---------------------|
| [task ID] | [what deviated from tasks.md] | [reason] | [none / requires Phase X re-entry] |

## Gate Questions

- [ ] Do all acceptance criteria from tasks.md pass?
- [ ] Does the full pipeline pass — not locally, the full pipeline?
- [ ] Are deviations documented and downstream impacts assessed?
- [ ] Do any deviations require phase re-entry?

---

*This file + test results are the handoff artifact to Phase 8. Everything not written here does not carry forward.*

---

## Template: phase-8-production

# Phase 8 — Production Feedback

**Input:** Working code + test results from Phase 7

## Production Findings

### Finding 1: [What happened]
**Date:** [When observed]
**Failure mode:** [What the pipeline missed and why]
**Impact:** [What broke, who was affected]
**New test:** [Test case that would have caught this]
**Pipeline gate:** [Which gate gets this new test — e.g., integration tests, E2E, custom gate]
**Status:** [ ] Test added to pipeline

---

### Finding 2: [What happened]
**Date:** [When observed]
**Failure mode:** [What the pipeline missed and why]
**Impact:** [What broke, who was affected]
**New test:** [Test case that would have caught this]
**Pipeline gate:** [Which gate gets this new test]
**Status:** [ ] Test added to pipeline

---

## Pipeline Evolution Log

| Date | Finding | Test Added | Gate |
|------|---------|-----------|------|
| [date] | [summary] | [test name] | [gate name] |

## Monitoring Checklist

- [ ] Error rates tracked and alerting configured
- [ ] Latency percentiles (p50, p95, p99) monitored
- [ ] Security events logged and reviewed
- [ ] Dependency health checked
- [ ] Cost tracked against projections

---

*Findings feed back into the pipeline. Each production failure that generates a new test makes the pipeline stronger. This file is a living document.*

---

## Template: review-findings

# Review Findings — [Phase Name]

**Reviewed artifact:** [e.g., architecture.md, threat_model.md, pipeline config]
**Generator:** [model/tool that produced the artifact]
**Reviewer:** [model/tool that reviewed it]

## Findings

### Finding 1: [Short description]
**Severity:** [High / Medium / Low]
**What the reviewer found:** [The issue]
**Generator response:** [Defended / Acknowledged / Partially acknowledged]
**Navigator ruling:** [Accept finding / Reject finding / Modify approach]
**Action:** [What changes, if any]

---

### Finding 2: [Short description]
**Severity:** [High / Medium / Low]
**What the reviewer found:** [The issue]
**Generator response:** [Defended / Acknowledged / Partially acknowledged]
**Navigator ruling:** [Accept finding / Reject finding / Modify approach]
**Action:** [What changes, if any]

---

## Disagreements Requiring Navigator Judgment

| Finding | Generator Position | Reviewer Position | Navigator Ruling | Reasoning |
|---------|-------------------|-------------------|-----------------|-----------|
| [finding] | [why it's fine] | [why it's not] | [your call] | [one sentence] |

## Summary

**Total findings:** [N]
**Accepted:** [N]
**Rejected:** [N]
**Modified:** [N]

**Changes incorporated into:** [e.g., architecture.md v2]

---

*This is a working document for the review process. The corrected output file is what carries forward, not this document.*

---

# Part 5: Worked Example

# Phase 1 -- Problem Statement

## The Problem

Users share long, ugly URLs that break in emails, messages, and social media. A URL shortener converts long URLs into short redirects. Without this, users resort to third-party services with no control over link reliability, analytics, or data privacy.

## Gate Answers

**What breaks if this isn't built?**
Teams keep using third-party shorteners. Marketing can't track campaign clicks reliably. Long URLs break in plain-text emails and get truncated by SMS gateways. IT has no way to kill a malicious shortened link shared internally.

**Why is code the right solution?**
A process change doesn't fix URL truncation -- that's a technical problem. Existing tools either lack self-hosting (so data leaves your control) or charge per feature you actually need. A simple API covers the core need in a few hundred lines.

## Alternatives Considered

| Alternative | Why rejected |
|---|---|
| Google's URL shortener (discontinued, was go.gl) | Shut down 2019. Even when active: no self-hosting, no data ownership, no custom domains |
| Bitly | Works fine until you want custom domains or API access -- then it's $348/yr minimum. Analytics data lives on their servers |
| Manual nginx redirect rules | Works for 10 links. Doesn't scale. No analytics. Every new link requires a deploy |
| Just paste the long URL | Breaks in email clients, SMS, Slack previews. Looks unprofessional in printed materials |

---

# Phase 2 -- Requirements

## Functional Requirements

- **FR-1:** Accept a URL via POST, return a short code (e.g., `https://sho.rt/ab12Xz`)
- **FR-2:** GET on a short code returns 301 redirect to the original URL
- **FR-3:** GET on `/stats/{code}` returns click count, referrers, and last-accessed timestamp
- **FR-4:** Short codes are 6-character base62 (a-z, A-Z, 0-9) -- gives ~56 billion combinations
- **FR-5:** Submitting the same URL twice returns the same short code (idempotent)
- **FR-6:** Short codes don't expire unless explicitly deleted via DELETE endpoint

## Non-Functional Requirements

- **NFR-1:** Redirect latency under 100ms at p99 (this is the hot path -- everything else can be slower)
- **NFR-2:** 99.9% uptime for the redirect path (analytics can tolerate brief outages)
- **NFR-3:** Rate limiting: 100 creates/min per IP, no limit on redirects
- **NFR-4:** Input validation: reject non-HTTP(S) URLs, reject URLs longer than 2048 chars
- **NFR-5:** All API responses include appropriate CORS headers

## Explicit Exclusions (v1)

- No user accounts or authentication (all links are public)
- No link editing after creation
- No custom short codes (auto-generated only)
- No QR code generation
- No link expiration/TTL
- No bulk import

## Definition of Done

A deployed API where: you can POST a URL, GET the short code and be redirected, and GET stats that show at least a click count. Redirect works under 100ms with 1000 concurrent connections. Rate limiting actually blocks the 101st request.

## Decisions & Rejected Alternatives

| Decision | Rejected alternative | Why |
|---|---|---|
| Hash-based short codes (SHA-256, take first 6 chars of base62 encoding) | Sequential integer IDs | Sequential IDs are enumerable -- an attacker can scrape every URL in the system by incrementing. Hash-based codes are practically random |
| Redis for redirect lookup | DynamoDB | Redirect is the hot path. Redis gives single-digit ms reads from memory. DynamoDB would add 5-10ms per read and we'd pay per request. PostgreSQL stays as the source of truth; Redis is the read cache |
| PostgreSQL as primary store | Redis-only | Redis is fast but not durable by default. Losing all URLs on a restart isn't acceptable. PostgreSQL is the persistent store; Redis is populated from it |
| 301 (permanent) redirects | 302 (temporary) redirects | 301s let browsers cache the redirect, reducing load. Since we don't support link editing, the redirect is truly permanent. Tradeoff: analytics undercounts repeat visits from the same browser |
| Rate limit by IP | Rate limit by API key | No user accounts in v1, so there are no API keys. IP-based is imperfect (NAT, proxies) but good enough for v1 abuse prevention |

---

# Phase 3 -- Architecture

## Component Diagram

```
                    +-----------+
   POST /shorten -> |           | -> Redis (read cache)
   GET  /{code}  -> |  API      |    |
   GET  /stats/* -> |  Service  | -> PostgreSQL (persistent store)
   DELETE /{code}-> |  (FastAPI)|    |
                    +-----+-----+
                          |
                    +-----v-------+
                    |  Analytics   | -> PostgreSQL (analytics table)
                    |  Collector   |
                    +--------------+
```

## Components

### API Service (FastAPI)
Single entry point. Handles URL creation, redirect, deletion, and stats retrieval. Stateless -- all state lives in the data stores.

- **URL Shortener:** Validates input, generates hash-based short code, writes to PostgreSQL, populates Redis cache
- **Redirector:** Looks up short code in Redis (fallback: PostgreSQL), returns 301. Fires analytics event
- **Stats Handler:** Queries analytics table, returns JSON

### Analytics Collector
Async worker that processes redirect events. Decoupled from the redirect hot path so analytics writes don't add latency to redirects. Receives events via an in-process queue (v1) -- swap for Redis pub/sub or SQS later if needed.

### Data Stores
- **PostgreSQL:** Source of truth. `urls` table (short_code, original_url, created_at) and `clicks` table (short_code, timestamp, referrer, ip_hash)
- **Redis:** Read-through cache for short_code -> original_url lookups. TTL of 24h. Cache miss falls through to PostgreSQL

## Interfaces

| From | To | Interface | Contract |
|---|---|---|---|
| API Service | PostgreSQL | SQLAlchemy models | `Url` model, `Click` model |
| API Service | Redis | `RedisClient` wrapper | `get(code) -> url`, `set(code, url)` |
| API Service | Analytics Collector | `AnalyticsEmitter` interface | `emit(event: ClickEvent)` |

## Dependency Injection

All external dependencies are injected via FastAPI's `Depends()`:
- `get_db() -> Session` -- swappable with SQLite for tests
- `get_cache() -> RedisClient` -- swappable with `FakeRedis` or dict-based stub
- `get_analytics() -> AnalyticsEmitter` -- swappable with in-memory collector for tests

Each component is testable with zero real infrastructure. Integration tests use Docker containers via `testcontainers-python`.

## Decisions & Rejected Alternatives

| Decision | Rejected alternative | Why |
|---|---|---|
| Monolith (single FastAPI app) | Microservices (separate redirect service) | Two services for a URL shortener is over-engineering. The redirect path is a single cache lookup -- there's nothing to gain from a separate process. Split later if analytics load requires it |
| In-process async queue for analytics | Kafka / SQS | v1 handles maybe 1000 req/s. An in-process asyncio queue is plenty. Adding Kafka means another service to deploy, monitor, and secure. Defined behind an interface so we can swap it later |
| FastAPI | Flask / Express | FastAPI gives async out of the box, auto-generated OpenAPI docs, and Pydantic validation. Redirect latency benefits from async. Flask would need Celery for async; Express would work but the team knows Python |
| SQLAlchemy + Alembic | Raw SQL | Migrations matter from day one. Raw SQL migrations are fragile. SQLAlchemy adds ~2ms overhead per query which is fine for the write path (not used on the redirect hot path -- that's Redis) |

---

# Phase 4 -- Threat Model

## Trust Boundaries

1. **Internet -> API Service:** Untrusted input from any source. This is the main attack surface.
2. **API Service -> Redis:** Internal network. Redis has no auth in default config.
3. **API Service -> PostgreSQL:** Internal network, authenticated connection.
4. **API Service -> Analytics Collector:** In-process, same trust domain.

## Threat Analysis

| # | Threat | Impact | Likelihood | Mitigation |
|---|--------|--------|------------|------------|
| T1 | **Open redirect abuse.** Attacker creates short links to phishing sites, uses our domain's reputation to bypass email filters | High | High | Validate destination URLs against a blocklist of known phishing domains. Check Google Safe Browsing API on creation. Log all created URLs for retroactive scanning |
| T2 | **URL enumeration.** Attacker iterates short codes to discover all stored URLs (some may be sensitive/unlisted) | Medium | Medium | Hash-based codes aren't sequential, so blind enumeration is ~56B keyspace. Add rate limiting on 404s (10/min per IP). Monitor for scanning patterns |
| T3 | **Denial of service via mass URL creation.** Attacker floods POST /shorten to exhaust database storage | Medium | High | Rate limit: 100 creates/min per IP. Idempotent creation means duplicate URLs don't consume storage. Set a hard cap on total URLs if needed |
| T4 | **SSRF via URL validation.** If the server fetches the destination URL to validate it (e.g., check if it's live), attacker submits `http://169.254.169.254/...` to hit cloud metadata | High | Medium | Don't fetch destination URLs server-side. Validation is syntactic only (valid URL format, HTTP(S) scheme). Never make outbound requests to user-supplied URLs |
| T5 | **Redis poisoning.** If Redis is accessible on the internal network without auth, an attacker with network access can overwrite cache entries to redirect users anywhere | Critical | Low | Enable Redis AUTH. Bind to localhost or private subnet. Use TLS for Redis connections. Even if Redis is poisoned, redirect through PostgreSQL on cache miss as a fallback verification |
| T6 | **Analytics data leakage.** Click data (IP addresses, referrers) is PII in many jurisdictions | Medium | Medium | Hash IP addresses before storage (SHA-256 + salt). Don't store raw referrer URLs -- extract domain only. Add a data retention policy (delete clicks older than 90 days) |
| T7 | **Stored XSS via URL.** Malicious URL containing JavaScript is rendered in analytics dashboard or API responses | Medium | Low | URLs are never rendered as HTML. API returns JSON only. If a dashboard is added later, output-encode all URL values. Content-Type headers must be `application/json` |

## IAM & Infrastructure

- **Database credentials:** Stored in environment variables (v1). Move to a secrets manager before production. DB user has access only to the `shortener` schema, not the whole server.
- **Redis:** No sensitive data beyond the URL mappings. If compromised, attacker can redirect users (see T5) but can't access other systems.
- **Deployment role (if cloud):** Needs access to the database and Redis only. No S3, no SQS, no other services. Scope the IAM role to exactly these two resources.

## Error Handling

- 404 on unknown short codes returns `{"error": "not found"}` -- no information about whether the code was ever valid
- Database connection errors return 503, not stack traces
- Rate limit responses return 429 with `Retry-After` header -- don't reveal the exact limit threshold in the response body
- Validation errors return 422 with field-level detail (this is fine -- it's the user's own input)

## Supply Chain

- Pin all Python dependencies with hashes in `requirements.txt` (use `pip-compile --generate-hashes`)
- Run `pip-audit` in CI to check for known vulnerabilities
- FastAPI, SQLAlchemy, and redis-py are mature, widely-used packages -- low supply chain risk
- `gitleaks` in CI to catch accidentally committed secrets
- Container base image: use `python:3.12-slim`, pin the digest, rebuild weekly

---

# Phase 5 -- CI/CD Pipeline

## Pipeline Stages

```yaml
# .github/workflows/ci.yml
name: CI
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    services:
      postgres:
        image: postgres:16
        env:
          POSTGRES_DB: shortener_test
          POSTGRES_PASSWORD: test
        ports: ["5432:5432"]
      redis:
        image: redis:7
        ports: ["6379:6379"]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: pip install -r requirements.txt -r requirements-dev.txt

      # Quality gates
      - run: ruff check .                     # Linting
      - run: ruff format --check .            # Formatting
      - run: pytest --cov=app --cov-fail-under=85 tests/

      # Security gates
      - run: bandit -r app/                   # SAST
      - run: pip-audit                        # SCA / dependency vulnerabilities
      - run: gitleaks detect --source .       # Secret scanning
```

## Gate-to-Threat Mapping

| Gate | Tool | Catches threat | Doesn't catch |
|---|---|---|---|
| SAST | `bandit` | T7 (XSS patterns), hardcoded secrets, insecure function calls | Logic bugs, business logic flaws |
| SCA | `pip-audit` | Known CVEs in dependencies (supply chain) | Zero-days, malicious packages not yet flagged |
| Secret scanning | `gitleaks` | Committed API keys, database passwords, tokens | Secrets in env vars or config management |
| Unit tests | `pytest` | T4 (SSRF -- test that no outbound requests are made), T2 (rate limiting on 404s), input validation | Real network issues, race conditions |
| Integration tests | `pytest` + real Redis/Postgres | T5 (Redis auth -- test that unauthenticated Redis connection fails), actual redirect latency | Production-scale load |
| Linting | `ruff` | Code quality, import hygiene, basic type issues | Security vulnerabilities |

## Custom Security Gates (from threat model)

These go beyond the standard tooling:

```python
# tests/security/test_no_outbound_requests.py
# Maps to T4: SSRF prevention
def test_shorten_does_not_fetch_destination(monkeypatch):
    """Ensure URL creation never makes outbound HTTP requests."""
    import socket
    def deny_all(*args, **kwargs):
        raise RuntimeError("Outbound connection attempted during URL creation")
    monkeypatch.setattr(socket, "create_connection", deny_all)
    response = client.post("/shorten", json={"url": "https://example.com/long"})
    assert response.status_code == 201

# tests/security/test_error_no_leakage.py
# Maps to T2, error handling review
def test_404_reveals_nothing():
    response = client.get("/nonexistent-code")
    body = response.json()
    assert response.status_code == 404
    assert body == {"error": "not found"}
    assert "traceback" not in response.text.lower()
```

## Dummy Product

Minimal FastAPI app that exercises every gate:

- `app/main.py` -- FastAPI app with `/shorten`, `/{code}`, `/stats/{code}`, `/health`
- `app/models.py` -- SQLAlchemy `Url` and `Click` models
- `app/cache.py` -- `RedisClient` wrapper with `get`/`set`
- `app/analytics.py` -- `AnalyticsEmitter` interface + in-memory implementation
- `tests/` -- Unit tests for each component with injected fakes, plus the security tests above

The dummy product is intentionally simple. It returns hardcoded responses where real logic would go, but it proves the pipeline catches real problems: missing tests, vulnerable dependencies, leaked secrets, and SSRF patterns.

## What the Pipeline Proves vs. Doesn't Catch

**Proves:**
- No known vulnerable dependencies ship
- No secrets in the repo
- No obvious SAST findings (insecure hashing, SQL injection patterns)
- Redirect path doesn't make outbound requests (SSRF gate)
- Error responses don't leak internals
- 85%+ code coverage (as a side effect of testing behavior, not a target)

**Doesn't catch:**
- Open redirect abuse (T1) -- requires runtime blocklist checking, not a static gate
- Redis misconfiguration in production (T5) -- integration tests use a test Redis, not the production instance
- Performance under real load (NFR-1) -- need a separate load test stage (add k6 or locust later)
- Data retention compliance (T6) -- policy enforcement, not a CI gate

---

