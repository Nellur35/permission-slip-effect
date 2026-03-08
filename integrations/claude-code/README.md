# Claude Code Integration

## Installation

### As a persistent skill (all projects)

```bash
git clone https://github.com/Nellur35/permission-slip-effect.git \
  ~/.claude/skills/permission-slip-effect
```

### Per-project

```bash
mkdir -p .claude/skills/methodology
cp integrations/claude-code/.claude/skills/*/SKILL.md .claude/skills/*/SKILL.md
```

### As a CLAUDE.md drop-in

Copy `methodology/CLAUDE-skill.md` to your project root alongside your existing `CLAUDE.md`. Claude Code picks it up automatically.

## What's included

| Skill | Purpose |
|-------|---------|
| `methodology/SKILL.md` | Orchestrator — routes to the right skill per phase |
| `intake/SKILL.md` | `/intake` — interactive Phase 1 problem definition |
| `review/SKILL.md` | `/review` — adversarial review at any phase |
| `gate-check/SKILL.md` | `/gate-check` — verify phase exit criteria |
| `threat-model/SKILL.md` | `/threat-model` — Phase 4 threat modeling |
| `audit/SKILL.md` | `/audit` — scan existing codebase and CI/CD |
