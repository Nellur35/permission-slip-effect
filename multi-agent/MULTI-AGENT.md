# Multi-Agent Evolution

Multi-agent is not a project configuration. It emerges when the project's own history shows it's needed. Roles are earned through evidence, not assigned upfront. An agent without context is a generic prompt wearing a costume.

Entry format: [`templates/diary-entry.md`](templates/diary-entry.md) · Platform configs: [`steering/`](steering/) · Hooks: [`hooks/`](hooks/)

---

## Tier 0: Single Agent (Default)

One navigator, one AI. All 8 phases work as documented. The diary auto-collects in the background.

**Do:** Add the diary steering instruction and hook to your project. That's it.

**Skip this and multi-agent is theater.**

---

## Tier 1: Pipeline Mode (Any Time)

Multi-model reasoning via the CLI. No threshold required.

```bash
pipeline.py review architecture.md          # adversarial review
pipeline.py reason "Should we migrate?"     # full reasoning pipeline
pipeline.py emerge diary.md                 # analyze diary for agent emergence
```

---

## Tier 2: Session Subagents (Earned Through Evidence)

Specialized subagents within a working session. Diary is the message bus. Knowledge artifacts are shared memory. You are the orchestrator.

**Readiness signals** (signals, not gates):

- 15+ diary entries with visible concern distribution
- One concern category in 25%+ of entries
- 3+ entries with `[RECURRING]` or `[PATTERN]` markers
- You spend more time loading context than making decisions

**How:** Run `pipeline.py emerge diary.md` → read concern distribution → decide which roles earn a dedicated context window. Every role needs a corresponding knowledge artifact — no artifact, no role.

| Diary pattern | Implied role | Required artifact |
|---|---|---|
| Security concerns in 25%+ of entries | Security Reviewer | Threat model |
| Architecture decisions revisited | Architecture Challenger | ADR log |
| Tech debt accumulating | Debt Tracker | Debt registry |
| Test gaps recurring | Test Strategist | Coverage map + failure history |

---

## When a Single Window Breaks: Domain-Split Sessions

*Experimental — design pattern, not yet validated with diary data.*

You're already working in multiple windows. This makes it deliberate — each window holds a coherent domain instead of a degraded slice of everything.

### Triggers

- **Contradictory guidance.** Steering files from different domains conflict.
- **Context amnesia.** Decisions fall off the context window mid-conversation.
- **Shallow analysis.** Generic responses where specific ones used to appear.
- **Decision Surface Area Test.** Load threat model + architecture + current task + diary into one window. If the agent loses coherence — split.

### How to Split

The split follows the same principle as Tier 2 role emergence — the project's own complexity determines the domains, not a predetermined template. Look at where the diary clusters, where context conflicts appear, and where the AI's quality degrades.

Different projects split differently:

| Project type | Likely domains |
|---|---|
| Security-critical backend | Threat model · Implementation · Review |
| Full-stack app | Frontend · Backend · Testing · Knowledge |
| Data pipeline | Ingestion · Transformation · Serving |
| Infrastructure | IaC · Security policy · Monitoring |
| Solo CRUD app | Implementation · Review (minimum useful split) |

Each window loads only the steering files and artifacts for its domain. The diary reveals which domains need separation — the same way it reveals which roles need agents in Tier 2. Don't predefine the split. Let the friction tell you.

### Cross-Artifact Sync

*You don't solve activation energy with willpower — you remove the decision point.*

Upstream windows **write** binding constraints to `cross-artifacts.md`. Downstream windows **read** it on every prompt. The AI manages sync. You review the log.

**Upstream steering addition:**
```
When you finalize a structural decision that other domains need,
write it to cross-artifacts.md: [Domain — date] constraint.
If superseding an earlier constraint, mark the old one ~~SUPERSEDED~~.
```

**Downstream steering addition:**
```
Before writing code, read cross-artifacts.md.
Active constraints override conversational context. Skip ~~SUPERSEDED~~ entries.
```

**Known failure modes:**

- **Helpful Housekeeper.** AI rewrites the entire file instead of appending — constraints from other domains vanish. Fix: deterministic CLI tool for file I/O (not yet built).
- **Context Avalanche.** Superseded entries accumulate, polluting downstream context. Fix: CLI tool that archives old entries and serves only active constraints to readers.
- **Sycophantic Bypass.** Developer says "ignore OAuth2 constraint for this prototype." AI complies. Fix: pre-commit gate check comparing code against active constraints.
- **Tautology Trap.** Same model writes constraints and writes the code that must follow them. It designs compliant code by knowing the constraints, not by independently verifying correctness. Fix: review window uses a different model or doesn't load the upstream reasoning — only the constraints.

The steering-based version works for projects with <20 active constraints. Build the hardened CLI version when you hit failure modes.

**Fallback:** If your platform doesn't support AI file writes, the Navigator carries constraints manually. Fragile — diary catches drift after the fact, not before.

### Navigator Role

With automated sync, the Navigator manages oversight, not ferrying:

- Review `cross-artifacts.md` for stale or contradictory constraints
- Resolve cross-window SPLITs
- Split further when symptoms recur; merge back when domains stabilize

---

## Tier 3: Persistent Agent Roles (Rare)

Autonomous agents across sessions — monitoring and acting without you initiating.

**All of these required:**

1. At least one Tier 2 subagent used 5+ times with confirmed value
2. Project spans 3+ repos or major subsystems
3. CI/CD pipeline with automated quality gates
4. Knowledge artifacts maintained across 10+ sessions
5. You can articulate what each agent **decides**, not just **reviews**

### Security Implications

- **Diary as injection surface.** Poisoned entries persist across sessions. Mitigations: diary entries committed via PR, spot-checks, `emerge` runs on a different model than the one that wrote entries.
- **Privilege escalation.** Tier 2 agent writes diary entries strengthening the case for Tier 3. Mitigation: diary is a factual change log — no self-assessment, all entries verifiable from git diff.
- **Artifact poisoning.** Corrupted threat models cascade through all agent reasoning. Mitigations: PR review, adversarial review on artifacts, periodic `pipeline.py review`.
- **Steering file supply chain.** Steering files load automatically, modifiable via PR. Treat them as security-critical configuration.

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
| 2: Session Subagents | Choose roles, define scope, review output | Execute within scope, update artifacts |
| Domain-Split | Review constraint log, resolve cross-window SPLITs | Reason within domain, sync via cross-artifacts |
| 3: Persistent Agents | Set boundaries, review PRs, periodic strategic review | Monitor, propose, maintain artifacts autonomously |

The AI does the work. You make the decisions.
