# Multi-Agent Evolution

Multi-agent is not a project configuration. It emerges when the project's own history shows it's needed. Roles are earned through evidence, not assigned upfront.

---

## The Project Diary

Every session, the AI logs a structured entry for each meaningful change: what changed, why, which concern drove it, what was deferred. You don't write it, don't manage it, don't think about it. Steering files and hooks handle collection.

Over weeks this accumulates into the project's operational memory — a structured log that pattern analysis can mine for where specialized agents would reduce your load. Glance at recent entries when curious. Correct anything obviously wrong. The analysis works on noisy data. Perfection is not required.

Entry format: [`templates/diary-entry.md`](templates/diary-entry.md). Platform configs: [`steering/`](steering/). Hooks: [`hooks/`](hooks/).

---

## Why Not Start Multi-Agent?

An agent without context is a generic prompt wearing a costume. A "Security Agent" without a populated threat model, without vulnerability history, without architecture decisions to reason about — it produces the same output you'd get from asking any model "review this for security." You pay coordination costs for single-agent quality.

Multi-agent becomes worth it when:
1. A single agent can't hold all relevant context for any one concern
2. Patterns in the work reveal where specialized attention creates value
3. You spend more time loading context than making decisions

---

## Tier 0: Single Agent (Default)

One navigator, one AI. All 8 phases work as documented. The AI produces, you decide. Phase artifacts accumulate. The diary auto-collects in the background.

This is where the knowledge layer gets built. Add the diary steering instruction and hook to your project (see `steering/` for one-line additions to your existing configs). That's it.

Skip this and multi-agent is theater.

---

## Tier 1: Pipeline Mode (Any Time)

The reasoning pipeline already does multi-model reasoning. Multiple models analyze artifacts through defined frameworks.

```bash
pipeline.py review architecture.md                                  # adversarial review
pipeline.py reason "Should we migrate to event-driven architecture?" # full reasoning pipeline
pipeline.py emerge diary.md                                          # analyze diary for agent emergence
```

Use any time. No threshold required.

The `emerge` command takes the diary as input, applies Graph of Thoughts to map relationships between entries, and outputs: concern frequency distribution, recurring pattern clusters, deferred item accumulation, and agent role candidates with evidence. You decide whether to act.

---

## Tier 2: Session Subagents (Earned Through Evidence)

Specialized subagents within a working session. You delegate scoped tasks to agents that have access to specific knowledge artifacts.

### How Roles Emerge

1. **Accumulate.** Work in Tier 0. The diary auto-collects. Minimum ~15-30 entries before patterns become meaningful — could be 2 weeks of intense work or 2 months part-time.

2. **Analyze.** Run `pipeline.py emerge diary.md`. The pipeline reads every entry, builds a graph of concern relationships, identifies clusters, surfaces candidates.

3. **Read the output.** It might show: security concerns in 28% of entries, always cross-referencing threat model with implementation. Or dependency conflicts recurring 5 times. Or architecture reviews requested in 40% of sessions but only 10% resulting in changes.

4. **Decide.** For each candidate: Does this pattern consume disproportionate time? Would a dedicated context window improve quality? Is the knowledge artifact rich enough to ground the agent? If you remove this concern from the main agent, does it get better at everything else?

5. **Configure.** Create the agent definition on your platform, referencing the knowledge artifacts the role requires.

### Readiness Signals

Signals, not gates:

- 15+ diary entries with visible concern distribution
- One concern category in 25%+ of entries
- 3+ entries with `[RECURRING]` or `[PATTERN]` markers
- Deferred items accumulating in a specific concern area
- You spend more time loading context than making decisions
- A retro identified a recurring issue a dedicated agent could catch earlier

### No Artifact, No Role

Every agent role needs a corresponding knowledge artifact. The diary reveals the role; the artifact grounds it.

| What the diary reveals | Implied role | Required artifact |
|---|---|---|
| Security concerns in 25%+ of entries | Security Reviewer | Threat model with mitigations |
| Architecture decisions frequently revisited | Architecture Challenger | Architecture decision log (ADRs) |
| Tech debt accumulating faster than resolved | Debt Tracker | Tech debt registry with priorities |
| Test gaps discovered repeatedly | Test Strategist | Test coverage map + failure history |
| Dependency conflicts recurring | Dependency Auditor | Package manifest + conflict log |
| Performance regressions caught late | Performance Monitor | Baseline metrics + benchmark history |

The left column comes from your data. The right columns follow. Roles you didn't predict will emerge. Roles you expected might never appear. Trust the diary.

---

## Tier 3: Persistent Agent Roles (Rare)

Autonomous agents operating across sessions — monitoring and acting on the knowledge layer without you initiating it.

### When Tier 3 Is Justified

All of these:

1. At least one Tier 2 subagent used 5+ times with confirmed value
2. Project spans 3+ repositories or major subsystems
3. CI/CD pipeline established with automated quality gates
4. Knowledge artifacts maintained across 10+ sessions without degradation
5. You can articulate what each agent **decides**, not just what it **reviews**

### The Decision Surface Area Test

Load the threat model, the architecture doc, the current implementation task, and relevant diary entries into a single context window. If the agent loses coherence, misses connections, or contradicts itself — context has exceeded single-agent capacity. That's your signal.

### Security Implications

Persistent agents introduce attack surface. The diary mechanism adds specific vectors your threat model must address.

**Diary as persistent injection surface.** A poisoned diary entry persists in the filesystem and is re-read across sessions — a durable backdoor, not a one-shot injection. Mitigations: diary entries are committed with the code they describe (same PR review gate), autonomous agent diary entries get periodic spot-checks, the `emerge` analysis runs on a different model than the one that wrote the entries.

**Privilege escalation through graduated tiers.** An agent at Tier 2 could write diary entries that strengthen the case for Tier 3. Mitigation: the diary is a factual change log, not a self-assessment. "Added test," "fixed dependency conflict," "deferred migration" — all verifiable from the git diff. No confidence rating or quality self-assessment to inflate.

**Knowledge artifact poisoning.** Corrupted threat models or architecture docs cascade through all subsequent agent reasoning. The diary amplifies this because entries reference artifacts, creating dependency chains. Mitigations: artifacts go through PR review, adversarial review (Phase 4) applies to knowledge artifacts, periodic `pipeline.py review` catches drift.

**Steering file supply chain.** CLAUDE.md, .cursorrules, AGENTS.md load automatically and can be modified through PRs. Treat steering files as security-critical configuration — review with the same rigor as IAM policies or CI pipeline definitions.

---

## How Agents Coordinate

Agents synchronize through the knowledge layer. When one agent updates the threat model, a diary entry is written. When another agent starts a session, it reads recent diary entries. The diary is the message bus. The knowledge artifacts are the shared memory. You are the orchestrator.

No separate synchronization protocol. No message queue. No consensus algorithm. The artifact structure already provides everything multi-agent coordination requires.

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

| Tier | You | The AI |
|---|---|---|
| 0: Single Agent | Make all decisions, review output | Produce artifacts, auto-write diary |
| 1: Pipeline | Decide when to analyze, evaluate candidates | Run analysis, surface patterns |
| 2: Session Subagents | Choose roles, define scope, review output | Execute within scope, update artifacts, write diary |
| 3: Persistent Agents | Set boundaries, review PRs, periodic strategic review | Monitor, propose, maintain artifacts autonomously |

The AI does the work. You make the decisions.
