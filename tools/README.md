# Tools

Standalone prompts for security-first development. Each tool works in any AI model — Claude Code, Kiro, Cursor, ChatGPT, Gemini, or anything else.

## How to Use

### Option 1: Give the AI the single-file URL (easiest)

Point your AI tool at the full-context file:

```
Read https://raw.githubusercontent.com/Nellur35/permission-slip-effect/main/FULL-CONTEXT.md
and use the threat-model tool on my architecture
```

One file, one fetch. The AI gets the complete methodology, all tools, and templates.

### Option 2: Paste manually (for tools that can't read URLs)

1. Open any AI chat.
2. Paste the contents of the tool file as the prompt.
3. Paste your input (architecture doc, threat model, project structure, etc.) where indicated.
4. Get structured output.

No methodology knowledge required. Each tool is self-contained.

## Available Tools

### `intake.md`
Interactive questionnaire for Phase 1 problem definition. Asks one question at a time, pushes back on vague answers, redirects solution-jumping back to the problem. Supports greenfield projects and existing codebases.

**Input:** Describe your project
**Output:** `problem_statement.md` (greenfield) or `reconstruction_assessment.md` (existing project)

### `audit.md`
Scan an existing codebase and CI/CD pipeline. Maps architecture, test coverage, security controls, and pipeline gates. Outputs a gap analysis with a recommended entry point into the methodology.

**Input:** Project file tree, CI/CD config, existing docs
**Output:** Gap analysis with pipeline coverage, architecture map, priority actions

### `threat-model.md`
Generate a structured threat model from an architecture document. Examines trust boundaries, IAM blast radius, secrets lifecycle, data lifecycle, supply chain (including LLM-generated code), and 10 other areas.

**Input:** `architecture.md` or system description
**Output:** `threat_model.md` with risks, impact ratings, and mitigations

### `review.md`
Adversarial review of any development artifact. Finds what is wrong, not whether it is good. Includes review lenses for architecture, threat models, CI/CD pipelines, requirements, and code.

**Input:** Any artifact (architecture, threat model, pipeline config, code, design doc)
**Output:** Structured findings with severity, impact, and recommended actions

### `gate-check.md`
Exit criteria checklist for all 8 phases. Each gate lists what it proves and what it doesn't catch. Use it to verify you've met the bar before moving forward.

**Input:** The phase number you are checking
**Output:** Pass/fail for each gate question, with gaps identified

## Skills vs Tools

**Skills** (`.claude/skills/`) are Claude Code commands: `/intake`, `/review`, `/gate-check`, `/threat-model`, `/audit`. They auto-detect context, read project files, and generate output directly. Use these if you work in Claude Code.

**Tools** (`tools/`) work in any AI model. Point the AI at this repo and tell it which tool to use, or paste the tool contents manually if your AI can't read URLs. Use these if you work in Kiro, Cursor, ChatGPT, Gemini, or any other tool.

Same capabilities, different delivery. Skills add auto-detection and file I/O. Tools are portable.

## Relationship to the Full Methodology

These tools extract focused capabilities from the [Security-First AI Dev Methodology](../methodology/METHODOLOGY.md). They are the executables; the methodology is the operating manual. Use any tool independently, or use them together as part of the full 8-phase workflow.
