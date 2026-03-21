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

## Stage 2.5: Telemetry Review (If Available)

*What did the tools actually do vs. what the navigator noticed?*

If `telemetry.jsonl` exists at project root, run the analysis script before generating lessons:

```bash
bash .claude/skills/telemetry/analyze-telemetry.sh          # current session
bash .claude/skills/telemetry/analyze-telemetry.sh --all     # cross-session trends
```

Read the output. Answer:

1. **Navigator blind spots.** Which skill activations does the navigator not mention in the session description? These are invisible actions — the model used a skill, produced (or didn't produce) output, and the navigator didn't notice.
2. **Overtriggering.** Which skills activated but produced no output? Two possibilities: wrong skill triggered (description field needs tuning), or navigator changed direction mid-skill (legitimate, but worth noting).
3. **Undertriggering.** Based on the session description, which skills *should* have fired but didn't? Compare the session events against the skill descriptions.
4. **Override patterns.** If the navigator overrode a skill's output, why? Categories: scope mismatch (fix skill instructions), quality issue (add to gotchas), context issue (skill didn't read the right artifacts), legitimate pivot (not a skill problem).
5. **Rerun patterns.** If a skill was invoked multiple times, was it iteration (refining output — healthy) or thrashing (not getting what was needed — skill needs rewrite)?
6. **Completion rate.** If below 70%, the skill library is doing more reading than producing. Either skills are overtriggering or the methodology is pulling in more context than needed for the task.

Feed all findings into Stage 3 as telemetry-sourced lessons. Format:

```
Lesson: [name]
Source: telemetry — [metric or signal that surfaced it]
Type: skill-tuning
Scope: tactical
Action: [specific change to skill file, description, or hook config]
Target: [which SKILL.md, hook config, or description field]
Priority: do now | next session
```

When telemetry is available, append to the diary entry: skills activated, completion rate, overrides, telemetry signals.

If no `telemetry.jsonl` exists, skip this stage — the retro works without it. Telemetry adds a data layer; the retro is the interpretation layer.

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

---

## Gotchas

**Produces vague lessons.** "Improve test coverage" is not a lesson. "Add edge case test for empty input to `validate_token()` in `tests/test_auth.py`" is a lesson. If the Action field doesn't name a specific file or rule, it's a strategic finding, not a tactical lesson.

**Skips "what worked well" analysis.** The model treats the retro as a postmortem — it finds problems. Stage 2 explicitly asks what worked and why, with the same causal depth as problems. Good outcomes have structural conditions worth protecting.

**Conflict detection is theoretical.** Stage 3 says to check if a lesson contradicts an existing rule and escalate. In practice, the model almost never detects conflicts because it would need to read every existing rule and gate to compare. Running a gate check after applying retro lessons is the safety net.

**Quick summary path is too quick.** The quick filter says routine sessions get one paragraph. The model uses this escape hatch aggressively — sessions with genuine surprises get quick-summarized because the model classifies them as routine. Bias toward the full loop. If in doubt, run it.

**Doesn't check if tactical lessons were applied.** The skill says "do now lessons get applied before the session ends." But it doesn't verify. If the retro says "add rule X" and the session ends without that edit, the lesson is lost.
