# Skill Telemetry Hooks

Telemetry answers: which skills fire, how often, in what phase, and what happens after. The diary captures what the *navigator* noticed. Telemetry captures what *actually happened*. Diff the two and you find blind spots.

---

## What Gets Logged

Every telemetry entry captures:

| Field | What | Example |
|---|---|---|
| `timestamp` | ISO 8601 | `2026-03-21T14:32:07Z` |
| `session_id` | Session identifier | `session-a1b2c3` |
| `event` | What happened | `skill_read`, `skill_output`, `skill_override` |
| `skill` | Which skill fired | `threat-model`, `review`, `gate-check` |
| `phase` | Methodology phase if known | `4`, `cross-phase`, `unknown` |
| `tool` | Which tool was used | `Read`, `Write`, `Bash` |
| `target` | File or artifact involved | `tools/threat-model.md`, `threat_model.md` |
| `notes` | Optional context | `user redirected to different approach` |

### Event Types

- **`skill_read`** — Claude read a skill file. This is activation — the model decided this skill was relevant.
- **`skill_output`** — The skill produced its artifact (wrote threat_model.md, generated review findings, etc.).
- **`skill_skip`** — A skill was read but no artifact was produced. The model changed direction.
- **`skill_override`** — The navigator rejected or significantly modified the skill's output.
- **`skill_rerun`** — The same skill was invoked again in the same session. Signal of either iteration or thrashing.

---

## Log Format

JSONL (one JSON object per line) in `telemetry.jsonl` at project root, alongside `diary.md`.

```jsonl
{"timestamp":"2026-03-21T14:32:07Z","session_id":"s-a1b2","event":"skill_read","skill":"threat-model","phase":"4","tool":"Read","target":"integrations/claude-code/.claude/skills/threat-model/SKILL.md","notes":""}
{"timestamp":"2026-03-21T14:38:22Z","session_id":"s-a1b2","event":"skill_output","skill":"threat-model","phase":"4","tool":"Write","target":"threat_model.md","notes":""}
{"timestamp":"2026-03-21T15:10:45Z","session_id":"s-a1b2","event":"skill_read","skill":"review","phase":"4","tool":"Read","target":"integrations/claude-code/.claude/skills/review/SKILL.md","notes":""}
{"timestamp":"2026-03-21T15:22:03Z","session_id":"s-a1b2","event":"skill_override","skill":"review","phase":"4","tool":"Write","target":"review-findings.md","notes":"navigator: scope too broad, re-run on auth component only"}
```

---

## Claude Code — Hook Configuration

Add to `.claude/settings.json` (or your hooks config):

```json
{
  "hooks": {
    "preToolUse": [
      {
        "matcher": "Read",
        "command": "bash .claude/skills/telemetry/log-skill.sh pre_read \"$TOOL_INPUT\""
      }
    ],
    "postToolExecution": [
      {
        "matcher": "Read",
        "command": "bash .claude/skills/telemetry/log-skill.sh post_read \"$TOOL_INPUT\" \"$TOOL_OUTPUT\""
      },
      {
        "matcher": "Write|Edit",
        "command": "bash .claude/skills/telemetry/log-skill.sh post_write \"$TOOL_INPUT\""
      }
    ]
  }
}
```

The hook fires on every Read and Write. The script filters — only skill-related reads and methodology-artifact writes get logged. Everything else is ignored.

---

## Kiro — Agent Hook

Create `.kiro/hooks/skill-telemetry.md`:

```markdown
---
name: skill-telemetry
trigger: on_file_save
description: Log skill activations and artifact outputs to telemetry.jsonl
---

After reading any skill file or producing any methodology artifact (requirements.md, architecture.md, threat_model.md, review-findings.md, etc.), append a telemetry entry to telemetry.jsonl. Use the JSONL format from the telemetry specification.
```

Kiro's hook is less precise than Claude Code's — it fires on file save, not on tool use. Acceptable. The retro compensates for noise.

---

## Git — Pre-Commit Telemetry Summary (Optional)

Append to the existing diary pre-commit hook:

```bash
# Add to .git/hooks/pre-commit after the diary check

# Telemetry summary for this commit
if [ -f telemetry.jsonl ]; then
    SKILL_COUNT=$(wc -l < telemetry.jsonl)
    UNIQUE_SKILLS=$(jq -r '.skill' telemetry.jsonl 2>/dev/null | sort -u | wc -l)
    OVERRIDES=$(grep -c '"skill_override"' telemetry.jsonl || true)
    RERUNS=$(grep -c '"skill_rerun"' telemetry.jsonl || true)

    if [ "$SKILL_COUNT" -gt 0 ]; then
        echo ""
        echo "📊 Skill telemetry: $SKILL_COUNT events, $UNIQUE_SKILLS unique skills, $OVERRIDES overrides, $RERUNS reruns"
    fi
fi
```

---

## What Telemetry Does NOT Capture

- **Quality of output.** Telemetry says the skill fired. It doesn't say the output was good. That's the retro's job.
- **Navigator cognitive load.** Telemetry can't tell you the navigator was overwhelmed. Diary friction tags (`[BOTTLENECK]`) capture that.
- **Why a skill didn't fire.** Absence is invisible. If a skill should have triggered but didn't, only the retro catches it.
- **Cross-session trends.** Single-session telemetry is noise. Value emerges over 5+ sessions. The retro aggregates.

---

## Privacy and Storage

- Telemetry stays local. `telemetry.jsonl` lives in the project, committed to git alongside `diary.md`.
- No external transmission. No analytics service. The navigator owns the data.
- `.gitignore` it if you don't want telemetry in version control — but the retro is less useful without historical data.
- Rotation: archive entries older than 30 days to `telemetry-archive/YYYY-MM.jsonl` to keep the active file small.
