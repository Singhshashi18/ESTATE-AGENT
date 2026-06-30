"""Posting layer. DRY_RUN logs only."""
from __future__ import annotations

import os
from datetime import datetime, timezone

from dotenv import load_dotenv

load_dotenv()

DRY_RUN = os.getenv("DRY_RUN", "true").lower() == "true"


def post_reply(post: dict, reply_text: str) -> dict:
    if DRY_RUN:
        return {
            "status": "dry_run",
            "posted_url": None,
            "posted_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        }
    return {"status": "pending", "posted_url": None, "posted_at": None}
