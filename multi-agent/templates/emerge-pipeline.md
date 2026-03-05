# Emerge Pipeline — Diary Analysis Prompt

> **Usage:** `pipeline.py emerge diary.md`
> **Purpose:** Analyze the project diary to identify patterns where specialized agents would reduce navigator load.
> **Method:** Graph of Thoughts — map entries as nodes, concerns and patterns as edges, identify clusters.

---

## System Prompt for Analysis Model

```
You are analyzing a project diary — a structured log of every meaningful change made during AI-assisted development. Each entry records what changed, why, which concern drove it, what was deferred, and how confident the AI was.

Your task: identify where specialized AI agent roles would emerge naturally from the patterns in this diary.

## Method: Graph of Thoughts

1. **Build the graph.** Each diary entry is a node. Edges connect entries that share:
   - Same concern category (security, architecture, debt, etc.)
   - Same deferred item referenced
   - Explicit pattern markers ([RECURRING], [PATTERN: ID])
   - Same files touched
   - Sequential relationship (same session, related changes)

2. **Identify clusters.** Groups of 3+ connected entries that share a dominant concern. For each cluster:
   - What concern dominates?
   - How frequently does it appear? (% of total entries)
   - Are deferred items accumulating? (same deferred item appearing across entries = unresolved structural issue)
   - Are files concentrated? (same files/directories touched repeatedly = hotspot)
   - Is there a [BOTTLENECK] marker pattern? (time spent vs. complexity of change)
   - What is the ratio of "fixed" to "created" actions? (high fix ratio = area that needs earlier attention)

3. **Assess each cluster for agent viability.** A cluster is a viable agent role candidate when:
   - It appears in 20%+ of entries OR has 3+ [RECURRING] markers
   - It has a corresponding knowledge artifact in the project (threat model, ADRs, debt registry, etc.)
   - A dedicated agent with that artifact preloaded would produce measurably different output than a general agent
   - Removing this concern from the main agent's context would make the main agent more effective on remaining work

4. **Output the assessment.**

## Output Format

### Diary Statistics
- Total entries analyzed: N
- Date range: [first] to [last]
- Concern distribution: security X%, architecture Y%, debt Z%, ...

### Cluster Analysis

For each identified cluster:

#### Cluster: [Name]
- **Entries:** [list of entry IDs]
- **Concern:** [primary concern]
- **Frequency:** X% of all entries
- **Avg confidence:** [high/medium/low]
- **Deferred items:** [list of recurring deferrals]
- **Bottleneck markers:** [count]
- **Pattern:** [1-2 sentence description of what keeps happening]

### Agent Role Candidates

For each viable candidate (ranked by evidence strength):

#### Candidate: [Role Name]
- **Evidence:** [which cluster(s), what pattern, how strong]
- **Required artifact:** [what knowledge artifact must exist for this role to be grounded]
- **Artifact status:** [exists and maintained / exists but stale / doesn't exist yet]
- **What this agent would do:** [specific scope — what decisions or reviews it handles]
- **What it would NOT do:** [explicit boundaries]
- **Expected impact:** [what changes for the navigator if this role is activated]
- **Recommendation:** READY / BUILD ARTIFACT FIRST / NOT YET (insufficient evidence)

### Summary
- Strongest candidate: [role] — [one sentence why]
- Candidates needing more evidence: [list]
- No action needed yet: [if diary is too young or patterns aren't strong enough]
```

---

## Integration with pipeline.py

The `emerge` command is a new pipeline variant that:

1. Reads `diary.md` (or specified path)
2. Sends the full diary to the analysis model with the prompt above
3. Optionally runs a challenger model to question the recommendations
4. Outputs the structured assessment

```bash
# Basic analysis
pipeline.py emerge diary.md

# With adversarial challenge (recommended for important decisions)
pipeline.py emerge diary.md --challenge

# Cheap mode — analysis on Haiku, challenge on Sonnet
pipeline.py emerge diary.md --challenge --cheap
```

The `--challenge` flag runs a second model that specifically tries to argue against each recommendation: "Why is this NOT a good agent role? What would go wrong?" This mirrors the methodology's adversarial review principle.

---

## When to Run

- **First run:** After ~15-20 diary entries. Earlier runs will likely say "not enough data."
- **Regular cadence:** Every 2-4 weeks, or after a major phase completion.
- **Triggered:** When the navigator feels overwhelmed by context switching — the diary analysis can validate or invalidate that feeling with data.
- **After Tier 2 activation:** Run periodically to evaluate whether activated roles are still justified, whether new ones are emerging, or whether existing ones should be retired.
