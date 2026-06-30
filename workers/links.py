"""UTM-tagged short link generator.

In production: hit your URL-shortener's API (YOURLS / Bitly / short.io) and
return the canonical short URL. For the mock run we just simulate it.
"""
from __future__ import annotations

import hashlib
import os
from urllib.parse import urlencode

from dotenv import load_dotenv

load_dotenv()

PRODUCT_URL    = os.getenv("PRODUCT_URL", "https://example.com/product")
SHORT_DOMAIN   = os.getenv("SHORT_DOMAIN", "https://short.example").rstrip("/")
AFFILIATE_TAG  = os.getenv("AFFILIATE_TAG", "")


def _short_code(seed: str) -> str:
    return hashlib.sha1(seed.encode()).hexdigest()[:7]


def build_tracked_link(post: dict) -> tuple[str, str]:
    """Return (short_link, full_destination_url).

    short_link        -> what we paste into the reply
    destination_url   -> what the shortener should redirect to (with UTM + affiliate)
    """
    code = _short_code(f"{post.get('platform','')}:{post.get('external_id','')}")
    params = {
        "utm_source":   post.get("platform", "social"),
        "utm_medium":   "ai_agent",
        "utm_campaign": "estate_planning",
        "utm_content":  post.get("subreddit", "") or post.get("external_id", ""),
    }
    if AFFILIATE_TAG:
        params["tag"] = AFFILIATE_TAG

    sep = "&" if "?" in PRODUCT_URL else "?"
    full = f"{PRODUCT_URL}{sep}{urlencode(params)}"
    short = f"{SHORT_DOMAIN}/{code}"
    return short, full
