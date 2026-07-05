"""Fetch daily paper candidates from the HuggingFace Daily Papers API."""

from __future__ import annotations

import requests

HF_DAILY_API = "https://huggingface.co/api/daily_papers"
USER_AGENT = "Tide/0.1 (https://github.com/JavanTang/Tide)"


def fetch_candidates(date: str | None = None, limit: int = 100) -> list[dict]:
    """Return the day's candidate papers as a list of normalized dicts.

    date: "YYYY-MM-DD"; None means the latest batch.
    """
    params: dict[str, str | int] = {"limit": limit}
    if date:
        params["date"] = date
    resp = requests.get(
        HF_DAILY_API, params=params, headers={"User-Agent": USER_AGENT}, timeout=30
    )
    resp.raise_for_status()
    return [_normalize(item) for item in resp.json()]


def _normalize(item: dict) -> dict:
    paper = item.get("paper", {})
    org = paper.get("organization") or {}
    return {
        "arxiv_id": paper.get("id"),
        "title": paper.get("title", "").strip(),
        "abstract": paper.get("summary", "").strip(),
        "upvotes": paper.get("upvotes", 0),
        "authors": [a.get("name") for a in paper.get("authors", [])],
        "organization": org.get("fullname") or org.get("name"),
        "github_repo": paper.get("githubRepo"),
        "github_stars": paper.get("githubStars"),
        "ai_keywords": paper.get("ai_keywords", []),
        "published_at": paper.get("publishedAt"),
        "hf_url": f"https://huggingface.co/papers/{paper.get('id')}",
        "arxiv_url": f"https://arxiv.org/abs/{paper.get('id')}",
    }


def select_top(candidates: list[dict], n: int = 5) -> list[dict]:
    """Placeholder selection: rank by upvotes (LLM scoring will replace this)."""
    ranked = sorted(candidates, key=lambda c: c.get("upvotes", 0), reverse=True)
    return ranked[:n]
