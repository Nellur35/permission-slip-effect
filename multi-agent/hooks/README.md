# Diary Enforcement Hooks

> **Purpose:** Safety net. The steering file is the primary collection mechanism. These hooks catch gaps — sessions where the AI made changes but didn't write a diary entry.

---

## Kiro — Agent Hook (on file save)

Create `.kiro/hooks/diary-check.md`:

```markdown
---
name: diary-check
trigger: on_file_save
description: Ensure diary entry exists for recent changes
---

Check if diary.md has been updated in this session. If changes were made to code, docs, or config files but no diary entry was written since the last one, write the missing entry now. Follow the diary entry format from the steering file.
```

This hook fires on every file save. If the AI already wrote the diary entry (as the steering file instructs), the hook sees the update and does nothing. If the AI forgot, the hook catches it.

---

## Kiro — Autonomous Agent Hook

For Tier 3 (persistent agents), add to the autonomous agent's task description:

```
After completing any task, append a diary entry to diary.md following the project's diary format. Include what you changed, why, which concern drove it, and what (if anything) was deferred.
```

The autonomous agent writes diary entries as part of its task completion, keeping the log current even when the navigator isn't actively reviewing.

---

## Claude Code — Custom Hook

Claude Code supports custom hooks for tool execution events. Add to your hooks config:

```json
{
  "hooks": {
    "postToolExecution": [
      {
        "matcher": "write|edit|bash",
        "command": "echo 'Reminder: update diary.md if this was a meaningful change'"
      }
    ]
  }
}
```

This is a soft reminder rather than enforcement. Claude Code's steering via CLAUDE.md is the primary mechanism. The hook serves as a nudge if the AI gets deep into implementation and forgets to log.

For stronger enforcement, use a session-end hook:

```json
{
  "hooks": {
    "preCompact": [
      {
        "command": "echo 'Before compacting: verify diary.md has entries for all changes this session'"
      }
    ]
  }
}
```

---

## Git — Pre-Commit Hook (All Platforms)

A git pre-commit hook that warns if code changed but diary.md didn't:

```bash
#!/bin/bash
# .git/hooks/pre-commit
# Warns if code/config changed but diary.md has no new entries

# Check if non-diary files were modified
CODE_CHANGES=$(git diff --cached --name-only | grep -v diary.md | grep -E '\.(ts|js|py|go|rs|md|yaml|json|toml)$' | wc -l)

# Check if diary.md was modified
DIARY_UPDATED=$(git diff --cached --name-only | grep -c diary.md)

if [ "$CODE_CHANGES" -gt 0 ] && [ "$DIARY_UPDATED" -eq 0 ]; then
    echo ""
    echo "⚠️  Code changed but diary.md was not updated."
    echo "   Consider adding a diary entry for this change."
    echo "   (This is a warning, not a block. Commit proceeds.)"
    echo ""
fi

# Always allow the commit — this is advisory, not blocking
exit 0
```

Install:
```bash
cp hooks/pre-commit .git/hooks/pre-commit
chmod +x .git/hooks/pre-commit
```

This works with any platform because it operates at the git level. It's advisory — warns but doesn't block. The navigator can ignore it for trivial changes.

---

## CI — Diary Freshness Check (Optional)

For teams or projects that want stronger enforcement, add a CI step:

```yaml
# .github/workflows/diary-check.yml
name: Diary Freshness
on: pull_request

jobs:
  check-diary:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Check diary coverage
        run: |
          # Count files changed in this PR (excluding diary.md)
          CHANGED=$(git diff --name-only origin/main...HEAD | grep -v diary.md | grep -E '\.(ts|js|py|go|rs)$' | wc -l)
          
          # Count new diary entries in this PR
          ENTRIES=$(git diff origin/main...HEAD -- diary.md | grep -c '^+###' || true)
          
          if [ "$CHANGED" -gt 3 ] && [ "$ENTRIES" -eq 0 ]; then
            echo "::warning::PR has $CHANGED code files changed but no diary entries. Consider documenting what changed and why."
          else
            echo "✅ Diary coverage looks good ($ENTRIES entries for $CHANGED files)"
          fi
```

This runs as a PR check. It warns but doesn't fail the build. The ratio of changes to entries is intentionally loose — not every file change needs an entry, but a PR with 10+ code files and zero diary entries probably missed something.

---

## Summary: Defense in Depth

| Layer | Mechanism | Enforcement Level |
|---|---|---|
| Platform hook | Fires on save/compact/commit, writes entry deterministically | **Primary** — doesn't compete with coding instructions |
| Steering file | AI instruction to write entries after each change | Secondary — works ~90% of the time but drifts in long sessions |
| Git pre-commit | Warns if code changed but diary didn't | Advisory — navigator sees the gap |
| CI check | PR-level coverage check | Team governance — optional |

**Use hooks when your platform supports them** (Kiro, Claude Code). Fall back to steering-only on platforms without hook support (Cursor, Windsurf). Add CI checks if you're running a team.
