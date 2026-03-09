# Cursor Integration

Two versions: **Light** (automatic guardrails) and **Full** (complete security methodology).

---

## Light Version — Install and forget

Three rules that activate automatically when you open matching files. No workflow changes, no manual steps. Security awareness in the background.

### Install

In Cursor's agent mode (⌘.), paste:

```
Read the three automatic .mdc rule files (security-first-coding, threat-model-infra, security-first-testing) from https://github.com/Nellur35/permission-slip-effect/tree/main/integrations/cursor/.cursor/rules/ and save them to this project's .cursor/rules/ directory. Create the directory if it doesn't exist.
```

Or clone and copy:

```bash
git clone https://github.com/Nellur35/permission-slip-effect.git /tmp/pse
mkdir -p .cursor/rules
cp /tmp/pse/integrations/cursor/.cursor/rules/security-first-coding.mdc .cursor/rules/
cp /tmp/pse/integrations/cursor/.cursor/rules/threat-model-infra.mdc .cursor/rules/
cp /tmp/pse/integrations/cursor/.cursor/rules/security-first-testing.mdc .cursor/rules/
rm -rf /tmp/pse
```

### What you get

| Rule | Triggers on | What it does |
|------|------------|-------------|
| `security-first-coding.mdc` | Source files (.py, .js, .ts, .go, etc.) | Security principles — enforces secrets/destructive-action rules, flags other issues as TODOs during prototyping |
| `threat-model-infra.mdc` | Dockerfiles, Terraform, GitHub Actions, docker-compose, CloudFormation | Threat model checklist — trust boundaries, IAM blast radius, secrets, container security |
| `security-first-testing.mdc` | Test files (*.test.*, *.spec.*, __tests__/, test_*.py) | Behavior-driven testing — test requirements not coverage, PBT for security logic |

**Won't interfere with normal work.** Rules only activate on matching files. During prototyping, security concerns are flagged as TODO comments instead of blocking your flow.

---

## Full Version — Complete security methodology

Everything in Light, plus six manually-invocable rules you call with `@rulename` when you need them. These add structured phases — threat modeling, adversarial review, gate checks — that the automatic rules can't do.

### Install

In Cursor's agent mode (⌘.), paste:

```
Read all .mdc rule files from https://github.com/Nellur35/permission-slip-effect/tree/main/integrations/cursor/.cursor/rules/ and save them to this project's .cursor/rules/ directory. Create the directory if it doesn't exist.
```

Or clone and copy:

```bash
git clone https://github.com/Nellur35/permission-slip-effect.git /tmp/pse
mkdir -p .cursor/rules
cp /tmp/pse/integrations/cursor/.cursor/rules/*.mdc .cursor/rules/
rm -rf /tmp/pse
```

### What you get (in addition to the Light rules)

| Rule | Invoke with | What it does |
|------|------------|-------------|
| `security-methodology.mdc` | `@security-methodology` | Overview — explains the full workflow and when to use each rule |
| `threat-model.mdc` | `@threat-model` | Generates a structured threat model from architecture docs — 13 security areas |
| `adversarial-review.mdc` | `@adversarial-review` | Attacks any artifact adversarially — finds what the author missed |
| `gate-check.mdc` | `@gate-check` | Verifies exit criteria before moving to the next phase |
| `security-audit.mdc` | `@security-audit` | Audits an existing codebase — coverage map, gaps, recommended entry point |
| `security-requirements.mdc` | `@security-requirements` | Adds testable security requirements, non-goals, trust boundaries, data classification |
| `reasoning-pipeline.mdc` | `@reasoning-pipeline` | Runs a multi-framework reasoning pipeline on complex decisions |

### Recommended flow for a new project

```
@security-requirements → @threat-model → @adversarial-review → @gate-check → build
```

### Recommended flow for an existing project

```
@security-audit → (follow its recommended entry point)
```

---

## Full methodology as context

For the complete 8-phase workflow as a single document (not rules, just context), point Cursor at:

```
Read https://raw.githubusercontent.com/Nellur35/permission-slip-effect/main/FULL-CONTEXT.md and use it as your development methodology for this project.
```

This is useful when you want Cursor to internalize the full methodology rather than invoke rules one at a time.

---

## Compatibility

Rules use the `.mdc` format with YAML frontmatter. Compatible with Cursor 2.2+. Automatic rules use `alwaysApply: false` with glob triggers. Manual rules use `alwaysApply: false` with no globs — they only activate when you invoke them with `@rulename`.
