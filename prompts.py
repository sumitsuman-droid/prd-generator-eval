PRD_GENERATION_PROMPT = """You are a senior product manager. Given a product idea, produce a PRD as valid JSON — no markdown, no code fences, no extra text, just the raw JSON object.

Product idea: {user_idea}

Reference examples (may be empty):
{retrieved_examples}

Return a single JSON object with exactly these keys:
{{
  "title": "string — a descriptive product name with a brief subtitle in the format 'ProductName: Subtitle describing what it does and for whom'. Example: 'MarketLens: Retail Media Insights Dashboard for B2B Marketplace Advertisers' or 'ETA Live: Real-Time Last-Mile Delivery Tracking for Food Delivery Customers'. The product name should be 1-2 words, the subtitle should be 6-12 words and describe the product's function and target user.",
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
- Every user story persona MUST correspond to one of the entries in target_users. Use the persona's distinguishing trait (e.g., "As a dual-income household tracking shared expenses across accounts, I want..."), not a generic label ("As a user...").
- Across all user stories, at least 3 distinct target_users personas must be represented.
- Output ONLY the JSON object. No preamble, no explanation."""


EVAL_PROMPT = """You are a Principal PM evaluator. Score the following PRD on five dimensions, each from 1 to 10.

PRD JSON:
{prd_json}

Dimensions:
1. specificity — Are requirements concrete and unambiguous?
2. measurability — Can success be quantified with the given metrics?
3. testability — Can acceptance criteria be verified objectively?
4. user_centricity — Do user stories reflect real, specific user needs with named, differentiated personas?
   Score 9-10: Persona names a concrete role and context (e.g., "remote engineer across timezones"); each story captures a genuine pain point; outcome is meaningful and non-circular.
   Score 4-6: Generic persona labels ("user", "admin", "manager") with plausible but interchangeable stories; outcomes stated but shallow or obvious; no differentiation between persona types.
   Score 1-3: Template-level personas ("As a user, I want to use the app"); stories are circular, trivially obvious, or purely structural; outcome clause is absent, restates the action, or adds no information.
5. completeness — Are all standard PRD sections present AND does each contain substantive, non-filler content? Section presence alone does not raise the score; content depth is the primary signal.
   Score 9-10: All sections present with specific, non-generic content; problem statement explains urgency; metrics have real baselines; risks are non-obvious; out-of-scope entries are deliberate decisions.
   Score 4-6: All or most sections present but content is thin — single-sentence entries, placeholder-quality text, metrics without baselines, risks that are generic boilerplate ("scope creep", "unclear requirements").
   Score 1-3: Multiple sections missing, OR all sections present but each is a vague filler sentence; no section would survive a real PM review; document is structurally complete but informationally empty.

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
