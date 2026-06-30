"""End-to-end mock pipeline."""
from __future__ import annotations

import os

from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel

from adapters.reddit_public import discover
from db.database import (
    fetch_summary,
    init_db,
    insert_classification,
    insert_post,
    insert_reply,
    update_post_status,
)
from workers.links import build_tracked_link
from workers.llm import classify, generate_reply
from workers.poster import post_reply

load_dotenv()
console = Console()


def _csv(name: str, default: str = "") -> list[str]:
    return [x.strip() for x in os.getenv(name, default).split(",") if x.strip()]


def run_pipeline() -> None:
    init_db()
    subs = _csv("SUBREDDITS", "EstatePlanning,personalfinance")
    keywords = _csv("KEYWORDS", "will,estate planning,power of attorney")
    console.print(Panel.fit(f"subs: {subs}", title="Pipeline start"))
    posts = discover(subs, keywords, per_sub=10)
    new_post_ids: list[tuple[int, dict]] = []
    for p in posts:
        pid = insert_post(p)
        if pid:
            new_post_ids.append((pid, p))
    for pid, post in new_post_ids:
        verdict = classify(post)
        insert_classification(pid, verdict["is_relevant"], verdict["intent"], verdict["reason"])
        if not verdict["is_relevant"]:
            update_post_status(pid, "rejected")
            continue
        reply_template = generate_reply(post)
        short_link, _full = build_tracked_link(post)
        reply_text = reply_template.replace("{LINK}", short_link)
        result = post_reply(post, reply_text)
        insert_reply(pid, reply_text, short_link, result["status"])
        update_post_status(pid, "drafted")
    s = fetch_summary()
    console.print(f"Posts: {s['posts']}  Replies: {s['replies_drafted']}")


if __name__ == "__main__":
    run_pipeline()
