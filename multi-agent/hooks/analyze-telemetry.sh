#!/bin/bash
# analyze-telemetry.sh — Generate telemetry summary for session retro
#
# Usage:
#   bash analyze-telemetry.sh                    # current session
#   bash analyze-telemetry.sh --session s-a1b2   # specific session
#   bash analyze-telemetry.sh --all              # cross-session aggregate
#
# Output: structured summary to stdout for the retro skill to consume

set -euo pipefail

TELEMETRY_FILE="${PROJECT_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || echo '.')}/telemetry.jsonl"

if [ ! -f "$TELEMETRY_FILE" ]; then
    echo "No telemetry data found at $TELEMETRY_FILE"
    exit 0
fi

MODE="${1:---current}"
SESSION_FILTER="${2:-}"

# --- Filter to relevant entries ---

case "$MODE" in
    --session)
        if [ -z "$SESSION_FILTER" ]; then
            echo "Error: --session requires a session ID"
            exit 1
        fi
        DATA=$(grep "\"session_id\":\"$SESSION_FILTER\"" "$TELEMETRY_FILE" || true)
        SCOPE="Session $SESSION_FILTER"
        ;;
    --all)
        DATA=$(cat "$TELEMETRY_FILE")
        SCOPE="All sessions"
        ;;
    --current|*)
        # Get the most recent session ID
        LATEST_SESSION=$(tail -1 "$TELEMETRY_FILE" | grep -oP '"session_id":"\K[^"]+' 2>/dev/null || echo "")
        if [ -z "$LATEST_SESSION" ]; then
            echo "No telemetry entries found."
            exit 0
        fi
        DATA=$(grep "\"session_id\":\"$LATEST_SESSION\"" "$TELEMETRY_FILE" || true)
        SCOPE="Current session ($LATEST_SESSION)"
        ;;
esac

if [ -z "$DATA" ]; then
    echo "No telemetry entries found for scope: $SCOPE"
    exit 0
fi

# --- Compute metrics ---

TOTAL_EVENTS=$(echo "$DATA" | wc -l)
SKILL_READS=$(echo "$DATA" | grep -c '"skill_read"' || true)
SKILL_OUTPUTS=$(echo "$DATA" | grep -c '"skill_output"' || true)
SKILL_SKIPS=$(echo "$DATA" | grep -c '"skill_skip"' || true)
SKILL_OVERRIDES=$(echo "$DATA" | grep -c '"skill_override"' || true)
SKILL_RERUNS=$(echo "$DATA" | grep -c '"skill_rerun"' || true)

# Unique skills activated
UNIQUE_SKILLS=$(echo "$DATA" | grep -oP '"skill":"\K[^"]+' | sort -u)
UNIQUE_COUNT=$(echo "$UNIQUE_SKILLS" | grep -c . || true)

# Completion rate: outputs / (reads + reruns)
ACTIVATIONS=$((SKILL_READS + SKILL_RERUNS))
if [ "$ACTIVATIONS" -gt 0 ]; then
    COMPLETION_RATE=$(( (SKILL_OUTPUTS * 100) / ACTIVATIONS ))
else
    COMPLETION_RATE="N/A"
fi

# Skills activated but never produced output
SKILLS_WITH_OUTPUT=$(echo "$DATA" | grep '"skill_output"' | grep -oP '"skill":"\K[^"]+' | sort -u || true)
SKILLS_WITHOUT_OUTPUT=""
while IFS= read -r skill; do
    if [ -n "$skill" ] && ! echo "$SKILLS_WITH_OUTPUT" | grep -q "^${skill}$"; then
        SKILLS_WITHOUT_OUTPUT="${SKILLS_WITHOUT_OUTPUT}${skill}, "
    fi
done <<< "$UNIQUE_SKILLS"
SKILLS_WITHOUT_OUTPUT=${SKILLS_WITHOUT_OUTPUT%, }

# Phase distribution
PHASE_DIST=$(echo "$DATA" | grep -oP '"phase":"\K[^"]+' | sort | uniq -c | sort -rn)

# --- Output ---

cat <<EOF
## Telemetry Summary — $SCOPE

### Activation Metrics

| Metric | Count |
|---|---|
| Total events | $TOTAL_EVENTS |
| Skills activated (reads) | $SKILL_READS |
| Skills produced output | $SKILL_OUTPUTS |
| Skills skipped (read, no output) | $SKILL_SKIPS |
| Navigator overrides | $SKILL_OVERRIDES |
| Reruns (same skill, same session) | $SKILL_RERUNS |
| Unique skills used | $UNIQUE_COUNT |
| Completion rate | ${COMPLETION_RATE}% |

### Skills Activated
$(echo "$UNIQUE_SKILLS" | while read -r s; do [ -n "$s" ] && echo "- $s"; done)

### Skills Read but No Output
$(if [ -n "$SKILLS_WITHOUT_OUTPUT" ]; then echo "$SKILLS_WITHOUT_OUTPUT"; else echo "None — all activated skills produced output"; fi)

### Phase Distribution
$(echo "$PHASE_DIST" | while read -r count phase; do echo "- Phase $phase: $count events"; done)

### Signals

$(if [ "$SKILL_RERUNS" -gt 2 ]; then echo "⚠️  **High rerun count ($SKILL_RERUNS).** Possible thrashing — skill may not be producing what the navigator needs on first pass."; fi)
$(if [ "$SKILL_OVERRIDES" -gt 0 ]; then echo "⚠️  **$SKILL_OVERRIDES override(s).** Navigator rejected skill output. Check if skill instructions need updating."; fi)
$(if [ -n "$SKILLS_WITHOUT_OUTPUT" ]; then echo "⚠️  **Activated but unused:** $SKILLS_WITHOUT_OUTPUT. Model read the skill but didn't produce the expected artifact. Possible: wrong skill triggered, or navigator changed direction."; fi)
$(if [ "$ACTIVATIONS" -gt 0 ] && [ "$COMPLETION_RATE" != "N/A" ] && [ "$COMPLETION_RATE" -lt 50 ]; then echo "⚠️  **Low completion rate (${COMPLETION_RATE}%).** Most skill activations didn't produce output. Skills may be overtriggering."; fi)
EOF

# --- Cross-session trends (only in --all mode) ---

if [ "$MODE" = "--all" ]; then
    SESSION_COUNT=$(echo "$DATA" | grep -oP '"session_id":"\K[^"]+' | sort -u | wc -l)

    # Most used skills across all sessions
    TOP_SKILLS=$(echo "$DATA" | grep '"skill_read"' | grep -oP '"skill":"\K[^"]+' | sort | uniq -c | sort -rn | head -5)

    # Override rate per skill
    OVERRIDE_SKILLS=$(echo "$DATA" | grep '"skill_override"' | grep -oP '"skill":"\K[^"]+' | sort | uniq -c | sort -rn)

    cat <<EOF

### Cross-Session Trends ($SESSION_COUNT sessions)

**Most activated skills:**
$(echo "$TOP_SKILLS" | while read -r count skill; do echo "- $skill: $count activations"; done)

**Skills with overrides:**
$(if [ -n "$OVERRIDE_SKILLS" ]; then echo "$OVERRIDE_SKILLS" | while read -r count skill; do echo "- $skill: $count overrides"; done; else echo "None"; fi)
EOF
fi
