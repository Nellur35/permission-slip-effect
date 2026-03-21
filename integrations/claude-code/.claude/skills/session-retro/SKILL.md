---
name: session-retro
description: >
  Structured feedback loop for any work session. Runs RCA, retrospective,
  and produces executable lessons learned. Activates when the session is
  ending, a task is complete, or the user asks to run a retro, feedback
  loop, or lessons learned.
allowed-tools:
  - Read
  - Glob
  - Grep
  - Bash
  - Write
---

# Session Feedback Loop

**Trigger:** When the session is ending, a task is marked complete, or the navigator says they're done for now — offer to run the feedback loop before closing.

You are performing a structured feedback loop on the session. Not a postmortem — this runs on everything, not just failures.

**Quick filter first:** Did this session involve a decision, a surprise, or a recognized pattern? If yes → full loop. If routine execution → one-line summary: "What happened. Surprising: [yes/no]. Lesson: [one line or none]." Append to `diary.md`.

**Full loop:**

**Stage 1 — RCA:** For each significant event this session, trace: what happened → what caused it (5 Whys) → what structural condition enabled it (if this is a restatement of the event, go deeper) → where the decision point was → whether this is recurring (check `diary.md`). No judgment. Just causation. Events include bug fixes, features shipped, refactors completed, investigations done, tech debt addressed, or anything else that happened.

**Stage 2 — Retrospective:** Read the RCA. Start with what worked well — same causal depth as problems. What structural condition enabled it, and how do you protect it? Then: identify repeating patterns (within this session and historically). Note where expected ≠ actual. State what you understand now that you didn't before. Flag friction points.

**Stage 2.5 — Telemetry Review (if telemetry is installed):** Before generating lessons, run `bash .claude/skills/telemetry/analyze-telemetry.sh` (or `--all` for cross-session trends). Read the output. Answer: (1) Which skill activations does the navigator not mention in the session description? These are blind spots. (2) Which skills activated but produced no output — overtriggering or navigator pivot? (3) Which skills should have fired but didn't — undertriggering? (4) If the navigator overrode a skill's output, was it scope mismatch, quality issue, context issue, or legitimate pivot? (5) If a skill was invoked multiple times, was it iteration (healthy) or thrashing (skill needs rewrite)? (6) Completion rate below 70% means skills are doing more reading than producing. Feed all findings into Stage 3 as telemetry-sourced lessons with format: `Source: telemetry — [metric]`, `Type: skill-tuning`, `Target: [which SKILL.md or hook config]`. When telemetry is available, append to the diary entry: skills activated, completion rate, overrides, telemetry signals.

**Stage 3 — Lessons Learned:** For each retro finding, produce an executable action. Format:

```
Lesson: [name]
Source: [which RCA event or retro finding]
Type: rule | process | tool | knowledge | none
Scope: tactical | strategic
Action: [specific change — not "be more careful"]
Target: [which file gets updated]
Priority: do now | next session | backlog
```

**Scope:** Tactical = apply in under 2 minutes (rule addition, constraint append, config change). Strategic = informs future planning (architecture decision, process restructuring) — log with a scheduled session.

**Conflict check:** Before applying any lesson, check: does it contradict an existing rule, gate, or constraint? If yes — do not apply, do not waive. Escalate to a Graph of Thoughts analysis against `diary.md`. Map the dependency structure of both the existing rule and the conflicting lesson — when each was created, what evidence supports each, where the causal chains converge. The resolution comes from the shared root. Tag the conflict as ESCALATED in the output.

**Critical:** "Do now" applies to tactical lessons only — and only when no conflict is detected. Apply immediately — update CLAUDE.md, the relevant skill file, or project documentation before the session closes. A lesson not applied is a lesson lost.

**Diary:** Append a diary entry to `diary.md` after each run (the same diary used for agent emergence): date, one-line description, key finding, lessons applied, strategic items scheduled, any escalated conflicts.

**What not to do:**
- Do not skip this because the session went well. Good outcomes have causal structure too.
- Do not produce vague lessons like "improve testing." Produce "add edge case X to test suite Y."
- Do not maintain a separate lessons-learned file. Update the system directly. Write to the existing `diary.md`, not a new file.

## Gotchas

**Produces vague lessons.** "Improve test coverage" is not a lesson. "Add edge case test for empty input to `validate_token()` in `tests/test_auth.py`" is a lesson. If the Action field doesn't name a specific file or rule, it's a strategic finding, not a tactical lesson. The skill says this — the model ignores it under time pressure.

**Skips "what worked well" analysis.** The model treats the retro as a postmortem — it finds problems. Stage 2 explicitly asks what worked and why, with the same causal depth as problems. Good outcomes have structural conditions worth protecting. If the retro output has no "What Worked" section, or the section is one sentence, it's incomplete.

**Conflict detection is theoretical.** Stage 3 says to check if a lesson contradicts an existing rule and escalate. In practice, the model almost never detects conflicts because it would need to read every existing rule and gate to compare. When this matters most (a lesson that would weaken a security gate), the model is least likely to catch it. Running `/gate-check` after applying retro lessons is the safety net.

**Quick summary path is too quick.** The quick filter says routine sessions get one paragraph. The model uses this escape hatch aggressively — sessions with genuine surprises get quick-summarized because the model classifies them as routine. Bias toward the full loop. If in doubt, run it.

**Doesn't check if tactical lessons were applied.** The skill says "do now lessons get applied before the session ends." But it doesn't verify. If the retro says "add rule X to CLAUDE.md" and the session ends without that edit, the lesson is lost. The telemetry system (Stage 2.5) closes this gap — but only if telemetry is installed.
