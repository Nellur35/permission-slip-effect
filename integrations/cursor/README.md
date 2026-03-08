# Cursor Integration

## Installation

```bash
cp -r integrations/cursor/.cursor/rules/* .cursor/rules/
```

## What's included

Three rules activated by file type:

| Rule | Triggers on | What it does |
|------|------------|-------------|
| `security-first-coding.mdc` | Source files | Applies security principles |
| `threat-model-infra.mdc` | Dockerfiles, Terraform, pipeline configs | Triggers threat model checks |
| `security-first-testing.mdc` | Test files | Enforces behavior-driven testing |
