# Cursor Integration

## Installation

### Option 1: Tell Cursor to do it

In Cursor's agent mode (⌘.), paste:

```
Read the three .mdc rule files from https://github.com/Nellur35/permission-slip-effect/tree/main/integrations/cursor/.cursor/rules/ and save them to this project's .cursor/rules/ directory. Create the directory if it doesn't exist.
```

### Option 2: Clone and copy

```bash
git clone https://github.com/Nellur35/permission-slip-effect.git /tmp/pse
mkdir -p .cursor/rules
cp /tmp/pse/integrations/cursor/.cursor/rules/*.mdc .cursor/rules/
rm -rf /tmp/pse
```

Rules activate automatically when you open matching files — no restart needed.

## What's included

Three rules activated by file type:

| Rule | Triggers on | What it does |
|------|------------|-------------|
| `security-first-coding.mdc` | Source files (.py, .js, .ts, .go, etc.) | Applies security principles — input validation, least privilege, never-do list |
| `threat-model-infra.mdc` | Dockerfiles, Terraform, pipeline configs, IAM policies | Triggers threat model checks — trust boundaries, blast radius, secrets |
| `security-first-testing.mdc` | Test files | Enforces behavior-driven testing — test requirements not coverage, PBT for security logic |

Rules use `alwaysApply: false` with glob triggers, so they only fire when relevant files are open. The `.mdc` format is compatible with Cursor 2.2+.

## Full methodology

For the complete 8-phase workflow (not just the rules), point Cursor at:

```
Read https://raw.githubusercontent.com/Nellur35/permission-slip-effect/main/FULL-CONTEXT.md and use it as your development methodology for this project.
```
