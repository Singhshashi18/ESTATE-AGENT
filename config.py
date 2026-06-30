"""Centralized config + safety rails.

Reads env once, validates required keys depending on mode, and exposes
the limits used by the pipeline.
"""
from __future__ import annotations

import os
import sys

from dotenv import load_dotenv

load_dotenv()


def _bool(name: str, default: str = "false") -> bool:
    return os.getenv(name, default).lower() == "true"


def _int(name: str, default: int) -> int:
    try:
        return int(os.getenv(name, str(default)))
    except ValueError:
        return default


def _csv(name: str, default: str = "") -> list[str]:
    return [x.strip() for x in os.getenv(name, default).split(",") if x.strip()]


# --- mode flags
DRY_RUN        = _bool("DRY_RUN", "true")
HUMAN_APPROVAL = _bool("HUMAN_APPROVAL", "true")
MOCK_LLM       = _bool("MOCK_LLM", "true")

# --- targets
SUBREDDITS         = _csv("SUBREDDITS", "EstatePlanning,personalfinance")
KEYWORDS           = _csv("KEYWORDS", "will,estate planning,power of attorney")
POSTS_PER_SUBREDDIT = _int("POSTS_PER_SUBREDDIT", 10)

# --- safety rails
MAX_REPLIES_PER_RUN     = _int("MAX_REPLIES_PER_RUN", 5)
MAX_REPLIES_PER_SUB_RUN = _int("MAX_REPLIES_PER_SUB_RUN", 2)
REPLY_DELAY_SECONDS     = _int("REPLY_DELAY_SECONDS", 30)

# --- required strings
DATABASE_URL   = os.getenv("DATABASE_URL", "")
PRODUCT_URL    = os.getenv("PRODUCT_URL", "")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")


def validate_or_exit() -> None:
    """Fail fast if required config is missing for the chosen mode."""
    errs: list[str] = []

    if not DATABASE_URL:
        errs.append("DATABASE_URL is required")
    if not PRODUCT_URL:
        errs.append("PRODUCT_URL is required")

    if not MOCK_LLM and not OPENAI_API_KEY:
        errs.append("OPENAI_API_KEY is required when MOCK_LLM=false")

    if not DRY_RUN and not HUMAN_APPROVAL:
        # Going fully live -> Reddit creds must exist.
        for k in ("REDDIT_CLIENT_ID", "REDDIT_CLIENT_SECRET",
                  "REDDIT_USERNAME", "REDDIT_PASSWORD"):
            if not os.getenv(k):
                errs.append(f"{k} is required when DRY_RUN=false")

    if errs:
        print("Config error(s):")
        for e in errs:
            print(f"  - {e}")
        sys.exit(1)
