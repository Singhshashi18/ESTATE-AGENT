"""Realistic mock posts used when Reddit blocks unauthenticated discovery.
Replace with PRAW once API creds arrive.
"""
from __future__ import annotations

FIXTURE_POSTS: list[dict] = [
    {
        "platform":    "reddit",
        "external_id": "fix_001",
        "subreddit":   "EstatePlanning",
        "title":       "Where do I even start with estate planning at 35?",
        "body":        "We just had our first kid and I realized we have no will, no POA, "
                       "nothing. Looking for a beginner-friendly resource that walks you "
                       "through it without paying $2k to a lawyer right away.",
        "url":         "https://reddit.com/r/EstatePlanning/comments/fix_001",
        "author":      "newdad_2026",
    },
    {
        "platform":    "reddit",
        "external_id": "fix_002",
        "subreddit":   "personalfinance",
        "title":       "Do I really need a living trust or is a will enough?",
        "body":        "Net worth is around $400k mostly in 401k and a house. "
                       "Some people online say I MUST have a trust, others say a "
                       "simple will is fine. What's the actual difference?",
        "url":         "https://reddit.com/r/personalfinance/comments/fix_002",
        "author":      "midwest_saver",
    },
    {
        "platform":    "reddit",
        "external_id": "fix_003",
        "subreddit":   "legaladvice",
        "title":       "My mom passed last week and there's no will - what now? [TX]",
        "body":        "Devastated. She didn't leave a will. House is in her name only. "
                       "I have two siblings. Where do I even begin?",
        "url":         "https://reddit.com/r/legaladvice/comments/fix_003",
        "author":      "grieving_son",
    },
    {
        "platform":    "reddit",
        "external_id": "fix_004",
        "subreddit":   "personalfinance",
        "title":       "Best high-yield savings account in 2026?",
        "body":        "Looking to park 20k. Marcus vs Ally vs Wealthfront — thoughts?",
        "url":         "https://reddit.com/r/personalfinance/comments/fix_004",
        "author":      "yield_chaser",
    },
    {
        "platform":    "reddit",
        "external_id": "fix_005",
        "subreddit":   "EstatePlanning",
        "title":       "Power of attorney template for an aging parent?",
        "body":        "Dad is 78 and starting to slip. We want to set up a durable POA "
                       "before things get harder. Are the online template kits any good "
                       "or should we always go through a lawyer?",
        "url":         "https://reddit.com/r/EstatePlanning/comments/fix_005",
        "author":      "caretaker_jen",
    },
    {
        "platform":    "reddit",
        "external_id": "fix_006",
        "subreddit":   "personalfinance",
        "title":       "Can I really write my own will using one of those online kits?",
        "body":        "I'm 42, single, no kids, just trying to make sure my sister gets "
                       "everything. Is a DIY will going to hold up in court?",
        "url":         "https://reddit.com/r/personalfinance/comments/fix_006",
        "author":      "diy_jordan",
    },
    {
        "platform":    "reddit",
        "external_id": "fix_007",
        "subreddit":   "legaladvice",
        "title":       "Probate process is dragging on for months — is this normal?",
        "body":        "My grandfather died in January, we're still in probate. Estate "
                       "is small (under 200k). The lawyer keeps saying 'almost done'.",
        "url":         "https://reddit.com/r/legaladvice/comments/fix_007",
        "author":      "frustrated_grandkid",
    },
    {
        "platform":    "reddit",
        "external_id": "fix_008",
        "subreddit":   "EstatePlanning",
        "title":       "Funny meme about lawyers",
        "body":        "[image] tag yourself I'm the will signing one",
        "url":         "https://reddit.com/r/EstatePlanning/comments/fix_008",
        "author":      "meme_lord",
    },
]
