"""LLM wrapper. Has TWO modes:
   - MOCK_LLM=true  -> deterministic canned answers (no API key needed)
   - MOCK_LLM=false -> real OpenAI calls
"""
from __future__ import annotations

import json
import os
import random
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

MOCK_LLM = os.getenv("MOCK_LLM", "true").lower() == "true"
OPENAI_KEY = os.getenv("OPENAI_API_KEY", "")
MODEL_CLS = os.getenv("OPENAI_MODEL_CLASSIFIER", "gpt-4o-mini")
MODEL_GEN = os.getenv("OPENAI_MODEL_GENERATOR", "gpt-4o-mini")

PROMPT_DIR = Path(__file__).parent.parent / "prompts"
CLASSIFIER_PROMPT = (PROMPT_DIR / "classifier.txt").read_text(encoding="utf-8")
GENERATOR_PROMPT = (PROMPT_DIR / "generator.txt").read_text(encoding="utf-8")


# ---------- Real OpenAI client (lazy) ----------
_client = None
def _get_client():
    global _client
    if _client is None:
        from openai import OpenAI
        _client = OpenAI(api_key=OPENAI_KEY)
    return _client


# ---------- Classifier ----------
def classify(post: dict) -> dict:
    """Return {is_relevant: bool, intent: str, reason: str}."""
    if MOCK_LLM or not OPENAI_KEY:
        return _mock_classify(post)

    user_msg = f"TITLE: {post.get('title','')}\nBODY: {post.get('body','')[:1500]}"
    resp = _get_client().chat.completions.create(
        model=MODEL_CLS,
        messages=[
            {"role": "system", "content": CLASSIFIER_PROMPT},
            {"role": "user",   "content": user_msg},
        ],
        temperature=0,
        response_format={"type": "json_object"},
    )
    raw = resp.choices[0].message.content or "{}"
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        data = {"is_relevant": False, "intent": "parse_error", "reason": raw[:200]}
    return {
        "is_relevant": bool(data.get("is_relevant", False)),
        "intent":      str(data.get("intent", "")),
        "reason":      str(data.get("reason", "")),
    }


# ---------- Generator ----------
def generate_reply(post: dict) -> str:
    """Return reply text containing {LINK} placeholder."""
    if MOCK_LLM or not OPENAI_KEY:
        return _mock_reply(post)

    user_msg = (
        f"POST TITLE: {post.get('title','')}\n"
        f"POST BODY: {post.get('body','')[:2000]}\n"
        f"SUBREDDIT: r/{post.get('subreddit','')}"
    )
    resp = _get_client().chat.completions.create(
        model=MODEL_GEN,
        messages=[
            {"role": "system", "content": GENERATOR_PROMPT},
            {"role": "user",   "content": user_msg},
        ],
        temperature=0.7,
    )
    return (resp.choices[0].message.content or "").strip()


# ---------- Mock fallbacks ----------
def _mock_classify(post: dict) -> dict:
    text = f"{post.get('title','')} {post.get('body','')}".lower()
    accept_terms = ("will", "estate", "power of attorney", "poa", "trust", "probate")
    reject_terms = ("rip", "passed away", "passed last", "lawsuit", "sue ", "meme",
                    "devastated", "grieving", "just died")
    if any(r in text for r in reject_terms):
        return {"is_relevant": False, "intent": "off_topic_or_grief",
                "reason": "Mock: contains rejection trigger."}
    if any(a in text for a in accept_terms):
        return {"is_relevant": True, "intent": "estate_planning_question",
                "reason": "Mock: matches accepted estate-planning topic."}
    return {"is_relevant": False, "intent": "unrelated",
            "reason": "Mock: no estate-planning keyword found."}


def _mock_reply(post: dict) -> str:
    title = post.get("title", "your situation")
    openings = [
        f"Going through the same thing a couple of years ago really opened my eyes.",
        f"This kind of question comes up a lot — totally normal to feel stuck at first.",
        f"Sorting out '{title[:60]}...' was on my list for ages before I finally tackled it.",
    ]
    middles = [
        "What helped me most was starting with a basic will + POA, then layering on a trust later.",
        "I'd start by listing your assets and beneficiaries before touching any template — saves a ton of rework.",
        "Honestly, doing it yourself is fine for simple estates; you only need an attorney once things get complex.",
    ]
    closer = (
        "I used a step-by-step guide that walked me through everything — link here if it's useful: {LINK}. "
        "Not legal advice — consult a licensed attorney for your situation."
    )
    random.seed(post.get("external_id", "x"))
    return f"{random.choice(openings)} {random.choice(middles)} {closer}"
