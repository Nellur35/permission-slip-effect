# Google Antigravity Integration

## Installation

### Per-workspace

```bash
cp -r integrations/antigravity/.agents/skills/security-first-methodology \
  .agents/skills/security-first-methodology
```

### Global

```bash
cp -r integrations/antigravity/.agents/skills/security-first-methodology \
  ~/.gemini/antigravity/skills/security-first-methodology
```

## What it does

Adds security constraints to the agent's autonomous plan-execute-validate cycle: threat model step in every plan, security gates before execution, and validation that tests prove security controls work.
