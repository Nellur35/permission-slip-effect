# Cursor Integration

## Setup

Point Cursor at the repo and let it build rules that fit your project:

```
Read https://raw.githubusercontent.com/Nellur35/permission-slip-effect/main/FULL-CONTEXT.md

Based on this methodology, build .cursor/rules/ for my project. Ask me if I want just automatic guardrails (light) or the full security methodology with manual @rules I can invoke.

Here are examples of rules others have built from this methodology:
https://github.com/Nellur35/permission-slip-effect/tree/main/integrations/cursor/.cursor/rules/
```

Cursor will read the methodology, look at the example rules, and generate rules tailored to your project — your language, your stack, your workflow.

## What Cursor typically builds

**Automatic rules** (glob-triggered, activate when you open matching files):
- Security coding principles for your language
- Threat model checks on infrastructure files
- Testing principles on test files

**Manual rules** (invoke with `@rulename` when you need them):
- Threat modeling — generate a threat model from your architecture
- Adversarial review — attack any artifact to find what you missed
- Gate checks — verify exit criteria before moving phases
- Reasoning pipeline — multi-framework analysis for complex decisions
- Security audit — scan an existing codebase for gaps
- Security requirements — add testable security criteria

Every project gets different rules. A Terraform-heavy project gets different infra triggers than a React app. A solo developer gets different workflow rules than a team.

## Example rules

Pre-built examples are in [`.cursor/rules/`](.cursor/rules/). Use them as-is, modify them, or let Cursor use them as reference when generating your own:

| Example | Type | What it does |
|---------|------|-------------|
| `security-first-coding.mdc` | Auto (source files) | Security principles with prototype escape hatch |
| `threat-model-infra.mdc` | Auto (Dockerfiles, Terraform, etc.) | Infrastructure threat model checklist |
| `security-first-testing.mdc` | Auto (test files) | Behavior-driven testing principles |
| `security-methodology.mdc` | Manual (`@security-methodology`) | Overview — when to use each rule |
| `threat-model.mdc` | Manual (`@threat-model`) | Generate structured threat model (13 areas) |
| `adversarial-review.mdc` | Manual (`@adversarial-review`) | Attack any artifact adversarially |
| `gate-check.mdc` | Manual (`@gate-check`) | Phase exit criteria verification |
| `security-audit.mdc` | Manual (`@security-audit`) | Codebase audit with recommended entry point |
| `security-requirements.mdc` | Manual (`@security-requirements`) | Testable security requirements, non-goals, trust boundaries |
| `reasoning-pipeline.mdc` | Manual (`@reasoning-pipeline`) | Multi-framework reasoning for complex decisions |

## Compatibility

`.mdc` format with YAML frontmatter. Compatible with Cursor 2.2+.
