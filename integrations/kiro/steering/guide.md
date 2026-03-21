---
name: guide
description: Explains the Permission Slip Effect repo — what's available, which tool to use, where to start. Activates when the user asks what this is, how to use the methodology, what tools exist, or any discovery question about the project.
activation: manual
---

# Permission Slip Effect — Guide

Answer discovery questions about this project. Route the user, don't lecture.

## What This Is

Three things, same principle: a **reasoning pipeline** (chain frameworks on one problem), **standalone tools** (paste-and-go prompts for review, threat model, audit), and a **security-first methodology** (8-phase dev process with gate checks).

## Routing

| "I want to..." | Go to |
|---|---|
| Review something right now | `tools/review.md` — paste into any AI conversation |
| Threat model an architecture | `tools/threat-model.md` |
| Scan an existing codebase | `tools/audit.md` |
| Check if a phase is done | `tools/gate-check.md` |
| Define a problem properly | `tools/intake.md` |
| Run a session retrospective | `tools/session-retro.md` |
| Analyze a complex decision | `reasoning-pipeline.md` or `pipeline.py reason "..."` |
| Start a new project | `methodology/METHODOLOGY.md` — begin at Phase 1 |
| See a worked example | `methodology/examples/url-shortener/` |
| Set up multi-agent | `multi-agent/MULTI-AGENT.md` — start with Tier 0 first |

## Don't Use For

- Simple tasks where "think step by step" works
- Tasks where being wrong is cheap
- Throwaway scripts (use standalone tools, not the full methodology)

## Key Terms (Only If Asked)

Permission Slip = structured context that surfaces what RLHF suppresses. SPLIT = reviewers disagree on same evidence, human decides. Phase 0 = decomposition before analysis. Bootstrap gap = builder can't review its own output. Emergence = multi-agent roles earned through diary data.
