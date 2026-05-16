PRD_GENERATION_PROMPT = """You are a senior product manager. Given a product idea, produce a PRD as valid JSON — no markdown, no code fences, no extra text, just the raw JSON object.

Product idea: {user_idea}

Reference examples (may be empty):
{retrieved_examples}

Return a single JSON object with exactly these keys:
{{
  "title": "string — concise product name",
  "problem_statement": "string — 2-4 sentences describing the problem, who has it, and why it matters now",
  "target_users": ["string", ...],
  "user_stories": ["As a <persona>, I want <action> so that <outcome>", ...],
  "acceptance_criteria": ["string — specific, testable criterion", ...],
  "success_metrics": [
    {{"metric": "string", "baseline": "string", "target": "string"}},
    ...
  ],
  "risks_open_questions": ["string", ...],
  "out_of_scope": ["string", ...]
}}

Rules:
- Every list must have at least 3 items.
- success_metrics must have at least 3 objects, each with metric, baseline, and target.
- Be concrete and specific — avoid vague language like "improve user experience".
- Output ONLY the JSON object. No preamble, no explanation."""


EVAL_PROMPT = """You are a Principal PM evaluator. Score the following PRD on five dimensions, each from 1 to 10.

PRD JSON:
{prd_json}

Dimensions:
1. specificity — Are requirements concrete and unambiguous?
2. measurability — Can success be quantified with the given metrics?
3. testability — Can acceptance criteria be verified objectively?
4. user_centricity — Do user stories reflect real user needs with clear personas?
5. completeness — Are all standard PRD sections present and sufficiently detailed?

Weighted average for overall_score: specificity 25%, measurability 20%, testability 20%, user_centricity 20%, completeness 15%.

Return a single JSON object — no markdown, no code fences, no extra text:
{{
  "scores": {{
    "specificity":     {{"score": <1-10>, "reason": "one sentence"}},
    "measurability":   {{"score": <1-10>, "reason": "one sentence"}},
    "testability":     {{"score": <1-10>, "reason": "one sentence"}},
    "user_centricity": {{"score": <1-10>, "reason": "one sentence"}},
    "completeness":    {{"score": <1-10>, "reason": "one sentence"}}
  }},
  "overall_score": <float rounded to 1 decimal>,
  "top_3_improvements": ["string", "string", "string"]
}}

Output ONLY the JSON object."""
