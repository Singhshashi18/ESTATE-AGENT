"""Read-only Reddit discovery using public JSON endpoints."""
from __future__ import annotations

import time
from typing import Iterable

import requests

from adapters.fixtures import FIXTURE_POSTS

UA = {"User-Agent": "estate-agent-discovery/0.1"}


def fetch_subreddit_new(subreddit: str, limit: int = 10) -> list[dict]:
    url = f"https://www.reddit.com/r/{subreddit}/new.json?limit={limit}"
    resp = requests.get(url, headers=UA, timeout=15)
    resp.raise_for_status()
    out = []
    for c in resp.json().get("data", {}).get("children", []):
        d = c.get("data", {})
        out.append({
            "platform": "reddit",
            "external_id": d.get("id"),
            "subreddit": d.get("subreddit"),
            "title": d.get("title", ""),
            "body": d.get("selftext", ""),
            "url": f"https://www.reddit.com{d.get('permalink', '')}",
            "author": d.get("author"),
        })
    return out


def keyword_match(post: dict, keywords: Iterable[str]) -> bool:
    text = f"{post.get('title', '')} {post.get('body', '')}".lower()
    return any(k.lower() in text for k in keywords)


def discover(subreddits: list[str], keywords: list[str], per_sub: int = 10) -> list[dict]:
    results: list[dict] = []
    failures = 0
    for sub in subreddits:
        try:
            posts = fetch_subreddit_new(sub, limit=per_sub)
        except Exception as e:
            print(f"  ! failed r/{sub}: {e}")
            failures += 1
            continue
        matched = [p for p in posts if keyword_match(p, keywords)]
        results.extend(matched)
        time.sleep(1)
    if not results and failures == len(subreddits):
        print("  > all live requests blocked; falling back to local fixtures")
        results = list(FIXTURE_POSTS)
    return results
