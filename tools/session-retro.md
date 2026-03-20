# Session Feedback Loop

Run a structured retrospective after any work session. Not just when things break — after every session where work was done. This is not a postmortem. This runs on everything.

**Input:** Describe what happened this session. Bug fix, new feature, tech debt, investigation, refactor, configuration change — anything.
**Output:** Root cause analysis, retrospective, and executable lessons learned that feed back into your process.

---

## Quick Filter

Not every session needs three full stages.

**Full loop** — the session involved a decision with tradeoffs, something surprising, a recognized pattern, or enough complexity that the takeaway is unclear.

**Quick summary** — routine execution, no decisions or surprises. One paragraph: "What happened. Anything surprising: [yes/no]. Lesson: [one line or none]." Append to `diary.md` and move on.

If unsure, run the full loop.

---

## Stage 1: Root Cause Analysis

*What happened, and what caused it to happen that way?*

Not "what went wrong" — what was the chain of events and decisions that produced this outcome. For each significant event:

1. **What happened?** Factual. No judgment.
2. **What caused it?** Trace the causal chain. 5 Whys if not obvious.
3. **What enabled the cause?** Structural condition — process, tooling, knowledge, environment, timing. If this is a restatement of the event, go deeper.
4. **Decision point?** Where was a choice made (or not made) that shaped the outcome?
5. **Recurring?** First time, or seen before? Check `diary.md` for history.

---

## Stage 2: Retrospective

*Given what the RCA surfaced, what is the state of things?*

Read all RCA outputs. Answer with equal rigor for successes and problems:

1. **What worked well and why?** What structural condition enabled it? How do you protect it? Same causal depth as problems.
2. **What patterns are visible?** Root causes or enabling conditions repeating — within this session and across previous sessions?
3. **What was the delta?** Expected vs. actual. Where did reality diverge?
4. **New understanding?** What do you know now that you didn't before?
5. **Friction?** Where did the process slow down, require workarounds, or feel wrong?

---

## Stage 3: Lessons Learned

*What changes, concretely?*

Stages 1 and 2 are descriptive. Stage 3 is prescriptive. For each finding from the retrospective:

**Every lesson must be executable.** Not "be more careful about X." Instead: "add check for X to gate Y." If the action is a general principle, convert it to a specific change with a named target. If you cannot name a target file or rule, it is a strategic finding, not a tactical lesson.

**Conflict detection.** Before applying any lesson: does it contradict an existing rule, gate, or constraint? If yes — **do not apply. Do not waive. Escalate.** A conflict is a signal that either the rule is wrong, the lesson is wrong, or both are symptoms of a deeper structural issue. Run a Graph of Thoughts analysis with `diary.md` as the input corpus. Map the dependency structure of both. The resolution comes from the shared root, not from picking between leaf nodes. Tag the conflict as ESCALATED in the output.

**Scope:**
- **Tactical** — apply in under 2 minutes. Rule addition, constraint append, config change. "Do now" applies to tactical only.
- **Strategic** — informs future planning. Log in `diary.md` and schedule concretely — not "someday" but "which session."

Tactical "do now" lessons get applied before the session ends.

---

## Diary Entry

The methodology already maintains a diary — a structured log auto-collected via steering files and hooks (see [`multi-agent/MULTI-AGENT.md`](../multi-agent/MULTI-AGENT.md)). The feedback loop writes to the same diary. Do not create a separate file.

After completing the loop (full or quick summary), append to `diary.md`. The diary is the corpus that Graph of Thoughts runs against — for both agent emergence and conflict resolution. Feedback loop entries become part of that corpus.

---

## Output Format Reference

### RCA Entry
```
### Event: [factual description]
Causal chain:
1. [immediate cause]
2. [cause of #1]
...until structural root

Enabling condition: [what allowed this]
Decision point: [where the path was chosen]
Recurrence: [first time / seen before in {context}]
```

### Retrospective
```
### What Worked and Why
[causal explanation — structural condition to protect]

### Patterns
[recurring patterns, cross-session trends]

### Delta: Expected vs. Actual
[where reality diverged]

### New Understanding
[what you know now]

### Friction Points
[where the process resisted]
```

### Lessons Learned
```
### Lesson: [short name]
Source: [which RCA event / retro finding]
Type: rule | process | tool | knowledge | none
Scope: tactical | strategic
Action: [specific executable change]
Target: [which file, tool, template, or rule gets updated]
Priority: [do now | next session | backlog]
```

### Conflict (if detected)
```
### Conflict: [lesson name] vs [existing rule]
Rule: [the existing rule, where it lives, when created]
Lesson: [the conflicting lesson from this session]
Status: ESCALATED — requires GoT analysis against diary.md
```

### Diary Entry
```
## [date] — [one-line session description]
Type: feedback-loop
Events: [count]
Key finding: [single most important insight]
Lessons applied: [list of tactical changes made]
Strategic findings: [list with scheduled sessions]
Conflicts: [ESCALATED items, or none]
```

---

## What This Catches and What It Does Not

**Catches:** Recurring patterns, process friction, decision points, structural conditions enabling both good and bad results, knowledge gaps, successes worth protecting.

**Does not catch:** Problems you did not notice during the session. Use adversarial review (`tools/review.md`) for that.
