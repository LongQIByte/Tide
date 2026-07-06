"""Manually add arXiv papers to a day's tide (editor's picks).

Usage:
    python -m pipeline.add_paper 2407.04152 2202.07074 [--date YYYY-MM-DD] [--prune]

Fetches metadata from the arXiv API, appends entries to the date's
selected.json (source: "manual"), then runs the same fetch + deep-dive
pipeline used for HF-selected papers.
"""

from __future__ import annotations

import argparse
import json
import re
import xml.etree.ElementTree as ET
from datetime import date as _date

import requests

from . import arxiv_fetch, interpret
from .run import DATA_DIR

ATOM = "{http://www.w3.org/2005/Atom}"


def canonical_id(raw: str) -> str:
    """'2407.04152v2' or a filename like '2407.04152v2(1).pdf' -> '2407.04152'."""
    m = re.search(r"(\d{4}\.\d{4,5})", raw)
    if not m:
        raise ValueError(f"no arXiv id found in {raw!r}")
    return m.group(1)


def fetch_metadata(arxiv_id: str) -> dict:
    resp = requests.get(
        "https://export.arxiv.org/api/query",
        params={"id_list": arxiv_id},
        headers={"User-Agent": arxiv_fetch.USER_AGENT},
        timeout=30,
    )
    resp.raise_for_status()
    entry = ET.fromstring(resp.text).find(f"{ATOM}entry")
    if entry is None or entry.find(f"{ATOM}title") is None:
        raise ValueError(f"arXiv API returned no entry for {arxiv_id}")
    title = re.sub(r"\s+", " ", entry.find(f"{ATOM}title").text).strip()
    abstract = re.sub(r"\s+", " ", entry.find(f"{ATOM}summary").text).strip()
    authors = [a.find(f"{ATOM}name").text for a in entry.findall(f"{ATOM}author")]
    published = entry.find(f"{ATOM}published").text[:10]
    return {
        "arxiv_id": arxiv_id,
        "title": title,
        "abstract": abstract,
        "upvotes": 0,
        "authors": authors,
        "organization": None,
        "github_repo": None,
        "github_stars": None,
        "ai_keywords": [],
        "published_at": published,
        "hf_url": None,
        "arxiv_url": f"https://arxiv.org/abs/{arxiv_id}",
        "source": "manual",
    }


def add_papers(ids: list[str], date: str, prune: bool) -> None:
    out_dir = DATA_DIR / date
    out_dir.mkdir(parents=True, exist_ok=True)
    selected_file = out_dir / "selected.json"
    selected = (
        json.loads(selected_file.read_text()) if selected_file.exists() else []
    )
    existing = {p["arxiv_id"] for p in selected}

    for raw in ids:
        pid = canonical_id(raw)
        if pid in existing:
            print(f"{pid}: already in {date}, skipping metadata")
        else:
            print(f"{pid}: fetching arXiv metadata ...")
            paper = fetch_metadata(pid)
            selected.append(paper)
            existing.add(pid)
            print(f"      {paper['title'][:70]}")

        paper = next(p for p in selected if p["arxiv_id"] == pid)
        paper_dir = out_dir / pid
        paper_dir.mkdir(exist_ok=True)
        if (paper_dir / "deep_dive.zh.md").exists():
            print(f"      deep dive exists, skipping")
            continue
        if not (paper_dir / "paper.html").exists():
            result = arxiv_fetch.fetch_html(pid)
            if result is None:
                print(f"      no arXiv/ar5iv HTML available, cannot deep-dive")
                paper["html_available"] = False
                selected_file.write_text(
                    json.dumps(selected, ensure_ascii=False, indent=2)
                )
                continue
            html, base_url = result
            (paper_dir / "paper.html").write_text(html)
            figures = arxiv_fetch.extract_figures(html, base_url)
            figures = arxiv_fetch.download_figures(figures, paper_dir)
            paper["html_available"] = True
            paper["figures"] = figures
            print(f"      html ok, {len(figures)} figures")
        selected_file.write_text(json.dumps(selected, ensure_ascii=False, indent=2))
        interpret.deep_dive(date, pid, prune=prune)

    selected_file.write_text(json.dumps(selected, ensure_ascii=False, indent=2))
    print(f"Done: {len(ids)} paper(s) in {date}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("ids", nargs="+", help="arXiv ids (versions/filenames ok)")
    ap.add_argument("--date", help="date bucket, default today")
    ap.add_argument("--prune", action="store_true")
    args = ap.parse_args()
    add_papers(args.ids, args.date or _date.today().isoformat(), args.prune)


if __name__ == "__main__":
    main()
