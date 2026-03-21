#!/bin/bash
# log-skill.sh — Skill telemetry logger for Claude Code hooks
#
# Called by PreToolUse and PostToolExecution hooks.
# Filters for skill-related events only. Ignores everything else.
#
# Usage:
#   bash log-skill.sh pre_read "$TOOL_INPUT"
#   bash log-skill.sh post_read "$TOOL_INPUT" "$TOOL_OUTPUT"
#   bash log-skill.sh post_write "$TOOL_INPUT"

set -euo pipefail

TELEMETRY_FILE="${PROJECT_ROOT:-$(git rev-parse --show-toplevel 2>/dev/null || echo '.')}/telemetry.jsonl"
SESSION_ID="${CLAUDE_SESSION_ID:-session-$(date +%s | tail -c 5)}"
TIMESTAMP=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

EVENT_TYPE="$1"
TOOL_INPUT="${2:-}"
TOOL_OUTPUT="${3:-}"

# --- Skill detection patterns ---

# Skill file paths — adjust if your layout differs
SKILL_PATTERNS=(
    ".claude/skills/"
    ".kiro/steering/"
    ".kiro/hooks/"
    "tools/review.md"
    "tools/threat-model.md"
    "tools/audit.md"
    "tools/gate-check.md"
    "tools/intake.md"
    "tools/session-retro.md"
    "methodology/METHODOLOGY.md"
    "methodology/CLAUDE-skill.md"
    "FULL-CONTEXT.md"
    "reasoning-pipeline.md"
    "pipeline/"
    "multi-agent/"
)

# Methodology artifact patterns — outputs that skills produce
ARTIFACT_PATTERNS=(
    "requirements.md"
    "architecture.md"
    "threat_model.md"
    "review-findings.md"
    "diary.md"
    "tasks.md"
    "phase-"
)

# --- Helper functions ---

is_skill_path() {
    local path="$1"
    for pattern in "${SKILL_PATTERNS[@]}"; do
        if [[ "$path" == *"$pattern"* ]]; then
            return 0
        fi
    done
    return 1
}

is_artifact_path() {
    local path="$1"
    for pattern in "${ARTIFACT_PATTERNS[@]}"; do
        if [[ "$path" == *"$pattern"* ]]; then
            return 0
        fi
    done
    return 1
}

extract_skill_name() {
    local path="$1"
    # Try to extract skill name from path
    # .claude/skills/threat-model/SKILL.md -> threat-model
    if [[ "$path" == *".claude/skills/"* ]]; then
        echo "$path" | sed 's|.*\.claude/skills/||' | cut -d'/' -f1
    # .kiro/steering/review.md -> review
    elif [[ "$path" == *".kiro/steering/"* ]]; then
        basename "$path" .md
    # tools/threat-model.md -> threat-model
    elif [[ "$path" == *"tools/"* ]]; then
        basename "$path" .md
    # methodology/METHODOLOGY.md -> methodology
    elif [[ "$path" == *"methodology/"* ]]; then
        echo "methodology"
    elif [[ "$path" == *"FULL-CONTEXT.md"* ]]; then
        echo "full-context"
    elif [[ "$path" == *"reasoning-pipeline"* ]]; then
        echo "reasoning-pipeline"
    elif [[ "$path" == *"pipeline/"* ]]; then
        echo "pipeline-cli"
    elif [[ "$path" == *"multi-agent/"* ]]; then
        echo "multi-agent"
    else
        echo "unknown"
    fi
}

extract_phase() {
    # Try to infer phase from context
    # This is best-effort — the retro can correct it
    local path="$1"
    if [[ "$path" == *"intake"* || "$path" == *"phase-1"* ]]; then
        echo "1"
    elif [[ "$path" == *"requirements"* || "$path" == *"phase-2"* ]]; then
        echo "2"
    elif [[ "$path" == *"architecture"* || "$path" == *"phase-3"* ]]; then
        echo "3"
    elif [[ "$path" == *"threat-model"* || "$path" == *"threat_model"* || "$path" == *"phase-4"* ]]; then
        echo "4"
    elif [[ "$path" == *"cicd"* || "$path" == *"phase-5"* ]]; then
        echo "5"
    elif [[ "$path" == *"task"* || "$path" == *"phase-6"* ]]; then
        echo "6"
    elif [[ "$path" == *"phase-7"* ]]; then
        echo "7"
    elif [[ "$path" == *"phase-8"* || "$path" == *"session-retro"* ]]; then
        echo "8"
    elif [[ "$path" == *"review"* || "$path" == *"gate-check"* || "$path" == *"audit"* ]]; then
        echo "cross-phase"
    else
        echo "unknown"
    fi
}

log_event() {
    local event="$1"
    local skill="$2"
    local phase="$3"
    local tool="$4"
    local target="$5"
    local notes="${6:-}"

    # Escape quotes in notes
    notes=$(echo "$notes" | sed 's/"/\\"/g')

    echo "{\"timestamp\":\"$TIMESTAMP\",\"session_id\":\"$SESSION_ID\",\"event\":\"$event\",\"skill\":\"$skill\",\"phase\":\"$phase\",\"tool\":\"$tool\",\"target\":\"$target\",\"notes\":\"$notes\"}" >> "$TELEMETRY_FILE"
}

# --- Rerun detection ---

check_rerun() {
    local skill="$1"
    if [ -f "$TELEMETRY_FILE" ]; then
        local prior_reads
        prior_reads=$(grep "\"skill\":\"$skill\"" "$TELEMETRY_FILE" | grep -c "\"event\":\"skill_read\"" || true)
        if [ "$prior_reads" -gt 0 ]; then
            return 0  # This is a rerun
        fi
    fi
    return 1
}

# --- Main logic ---

case "$EVENT_TYPE" in
    pre_read)
        # Extract file path from tool input
        FILE_PATH=$(echo "$TOOL_INPUT" | grep -oP '"path"\s*:\s*"\K[^"]+' 2>/dev/null || echo "$TOOL_INPUT")

        if is_skill_path "$FILE_PATH"; then
            SKILL=$(extract_skill_name "$FILE_PATH")
            PHASE=$(extract_phase "$FILE_PATH")

            if check_rerun "$SKILL"; then
                log_event "skill_rerun" "$SKILL" "$PHASE" "Read" "$FILE_PATH" "repeated activation"
            else
                log_event "skill_read" "$SKILL" "$PHASE" "Read" "$FILE_PATH" ""
            fi
        fi
        ;;

    post_read)
        # Post-read — currently no action needed beyond pre_read logging
        # Future: could detect if the read failed or returned empty
        ;;

    post_write)
        FILE_PATH=$(echo "$TOOL_INPUT" | grep -oP '"path"\s*:\s*"\K[^"]+' 2>/dev/null || echo "$TOOL_INPUT")

        if is_artifact_path "$FILE_PATH"; then
            # Determine which skill likely produced this artifact
            SKILL=$(extract_skill_name "$FILE_PATH")
            PHASE=$(extract_phase "$FILE_PATH")
            log_event "skill_output" "$SKILL" "$PHASE" "Write" "$FILE_PATH" ""
        fi
        ;;

    *)
        # Unknown event type — ignore silently
        ;;
esac

exit 0
