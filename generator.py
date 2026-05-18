import json
import os
import re

import anthropic

from prompts import PRD_GENERATION_PROMPT, EVAL_PROMPT

MODEL = "claude-sonnet-4-6"
EVAL_MODEL = "claude-haiku-4-5-20251001"


def _get_api_key() -> str:
    try:
        import streamlit as st
        key = st.secrets.get("ANTHROPIC_API_KEY")
        if key:
            return key
    except Exception:
        pass
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass
    return os.environ.get("ANTHROPIC_API_KEY", "")


def _get_client() -> anthropic.Anthropic:
    return anthropic.Anthropic(api_key=_get_api_key())


def _strip_fences(text: str) -> str:
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    return text.strip()


def parse_prd_text(raw: str) -> dict:
    return json.loads(_strip_fences(raw))


def generate_prd(user_idea: str, retrieved_examples: str = "") -> dict:
    prompt = PRD_GENERATION_PROMPT.format(
        user_idea=user_idea,
        retrieved_examples=retrieved_examples or "None provided.",
    )
    message = _get_client().messages.create(
        model=MODEL,
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}],
    )
    raw = message.content[0].text
    return parse_prd_text(raw)


def evaluate_prd(prd: dict) -> dict:
    prompt = EVAL_PROMPT.format(prd_json=json.dumps(prd, indent=2))
    message = _get_client().messages.create(
        model=EVAL_MODEL,
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )
    raw = message.content[0].text
    return parse_prd_text(raw)


def generate_prd_streaming(user_idea: str, retrieved_examples: str = ""):
    """Yields raw text chunks from the streaming API. Caller assembles and parses JSON."""
    prompt = PRD_GENERATION_PROMPT.format(
        user_idea=user_idea,
        retrieved_examples=retrieved_examples or "None provided.",
    )
    with _get_client().messages.stream(
        model=MODEL,
        max_tokens=4096,
        messages=[{"role": "user", "content": prompt}],
    ) as stream:
        for text in stream.text_stream:
            yield text


def generate_prd_with_retrieval(user_idea: str) -> dict:
    from retrieval import retrieve_similar_prds
    retrieved = retrieve_similar_prds(user_idea, k=2)
    retrieved_examples = (
        "For reference, here are similar PRDs to use as style and structure "
        "guidance, not content to copy:\n\n" + retrieved
    )
    return generate_prd(user_idea, retrieved_examples=retrieved_examples)
