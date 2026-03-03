#!/usr/bin/env python3
"""
Security-First AI Dev Methodology — Reasoning Pipeline CLI

Orchestrates multi-model reasoning pipelines and adversarial reviews.
Ships as a skeleton with an Anthropic provider included. LLMs (or you)
can add providers for OpenAI, Google, Bedrock, Ollama, etc. by
implementing the Provider protocol.

Usage:
    # Adversarial review of an artifact
    python pipeline.py review architecture.md

    # Full reasoning pipeline
    python pipeline.py reason --pipeline standard "Should we migrate auth to OAuth2?"

    # Light pipeline with specific models
    python pipeline.py reason --pipeline light --architect claude --challenger gemini "Why do deploys keep failing?"

    # List available pipelines
    python pipeline.py pipelines

Environment variables:
    ANTHROPIC_API_KEY   — for Claude models
    OPENAI_API_KEY      — for GPT models (requires openai provider)
    GOOGLE_API_KEY      — for Gemini models (requires google provider)
    PIPELINE_ARCHITECT  — default architect model (default: claude)
    PIPELINE_CHALLENGER — default challenger model (default: claude)
"""

import argparse
import json
import os
import sys
import time
from dataclasses import dataclass, field, asdict
from pathlib import Path
from typing import Protocol, Optional


# ============================================================
# Provider Protocol — implement this for any LLM API
# ============================================================

class Provider(Protocol):
    """Minimal interface for an LLM provider. Implement complete() and you're done."""

    name: str

    def complete(self, system: str, user: str, temperature: float = 0.7) -> str:
        """Send a prompt, get text back. That's it."""
        ...


# ============================================================
# Anthropic Provider (included — works out of the box)
# ============================================================

class AnthropicProvider:
    name = "claude"

    def __init__(self, model: str = "claude-sonnet-4-20250514"):
        self.model = model
        self.api_key = os.environ.get("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise EnvironmentError("ANTHROPIC_API_KEY not set")

    def complete(self, system: str, user: str, temperature: float = 0.7) -> str:
        import urllib.request
        import urllib.error

        body = json.dumps({
            "model": self.model,
            "max_tokens": 4096,
            "temperature": temperature,
            "system": system,
            "messages": [{"role": "user", "content": user}],
        }).encode()

        req = urllib.request.Request(
            "https://api.anthropic.com/v1/messages",
            data=body,
            headers={
                "Content-Type": "application/json",
                "x-api-key": self.api_key,
                "anthropic-version": "2023-06-01",
            },
        )

        try:
            with urllib.request.urlopen(req) as resp:
                data = json.loads(resp.read())
                return "".join(b["text"] for b in data["content"] if b["type"] == "text")
        except urllib.error.HTTPError as e:
            error_body = e.read().decode()
            raise RuntimeError(f"Anthropic API error {e.code}: {error_body}")


# ============================================================
# Skeleton providers — LLMs or users fill these in
# ============================================================

class OpenAIProvider:
    """Skeleton. pip install openai, then implement complete()."""
    name = "openai"

    def __init__(self, model: str = "gpt-4o"):
        self.model = model
        self.api_key = os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            raise EnvironmentError("OPENAI_API_KEY not set")

    def complete(self, system: str, user: str, temperature: float = 0.7) -> str:
        # Implement:
        # from openai import OpenAI
        # client = OpenAI(api_key=self.api_key)
        # response = client.chat.completions.create(
        #     model=self.model,
        #     messages=[
        #         {"role": "system", "content": system},
        #         {"role": "user", "content": user},
        #     ],
        #     temperature=temperature,
        # )
        # return response.choices[0].message.content
        raise NotImplementedError("OpenAI provider not implemented. See comments above.")


class GoogleProvider:
    """Skeleton. pip install google-generativeai, then implement complete()."""
    name = "google"

    def __init__(self, model: str = "gemini-2.5-flash"):
        self.model = model
        self.api_key = os.environ.get("GOOGLE_API_KEY")
        if not self.api_key:
            raise EnvironmentError("GOOGLE_API_KEY not set")

    def complete(self, system: str, user: str, temperature: float = 0.7) -> str:
        # Implement:
        # import google.generativeai as genai
        # genai.configure(api_key=self.api_key)
        # model = genai.GenerativeModel(self.model, system_instruction=system)
        # response = model.generate_content(user, generation_config={"temperature": temperature})
        # return response.text
        raise NotImplementedError("Google provider not implemented. See comments above.")


class BedrockProvider:
    """Skeleton. pip install boto3, then implement complete()."""
    name = "bedrock"

    def __init__(self, model: str = "anthropic.claude-sonnet-4-20250514-v1:0", region: str = "us-east-1"):
        self.model = model
        self.region = region

    def complete(self, system: str, user: str, temperature: float = 0.7) -> str:
        # Implement:
        # import boto3
        # client = boto3.client("bedrock-runtime", region_name=self.region)
        # body = json.dumps({
        #     "anthropic_version": "bedrock-2023-05-31",
        #     "max_tokens": 4096,
        #     "temperature": temperature,
        #     "system": system,
        #     "messages": [{"role": "user", "content": user}],
        # })
        # response = client.invoke_model(modelId=self.model, body=body)
        # result = json.loads(response["body"].read())
        # return "".join(b["text"] for b in result["content"] if b["type"] == "text")
        raise NotImplementedError("Bedrock provider not implemented. See comments above.")


# Provider registry — add yours here
PROVIDERS = {
    "claude": AnthropicProvider,
    "openai": OpenAIProvider,
    "google": GoogleProvider,
    "bedrock": BedrockProvider,
}


def get_provider(name: str) -> Provider:
    if name not in PROVIDERS:
        print(f"Unknown provider: {name}. Available: {', '.join(PROVIDERS.keys())}", file=sys.stderr)
        sys.exit(1)
    return PROVIDERS[name]()


# ============================================================
# Framework Prompts — the actual reasoning stages
# ============================================================

FRAMEWORKS = {
    "FPR": {
        "name": "First Principles",
        "system": "You are a first-principles analyst. Question every assumption.",
        "prompt": """Analyze this problem using First Principles reasoning.

1. What assumptions are being made? List each one explicitly.
2. For each assumption: is it verified, plausible, or unverified?
3. What would change if each unverified assumption is wrong?
4. Is the framing of this problem itself correct, or is it solving the wrong thing?
5. What is the actual problem underneath the stated problem?

Respond in JSON:
{{
  "assumptions": [
    {{"assumption": "...", "status": "verified|plausible|unverified", "if_wrong": "..."}}
  ],
  "framing_valid": true/false,
  "reframing": "if framing is invalid, what should the real question be?",
  "key_insight": "the single most important finding"
}}

Problem:
{input}""",
    },
    "CoT": {
        "name": "Chain of Thought",
        "system": "You are a methodical analyst. Establish facts before conclusions.",
        "prompt": """Analyze this using Chain of Thought reasoning.

Walk through the problem step by step:
1. What are the established facts?
2. What is the sequence of events or dependencies?
3. What follows logically from each fact?
4. Where are the gaps in the chain?

Respond in JSON:
{{
  "facts": ["..."],
  "chain": [
    {{"step": 1, "from": "fact or prior step", "conclusion": "...", "confidence": "high|medium|low"}}
  ],
  "gaps": ["where the chain breaks or evidence is missing"],
  "key_insight": "..."
}}

Problem:
{input}""",
    },
    "RCAR": {
        "name": "Root Cause Analysis (5 Whys)",
        "system": "You are a root cause analyst. Symptoms are not causes. Keep asking why.",
        "prompt": """Analyze this using Root Cause Analysis (5 Whys).

Start with the visible problem, then ask "why?" at least 5 times:
1. What is the visible symptom?
2. Why is this happening? (Level 1)
3. Why? (Level 2)
4. Why? (Level 3)
5. Why? (Level 4)
6. Why? (Level 5 — this should be structural)

Respond in JSON:
{{
  "symptom": "the visible problem",
  "why_chain": [
    {{"level": 1, "why": "...", "evidence": "..."}}
  ],
  "root_cause": "the structural cause at the bottom",
  "structural_fix": "what would prevent recurrence",
  "key_insight": "..."
}}

Problem:
{input}""",
    },
    "GoT": {
        "name": "Graph of Thoughts",
        "system": "You are a systems thinker. Map interconnections and feedback loops.",
        "prompt": """Analyze this using Graph of Thoughts.

Map the system as interconnected nodes:
1. What are the key elements (nodes)?
2. How does each element influence the others (edges)?
3. Where are the feedback loops (reinforcing or balancing)?
4. Where are the leverage points — small changes with large effects?

Respond in JSON:
{{
  "nodes": [{{"name": "...", "role": "..."}}],
  "edges": [{{"from": "...", "to": "...", "relationship": "...", "strength": "strong|moderate|weak"}}],
  "feedback_loops": [{{"type": "reinforcing|balancing", "path": ["A", "B", "C", "A"], "effect": "..."}}],
  "leverage_points": [{{"point": "...", "why": "...", "intervention": "..."}}],
  "key_insight": "..."
}}

Problem:
{input}""",
    },
    "SMR": {
        "name": "Stakeholder Mapping",
        "system": "You are an organizational analyst. Map power, interest, and incentives.",
        "prompt": """Analyze this using Stakeholder Mapping.

For each stakeholder:
1. Who are they?
2. What do they want (stated goal)?
3. What are they actually optimizing for (real goal)?
4. What is their power to influence the outcome?
5. What would make them support vs. block this?

Respond in JSON:
{{
  "stakeholders": [
    {{
      "name": "...",
      "stated_goal": "...",
      "real_goal": "...",
      "power": "high|medium|low",
      "interest": "high|medium|low",
      "support_condition": "what would make them support this",
      "block_condition": "what would make them block this"
    }}
  ],
  "coalitions": [{{"name": "...", "members": ["..."], "shared_interest": "..."}}],
  "key_insight": "..."
}}

Problem:
{input}""",
    },
    "AdR": {
        "name": "Adversarial Reasoning",
        "system": "You are an adversarial analyst. Your mandate: find why this fails. Find what is being hidden. Find the uncomfortable truths everyone is avoiding. Do not be agreeable.",
        "prompt": """Analyze this using Adversarial Reasoning.

You have explicit permission to be uncomfortable. Surface what others won't say.

1. What is each party secretly protecting?
2. What incentives are misaligned?
3. What is the most likely way this fails?
4. What is everyone avoiding saying?
5. What would a hostile adversary exploit?

Respond in JSON:
{{
  "hidden_dynamics": [
    {{"actor": "...", "protecting": "...", "at_cost_of": "..."}}
  ],
  "misaligned_incentives": [{{"between": ["A", "B"], "conflict": "..."}}],
  "failure_modes": [
    {{"mode": "...", "likelihood": "high|medium|low", "impact": "high|medium|low", "why_ignored": "..."}}
  ],
  "uncomfortable_truths": ["things no one wants to say but are probably true"],
  "key_insight": "..."
}}

Problem:
{input}""",
    },
    "ToT": {
        "name": "Tree of Thoughts",
        "system": "You are a strategic analyst. Generate and compare multiple approaches. Do not recommend one — present tradeoffs.",
        "prompt": """Analyze this using Tree of Thoughts.

Generate 3-4 distinct strategic options. For each:
1. What is the approach?
2. What are the tradeoffs?
3. What does it optimize for? What does it sacrifice?
4. Estimated probability of success?
5. What could go wrong?

Respond in JSON:
{{
  "options": [
    {{
      "name": "short label",
      "approach": "...",
      "optimizes_for": "...",
      "sacrifices": "...",
      "success_probability": "high|medium|low",
      "risks": ["..."],
      "tradeoffs": "..."
    }}
  ],
  "comparison": "how the options differ on the dimension that matters most",
  "key_insight": "..."
}}

Problem (incorporate all prior analysis):
{input}""",
    },
    "PMR": {
        "name": "Pre-Mortem",
        "system": "You are a pre-mortem analyst. Assume this has already failed. Your job: explain why it failed. Be specific. Name the failure modes.",
        "prompt": """Run a Pre-Mortem on this decision.

It is 6 months from now. This has failed. Explain why.

1. What went wrong? (Name 3-5 specific failure modes)
2. What warning signs existed that were ignored?
3. Which assumption turned out to be wrong?
4. What should have been designed against?

Respond in JSON:
{{
  "failure_modes": [
    {{
      "what_failed": "...",
      "why": "...",
      "warning_signs": ["signs that existed but were ignored"],
      "could_have_been_prevented_by": "..."
    }}
  ],
  "most_likely_cause_of_death": "the single biggest risk",
  "design_against": ["specific mitigations to implement now"],
  "key_insight": "..."
}}

Decision/plan being evaluated:
{input}""",
    },
}


# ============================================================
# Pipeline Definitions
# ============================================================

PIPELINES = {
    "light": {
        "name": "Light Pipeline (3 stages)",
        "stages": ["RCAR", "ToT", "PMR"],
        "use_when": "Moderate decisions where framing is clear",
    },
    "standard": {
        "name": "Standard Pipeline — FPR opener (5 stages)",
        "stages": ["FPR", "RCAR", "AdR", "ToT", "PMR"],
        "use_when": "Complex decisions with ambiguity or where the brief might be wrong",
    },
    "standard-cot": {
        "name": "Standard Pipeline — CoT opener (5 stages)",
        "stages": ["CoT", "RCAR", "AdR", "ToT", "PMR"],
        "use_when": "Complex decisions where facts need establishing first",
    },
    "stakeholder": {
        "name": "Multi-Stakeholder Pipeline (5 stages)",
        "stages": ["FPR", "SMR", "AdR", "ToT", "PMR"],
        "use_when": "Competing interests, power dynamics, multiple parties",
    },
    "systems": {
        "name": "Systems Pipeline (5 stages)",
        "stages": ["FPR", "RCAR", "GoT", "ToT", "PMR"],
        "use_when": "Feedback loops, interconnected components, emergent behavior",
    },
    "review": {
        "name": "Adversarial Review (3 stages)",
        "stages": ["AdR", "ToT", "PMR"],
        "use_when": "Reviewing an existing artifact (architecture, threat model, design)",
    },
}


# ============================================================
# Pipeline Runner
# ============================================================

@dataclass
class StageResult:
    stage: str
    framework: str
    model: str
    raw: str
    parsed: Optional[dict] = None
    duration_seconds: float = 0.0
    error: Optional[str] = None


@dataclass
class PipelineResult:
    pipeline: str
    input_summary: str
    stages: list[StageResult] = field(default_factory=list)
    convergence: Optional[dict] = None
    total_duration_seconds: float = 0.0


def run_stage(
    provider: Provider,
    framework_key: str,
    accumulated_context: str,
    problem: str,
) -> StageResult:
    """Run a single reasoning stage."""
    fw = FRAMEWORKS[framework_key]
    full_input = accumulated_context + "\n\n" + problem if accumulated_context else problem
    prompt = fw["prompt"].replace("{input}", full_input)

    start = time.time()
    try:
        raw = provider.complete(system=fw["system"], user=prompt, temperature=0.7)
        duration = time.time() - start

        # Try to parse JSON from the response
        parsed = None
        try:
            # Handle markdown-wrapped JSON
            text = raw.strip()
            if text.startswith("```"):
                text = text.split("\n", 1)[1].rsplit("```", 1)[0].strip()
            parsed = json.loads(text)
        except (json.JSONDecodeError, IndexError):
            pass

        return StageResult(
            stage=framework_key,
            framework=fw["name"],
            model=provider.name,
            raw=raw,
            parsed=parsed,
            duration_seconds=round(duration, 2),
        )
    except Exception as e:
        return StageResult(
            stage=framework_key,
            framework=fw["name"],
            model=provider.name,
            raw="",
            duration_seconds=round(time.time() - start, 2),
            error=str(e),
        )


def run_convergence(provider: Provider, stages: list[StageResult], problem: str) -> dict:
    """Final convergence stage — synthesize all findings."""
    findings = []
    for s in stages:
        if s.parsed:
            findings.append(f"## {s.framework}\n{json.dumps(s.parsed, indent=2)}")
        elif s.raw:
            findings.append(f"## {s.framework}\n{s.raw}")

    system = """You are a convergence analyst. Synthesize findings from multiple reasoning stages
into a final recommendation. Focus on: genuine disagreements between stages, highest-risk items,
and actionable next steps. Do not repeat analysis — synthesize it."""

    prompt = f"""Synthesize these findings into a final recommendation.

Respond in JSON:
{{
  "summary": "2-3 sentence executive summary",
  "key_findings": ["the 3-5 most important insights across all stages"],
  "disagreements": [
    {{"between": ["stage A", "stage B"], "about": "...", "recommendation": "..."}}
  ],
  "risks_ranked": [
    {{"risk": "...", "likelihood": "high|medium|low", "impact": "high|medium|low", "mitigation": "..."}}
  ],
  "recommended_action": "what to do next",
  "navigator_decisions_needed": ["decisions that require human judgment"]
}}

Original problem: {problem}

Stage findings:
{''.join(findings)}"""

    start = time.time()
    raw = provider.complete(system=system, user=prompt, temperature=0.3)
    duration = time.time() - start

    try:
        text = raw.strip()
        if text.startswith("```"):
            text = text.split("\n", 1)[1].rsplit("```", 1)[0].strip()
        return {"result": json.loads(text), "duration_seconds": round(duration, 2)}
    except (json.JSONDecodeError, IndexError):
        return {"raw": raw, "duration_seconds": round(duration, 2)}


def run_pipeline(
    pipeline_key: str,
    problem: str,
    architect: Provider,
    challenger: Optional[Provider] = None,
) -> PipelineResult:
    """Run a full reasoning pipeline."""
    pipeline_def = PIPELINES[pipeline_key]
    result = PipelineResult(
        pipeline=pipeline_def["name"],
        input_summary=problem[:200] + "..." if len(problem) > 200 else problem,
    )

    start = time.time()
    accumulated = ""

    for i, stage_key in enumerate(pipeline_def["stages"]):
        # Alternate between architect and challenger for adversarial stages
        if stage_key == "AdR" and challenger:
            provider = challenger
        else:
            provider = architect

        print(f"  [{i+1}/{len(pipeline_def['stages'])}] {FRAMEWORKS[stage_key]['name']} ({provider.name})...", file=sys.stderr)
        stage_result = run_stage(provider, stage_key, accumulated, problem)
        result.stages.append(stage_result)

        if stage_result.error:
            print(f"  ERROR: {stage_result.error}", file=sys.stderr)
            continue

        # Accumulate context for next stage
        if stage_result.parsed:
            accumulated += f"\n\n## {stage_result.framework} findings:\n{json.dumps(stage_result.parsed, indent=2)}"
        elif stage_result.raw:
            accumulated += f"\n\n## {stage_result.framework} findings:\n{stage_result.raw}"

    # Convergence
    print(f"  [convergence] Synthesizing ({architect.name})...", file=sys.stderr)
    result.convergence = run_convergence(architect, result.stages, problem)
    result.total_duration_seconds = round(time.time() - start, 2)

    return result


# ============================================================
# Adversarial Review (artifact-focused)
# ============================================================

def run_review(
    artifact_path: str,
    architect: Provider,
    challenger: Optional[Provider] = None,
) -> PipelineResult:
    """Adversarial review of an existing artifact (architecture.md, threat_model.md, etc.)."""
    artifact = Path(artifact_path).read_text()
    problem = f"Review this artifact with an adversarial mandate. Find what is wrong, not whether it is good.\n\n{artifact}"
    return run_pipeline("review", problem, architect, challenger)


# ============================================================
# CLI
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="Security-First Reasoning Pipeline CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # -- reason command --
    reason_parser = subparsers.add_parser("reason", help="Run a reasoning pipeline on a problem")
    reason_parser.add_argument("problem", nargs="?", help="Problem statement (or - for stdin)")
    reason_parser.add_argument("--pipeline", "-p", default="standard", choices=PIPELINES.keys())
    reason_parser.add_argument("--architect", "-a", default=os.environ.get("PIPELINE_ARCHITECT", "claude"))
    reason_parser.add_argument("--challenger", "-c", default=os.environ.get("PIPELINE_CHALLENGER", None))
    reason_parser.add_argument("--output", "-o", help="Output file (default: stdout)")

    # -- review command --
    review_parser = subparsers.add_parser("review", help="Adversarial review of an artifact file")
    review_parser.add_argument("file", help="Path to artifact (architecture.md, threat_model.md, etc.)")
    review_parser.add_argument("--architect", "-a", default=os.environ.get("PIPELINE_ARCHITECT", "claude"))
    review_parser.add_argument("--challenger", "-c", default=os.environ.get("PIPELINE_CHALLENGER", None))
    review_parser.add_argument("--output", "-o", help="Output file (default: stdout)")

    # -- pipelines command --
    subparsers.add_parser("pipelines", help="List available pipeline variants")

    # -- frameworks command --
    subparsers.add_parser("frameworks", help="List available reasoning frameworks")

    args = parser.parse_args()

    if args.command == "pipelines":
        for key, p in PIPELINES.items():
            print(f"  {key:16s} {p['name']}")
            print(f"  {'':16s} Stages: {' → '.join(p['stages'])}")
            print(f"  {'':16s} Use when: {p['use_when']}")
            print()
        return

    if args.command == "frameworks":
        for key, f in FRAMEWORKS.items():
            print(f"  {key:5s} {f['name']}")
        return

    # Build providers
    architect = get_provider(args.architect)
    challenger = get_provider(args.challenger) if args.challenger else None

    if args.command == "review":
        if not Path(args.file).exists():
            print(f"File not found: {args.file}", file=sys.stderr)
            sys.exit(1)
        print(f"Adversarial review: {args.file}", file=sys.stderr)
        print(f"Architect: {args.architect}, Challenger: {args.challenger or args.architect}", file=sys.stderr)
        result = run_review(args.file, architect, challenger)

    elif args.command == "reason":
        problem = args.problem
        if problem == "-" or problem is None:
            print("Reading problem from stdin...", file=sys.stderr)
            problem = sys.stdin.read().strip()
        if not problem:
            print("No problem provided.", file=sys.stderr)
            sys.exit(1)

        print(f"Pipeline: {PIPELINES[args.pipeline]['name']}", file=sys.stderr)
        print(f"Architect: {args.architect}, Challenger: {args.challenger or args.architect}", file=sys.stderr)
        result = run_pipeline(args.pipeline, problem, architect, challenger)

    # Output JSON
    output = json.dumps(asdict(result), indent=2, default=str)
    if hasattr(args, 'output') and args.output:
        Path(args.output).write_text(output)
        print(f"Output written to {args.output}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
