# Multi-Agent Evolution

> **Core principle:** Multi-agent is not a project configuration. It's an emergence that the project's own history tells you is needed. Roles are earned through evidence, not assigned through ambition.

---

## The Project Diary

Every session, the AI automatically writes a structured diary entry for each meaningful change. The navigator doesn't write it, doesn't manage it, doesn't think about it. Steering files instruct the AI to maintain the diary. Platform hooks ensure entries are written even if the AI misses the instruction.

The diary records what changed, why, which concern drove it, what was reviewed, and what was deferred. Over weeks, this accumulates into the project's operational memory — a structured log that pattern analysis can mine for where specialized agents would reduce navigator load.

**The navigator's only interaction with the diary is optional:** glance at recent entries when curious, correct anything obviously wrong. The diary works on noisy data. Perfection is not required.

See `templates/diary-entry.md` for the entry format. See `steering/` for platform-specific auto-collection configs. See `hooks/` for enforcement mechanisms.

---

## Why Not Start Multi-Agent?

Every platform now supports parallel agents. The temptation is to spin up a Security Agent, a Testing Agent, and an Architecture Agent on day one.

An agent without context is a generic prompt wearing a costume. A "Security Agent" without a populated threat model, without vulnerability history, without architecture decisions to reason about — it produces the same generic advice you'd get from asking any model "review this for security." You pay multi-agent coordination costs for single-agent quality.

Multi-agent becomes valuable when:
1. A single agent can't hold all relevant context for any one concern
2. Patterns in the work reveal where specialized attention creates value
3. The navigator spends more time on coordination than on decisions

The methodology handles this through three tiers that you progress through naturally.

---

## Tier 0: Single Agent (Default)

One navigator, one AI. All 8 phases work as documented. The AI produces, the navigator decides. Phase artifacts accumulate. The diary auto-collects in the background.

**This is where the knowledge layer gets built.** No special configuration needed beyond adding the diary steering instruction and hook to your project (see `steering/` for one-line additions to your existing configs).

**You are building the foundation that makes everything else possible.** Skip this and multi-agent is theater.

---

## Tier 1: Pipeline Mode (Ad Hoc — Any Time)

The reasoning pipeline (`pipeline/pipeline.py`) implements multi-model reasoning. Multiple models analyze artifacts through defined frameworks.

```bash
# Adversarial review of any artifact
pipeline.py review architecture.md

# Full reasoning pipeline on a problem
pipeline.py reason "Should we migrate to event-driven architecture?"

# NEW: Analyze the diary for agent emergence patterns
pipeline.py emerge diary.md
```

**When to use:** Any time. No threshold required.

**The `emerge` command:** Takes the project diary as input. Applies Graph of Thoughts to map relationships between entries. Outputs:
- Concern frequency distribution (which concerns dominate the work?)
- Recurring pattern clusters (what keeps coming back?)
- Navigator time concentration (where is human attention spent vs. change complexity?)
- Deferred item accumulation (what's being punted and where does it pile up?)
- **Agent role candidates** with evidence (which patterns justify dedicated agents, and why?)

The output is a recommendation backed by diary data. The navigator decides whether to act.

---

## Tier 2: Session Subagents (Earned Through Evidence)

Specialized subagents within a working session. The navigator delegates scoped tasks to agents with access to specific knowledge artifacts.

### How Roles Emerge

1. **Accumulate.** Work in Tier 0. The diary auto-collects. Minimum ~15-30 entries before patterns become meaningful (calendar time varies — could be 2 weeks of intense work or 2 months of part-time).

2. **Analyze.** Run `pipeline.py emerge diary.md`. The pipeline reads every entry, builds a graph of concern relationships, identifies clusters, and surfaces candidates.

3. **The analysis might show:**
   - "Security concern appears in 28% of entries, often cross-referencing threat model with implementation. A dedicated agent preloading this context would eliminate repeated context-building."
   - "Dependency conflicts have recurred 5 times with low confidence ratings. A dedicated agent with package manifest access could handle these before they reach the navigator."
   - "Architecture review is requested in 40% of sessions but only 10% result in changes. This is a review bottleneck — an agent that pre-screens could save navigator time."

4. **Decide.** The navigator evaluates each candidate:
   - Does this pattern consume disproportionate navigator time?
   - Would a dedicated context window improve quality?
   - Is the knowledge artifact for this concern rich enough to ground the agent?
   - If I remove this concern from the main agent's load, does the main agent become more effective?

5. **Configure.** Create the agent definition on your platform, referencing the specific knowledge artifacts the role requires (see Platform Reference below).

### Readiness Signals

These aren't hard gates — they're signals the diary analysis is likely to find something actionable:

- Diary has 15+ entries with visible concern distribution
- At least one concern category appears in 25%+ of entries
- 3+ entries share patterns the AI flagged with `[RECURRING]` or `[PATTERN]`
- Deferred items are accumulating in a specific concern area
- Navigator reports spending more time loading context than making decisions
- A retro identified a recurring issue that could be caught earlier by a dedicated agent

### Role-to-Artifact Principle

Every agent role must have a corresponding knowledge artifact. No artifact, no role.

| What the diary reveals | Implied role | Required artifact |
|---|---|---|
| Security concerns in 25%+ of entries | Security Reviewer | Threat model with mitigations |
| Architecture decisions frequently revisited | Architecture Challenger | Architecture decision log (ADRs) |
| Tech debt accumulating faster than resolved | Debt Tracker | Tech debt registry with priorities |
| Test gaps discovered repeatedly | Test Strategist | Test coverage map + failure history |
| Dependency conflicts recurring | Dependency Auditor | Package manifest + conflict log |
| Performance regressions caught late | Performance Monitor | Baseline metrics + benchmark history |

The left column comes from your data. The right columns follow. **Roles you didn't predict will emerge. Roles you expected might never appear.** Trust the diary.

---

## Tier 3: Persistent Agent Roles (Rare)

Autonomous agents operating continuously across sessions — monitoring and acting on the knowledge layer without navigator initiation.

### When Tier 3 Is Justified

All of the following:

1. At least one Tier 2 subagent has been used 5+ times with confirmed value
2. Project spans 3+ repositories or major subsystems
3. CI/CD pipeline is established with automated quality gates
4. Knowledge artifacts maintained across 10+ sessions without degradation
5. The navigator can articulate what each agent **decides**, not just what it **reviews**

### The Decision Surface Area Test

A project is complex enough for Tier 3 when a single agent cannot hold enough context to make good decisions about any one concern.

**Concrete test:** Load the threat model, the architecture doc, the current implementation task, and relevant diary entries into a single context window. If the agent loses coherence, misses connections, or contradicts itself — context has exceeded single-agent capacity. That's your signal.

### Security Implications

Persistent agents introduce attack surface. The diary mechanism adds specific vectors that the threat model must address.

**Diary as persistent injection surface.** Unlike prompt injection that affects one session, a poisoned diary entry persists in the filesystem and is re-read across sessions. A malicious entry could influence agent behavior for weeks. Mitigations:
- Diary entries are committed with the code they describe — same PR review gate applies
- At Tier 3, autonomous agent diary entries should be flagged for periodic navigator spot-checks
- The `emerge` analysis should be run by a different model than the one that wrote the diary entries, preventing self-reinforcing patterns

**Privilege escalation through graduated tiers.** An agent operating at Tier 2 could theoretically write diary entries that strengthen the case for Tier 3 autonomy. Mitigation: the diary is a factual change log, not a self-assessment. Every entry ("added test," "fixed dependency conflict," "deferred migration") is verifiable from the git diff. The concern tag is the only subjective field — and even that is usually obvious from what files were touched. There is no confidence rating or quality self-assessment for the agent to inflate.

**Knowledge artifact poisoning.** If threat models and architecture docs serve as grounding documents for agents, corruption of these artifacts cascades through all subsequent agent reasoning. The diary amplifies this because entries reference these artifacts, creating dependency chains. Mitigations:
- Artifacts go through the same PR review as code
- The methodology's adversarial review (Phase 4) applies to knowledge artifacts, not just code
- Periodic `pipeline.py review` of knowledge artifacts catches drift

**Steering file supply chain.** CLAUDE.md, .cursorrules, AGENTS.md load automatically and can be modified through PRs. These are high-value, low-detection attack surfaces. Mitigation: steering files should be treated as security-critical configuration — reviewed with the same rigor as IAM policies or CI pipeline definitions.

---

## The Diary as the Coordination Mechanism

Traditional multi-agent systems synchronize through message passing, shared memory, or orchestration protocols. In this methodology, agents synchronize through the knowledge layer.

When Agent A updates the threat model, a diary entry is auto-written. When Agent B starts a session, it reads recent diary entries to understand what changed. **The diary IS the message bus. The knowledge artifacts ARE the shared memory. The navigator IS the orchestrator.**

No separate synchronization protocol needed. The methodology's existing artifact structure provides everything multi-agent coordination requires. Multi-agent isn't a new architecture on top of the methodology — it's what happens when the knowledge layer gets rich enough that a single agent can't hold it all.

---

## Platform Capabilities (March 2026)

| Capability | Claude Code | Kiro | Codex | Cursor | Windsurf |
|---|---|---|---|---|---|
| Custom subagents | `.claude/agents/*.md` | `.kiro/agents/*.md` | Agents SDK | Composer config | `AGENTS.md` |
| Parallel execution | ~10 concurrent | Built-in + custom | Multi-thread | Up to 8 | Git worktrees |
| Background/async | Ctrl+B | Autonomous agent | Cloud tasks | Cloud agents | Cascade flow |
| Context isolation | Per-subagent window | Per-subagent window | Per-thread | Per-agent | Per-session |
| Steering files | CLAUDE.md | steering/*.md | AGENTS.md | .cursorrules | AGENTS.md + Rules |
| Hooks/triggers | Custom hooks | Agent hooks | Automations | Limited | Limited |
| Multi-repo support | Agent Teams | Autonomous agent | Multi-project | Single repo | Single repo |

---

## Navigator Role at Each Tier

| Tier | Navigator | AI |
|---|---|---|
| 0: Single Agent | Make all decisions, review output | Produce artifacts, auto-write diary |
| 1: Pipeline | Decide when to analyze, evaluate emergence candidates | Run analysis, surface patterns from diary |
| 2: Session Subagents | Choose which roles to activate, define scope, review output | Execute within scope, update artifacts, auto-write diary |
| 3: Persistent Agents | Set boundaries, review PRs, periodic strategic review | Monitor, propose, maintain artifacts autonomously |

**At every tier: the AI does the work, you make the decisions.**
