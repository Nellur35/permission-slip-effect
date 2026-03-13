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

3. **Read the output.** Concern distribution, recurring clusters, deferred item accumulation, bottleneck markers. Each role candidate comes with the diary entries that support it and the knowledge artifact it would need.

4. **Decide.** For each candidate: Does this pattern consume disproportionate time? Would a dedicated context window improve quality? Is the knowledge artifact rich enough to ground the agent? If you remove this concern from the main agent, does it get better at everything else?

5. **Configure.** Create the agent definition on your platform, referencing the knowledge artifacts the role requires. See [`templates/agent-configs.md`](templates/agent-configs.md) for per-platform examples.

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

## When a Single Window Breaks: Domain-Split Sessions

*Experimental — design pattern, not yet validated with diary data.*

You're already working in multiple windows. One for the component you're building, one for tests, maybe one for docs. This section is about making that deliberate — splitting context across windows so each one holds a coherent domain instead of a degraded slice of everything.

### When to Split

You'll know because the AI starts failing in specific ways:

- **Contradictory guidance.** The threat model steering says "minimize attack surface" while the implementation steering says "add this integration." Both are loaded, neither wins.
- **Context amnesia.** You made an architecture decision in one conversation, but the AI in the same window doesn't remember it 20 messages later. The context window is full and older decisions are falling off.
- **Shallow analysis.** The AI produces generic responses where it used to produce specific ones. It's holding too many artifacts to reason deeply about any of them.
- **The Decision Surface Area Test.** Load the threat model, the architecture doc, the current implementation task, and relevant diary entries into a single context window. If the agent loses coherence, misses connections, or contradicts itself — context has exceeded single-agent capacity.

### How to Split

Each window owns a domain and its artifacts. The window loads only the steering files and knowledge artifacts relevant to that domain.

Example split for a security-critical project:

| Window | Domain | Loads | Produces |
|--------|--------|-------|----------|
| 1 | Requirements & scope | requirements.md, security-requirements steering | Updated requirements, non-goals, scope decisions |
| 2 | Architecture & design | architecture.md, threat-model steering | Architecture decisions, trust boundary diagrams |
| 3 | Implementation | Current task, relevant architecture section, coding steering | Code, tests, diary entries |
| 4 | Review | Artifacts from windows 1-3, adversarial-review steering | Findings, SPLITs, amendment requests |

You don't need all four. Two windows — implementation + review — is the minimum useful split.

### Cross-Artifacts: Automated State Sync

The repo's own principle applies here: *you don't solve activation energy with willpower — you remove the decision point.* Expecting a developer to manually ferry decisions between windows under deadline pressure is a guaranteed failure mode. Domains drift silently, and you end up with split-brain implementations.

The fix: upstream windows (architecture, threat model) **write** constraints to a shared state file. Downstream windows (implementation, review) **read** that file on every prompt. The AI manages its own sync. You review the log.

**The state file:** `cross-artifacts.md` (or `.cursor/cross-artifacts.md`, `.claude/cross-artifacts.md` — wherever your platform keeps project state). Append-only with timestamps. Each entry is a binding constraint from one domain.

```markdown
## Active Constraints

- **[Architecture — 2026-03-13]** Auth is OAuth2 with refresh tokens, 24hr expiry. No session cookies.
- **[Threat-Model — 2026-03-13]** The refresh token endpoint is high-risk. Rate limit and monitor.
- **[Architecture — 2026-03-14]** ~~SUPERSEDED~~ Auth is OAuth2 with opaque tokens, server-side session. (Replaces: refresh token constraint above.)
```

When a decision changes, the old constraint is marked superseded and the new one references it. Downstream windows see the current state without having to resolve conflicts.

**Upstream steering (writers):** Add to architecture or threat model steering files:

```
When you finalize a structural decision that other domains need to follow,
write it to cross-artifacts.md using the format: [Domain — date] constraint.
If this supersedes an earlier constraint, mark the old one ~~SUPERSEDED~~
and reference it. Keep constraints concise and binding.
```

**Downstream steering (readers):** Add to implementation or review steering files:

```
Before writing code or producing findings, read cross-artifacts.md.
Active constraints in this file are absolute and override conversational context.
If a constraint mandates OAuth2 and you write session cookies, you have failed.
Skip any entry marked ~~SUPERSEDED~~.
```

**What this gives you:**

- **Zero activation energy.** The AI writes and reads constraints automatically. No human ferrying.
- **No split-brain.** The implementation window can't accidentally build the wrong architecture because the constraint file anchors it.
- **Auditable history.** If something goes wrong, `cross-artifacts.md` shows exactly which constraints were active and when they changed.

**Known failure modes with steering-based sync:**

Adversarial review of this pattern identified three failure modes that natural-language steering alone doesn't prevent:

- **The Helpful Housekeeper.** The AI decides `cross-artifacts.md` is messy and rewrites the entire file instead of appending. Specific constraints from other domains vanish silently. The AI is optimizing for clean formatting, not state integrity.
- **The Context Avalanche.** After a month of development, the file holds 50 active constraints and 200 superseded ones. The downstream window reads all 250 on every prompt, polluting its context window with dead information. The very mechanism designed to prevent context collapse causes it.
- **The Sycophantic Bypass.** The developer says "just for testing, ignore the OAuth2 constraint." The implementation AI complies — sycophancy beats steering. The constraint file says "absolute" but the human override wins.

**The hardened version:** A deterministic CLI tool (similar to `pipeline.py`) that handles all file I/O. The AI passes structured input — `add`, `supersede`, `archive` — and the script handles formatting, timestamping, and separating active constraints from archived ones. The downstream window reads only active constraints, not the full history. This prevents file corruption (the AI never touches the file directly), prevents context avalanche (archived entries are hidden from readers), and creates a clean audit trail.

The sycophantic bypass requires a different fix: a pre-commit gate check that compares generated code against active constraints in `cross-artifacts.md`. This catches the drift after the fact, but before it ships.

Neither the CLI tool nor the gate check exist yet. The steering-based version above works for projects where the constraint count stays low (under ~20 active). Build the hardened version when you hit the failure modes.

**Fallback for platforms without file access:** If your platform doesn't support file writes from the AI, the Navigator carries constraints manually. This works but is fragile — the diary partially catches drift (entries that contradict constraints from another window become visible in the log), but the diary is detection, not prevention. Automate if you can.

### The Navigator Role

With automated sync, the Navigator role shifts from ferrying to oversight:

- **Review the constraint log.** Periodically check `cross-artifacts.md` for constraints that are stale, contradictory, or superseded without replacement.
- **Resolve cross-window SPLITs.** When the review window flags a contradiction between domains, you decide which domain yields.
- **When to split further.** If one window starts showing the same symptoms (contradictions, amnesia, shallow analysis), split it.
- **When to merge back.** If two windows are consistently producing compatible output and the project has simplified, collapse them.

### What This Doesn't Solve

This is context management, not capability improvement. If the model produces shallow analysis with full context, splitting the context won't fix it — that's a model capability issue, not a window architecture issue.

The automated sync also introduces a new attack surface: a compromised upstream window can write malicious constraints that downstream windows obey. Mitigations: `cross-artifacts.md` is committed via PR (same review gate as code), the review window's adversarial steering should flag constraints that weaken security posture, and periodic `pipeline.py review cross-artifacts.md` catches poisoned constraints.

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
| Domain-Split | Manage flow between windows, carry cross-artifacts, resolve cross-window SPLITs | Reason deeply within domain scope, produce domain artifacts |
| 3: Persistent Agents | Set boundaries, review PRs, periodic strategic review | Monitor, propose, maintain artifacts autonomously |

The AI does the work. You make the decisions.
