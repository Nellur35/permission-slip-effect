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
