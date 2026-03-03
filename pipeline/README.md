# Reasoning Pipeline CLI

Automates the multi-model reasoning pipeline and adversarial review from the methodology. No AWS account needed -- works with any LLM API.

## Quick Start

```bash
# Set your API key
export ANTHROPIC_API_KEY=sk-ant-...

# Adversarial review of an artifact
python pipeline.py review architecture.md

# Full reasoning pipeline
python pipeline.py reason "Should we migrate auth from API keys to OAuth2?"

# Specific pipeline variant
python pipeline.py reason --pipeline stakeholder "How should we handle the reorg?"

# Multi-model (Challenger uses a different provider)
python pipeline.py reason --architect claude --challenger openai "Why do deploys keep failing?"

# Cheap mode -- analysis on Haiku/Flash, convergence on Sonnet
python pipeline.py reason --cheap "Should we refactor the auth module?"

# Skip cost confirmation (CI-friendly)
python pipeline.py review architecture.md --yes -o results.json

# Read problem from a file
python pipeline.py reason < problem.txt
```

## Cost Awareness

Every run shows estimated token count and cost before asking for confirmation:

```
Pipeline: Standard Pipeline -- FPR opener (5 stages)
Architect: claude-sonnet-4-20250514
Estimated: ~22,300 tokens, ~$0.2345
Proceed? [Y/n]
```

Use `--yes` / `-y` to skip confirmation (for CI). Use `--cheap` to cut costs:

| Mode | Sonnet (5 stages) | With --cheap |
|------|-------------------|-------------|
| Standard | ~$0.20-0.30 | ~$0.05-0.08 |
| Light (3 stages) | ~$0.10-0.15 | ~$0.03-0.05 |
| Review (3 stages) | ~$0.10-0.15 | ~$0.03-0.05 |

`--cheap` runs analysis stages on Haiku/Flash/Mini and only brings the full model in for convergence synthesis.

## No Dependencies

The Anthropic provider uses only `urllib` from the standard library. No pip install needed for basic usage.

Other providers (OpenAI, Google, Bedrock) are included as skeletons with commented-out implementations. Uncomment and install their SDK, or ask an LLM to fill them in -- the interface is one method: `complete(system, user, temperature) -> str`.

## Available Pipelines

```
light             Light Pipeline (3 stages)
                  Stages: RCAR -> ToT -> PMR
                  Use when: Moderate decisions where framing is clear

standard          Standard Pipeline -- FPR opener (5 stages)
                  Stages: FPR -> RCAR -> AdR -> ToT -> PMR
                  Use when: Complex decisions with ambiguity

standard-cot      Standard Pipeline -- CoT opener (5 stages)
                  Stages: CoT -> RCAR -> AdR -> ToT -> PMR
                  Use when: Complex decisions where facts need establishing first

stakeholder       Multi-Stakeholder Pipeline (5 stages)
                  Stages: FPR -> SMR -> AdR -> ToT -> PMR
                  Use when: Competing interests, power dynamics, multiple parties

systems           Systems Pipeline (5 stages)
                  Stages: FPR -> RCAR -> GoT -> ToT -> PMR
                  Use when: Feedback loops, interconnected components

review            Adversarial Review (3 stages)
                  Stages: AdR -> ToT -> PMR
                  Use when: Reviewing an existing artifact
```

## Available Frameworks

| Key  | Framework | What It Does |
|------|-----------|-------------|
| FPR  | First Principles | Validates assumptions, checks if the framing is correct |
| CoT  | Chain of Thought | Establishes facts, timeline, sequential logic |
| RCAR | Root Cause (5 Whys) | Finds structural causes, not symptoms |
| GoT  | Graph of Thoughts | Maps interconnections and feedback loops |
| SMR  | Stakeholder Mapping | Maps power and interest for each player |
| AdR  | Adversarial Reasoning | Finds hidden incentives, failure modes, uncomfortable truths |
| ToT  | Tree of Thoughts | Generates and compares strategic options |
| PMR  | Pre-Mortem | Assumes failure, works backward to identify why |

## Output Format

JSON. Every run produces:

```json
{
  "pipeline": "Standard Pipeline -- FPR opener (5 stages)",
  "input_summary": "Should we migrate...",
  "stages": [
    {
      "stage": "FPR",
      "framework": "First Principles",
      "model": "claude",
      "parsed": { "..." : "..." },
      "duration_seconds": 3.2
    }
  ],
  "convergence": {
    "result": {
      "summary": "...",
      "key_findings": ["..."],
      "risks_ranked": [{"risk": "...", "likelihood": "high", "mitigation": "..."}],
      "navigator_decisions_needed": ["..."]
    }
  },
  "total_duration_seconds": 18.7
}
```

## Adding Providers

Implement one method:

```python
class MyProvider:
    name = "my-llm"

    def __init__(self, model="my-model-v1"):
        self.model = model
    
    def complete(self, system: str, user: str, temperature: float = 0.7) -> str:
        # Call your API, return text
        ...
```

Then add it to `PROVIDERS` dict in `pipeline.py`. That's it.

## CI Integration

```bash
# In your pipeline -- review architecture before merge
python pipeline.py review architecture.md --yes -o review-results.json

# Check for high-risk findings
python -c "
import json
r = json.load(open('review-results.json'))
risks = r.get('convergence', {}).get('result', {}).get('risks_ranked', [])
high = [x for x in risks if x.get('likelihood') == 'high' and x.get('impact') == 'high']
if high:
    print(f'BLOCKED: {len(high)} high-likelihood, high-impact risks found')
    for h in high: print(f'  - {h[\"risk\"]}')
    exit(1)
print('PASSED: No critical risks')
"
```
