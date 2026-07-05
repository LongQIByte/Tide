"""Tide ingestion pipeline: HF Daily Papers -> select -> arXiv full text + figures.

Usage:
    python -m pipeline.run [--date YYYY-MM-DD] [--top N] [--skip-figures]

Output layout:
    data/<date>/candidates.json          all candidates of the day
    data/<date>/selected.json            the selected few (with figure metadata)
    data/<date>/<arxiv_id>/paper.html    official arXiv HTML full text
    data/<date>/<arxiv_id>/figN_M.png    downloaded figures
"""

from __future__ import annotations

import argparse
import json
from datetime import date as _date
from pathlib import Path

from . import arxiv_fetch, hf_daily

DATA_DIR = Path(__file__).resolve().parent.parent / "data"


def run(date: str | None, top: int, skip_figures: bool) -> Path:
    day = date or _date.today().isoformat()
    out_dir = DATA_DIR / day
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"[1/3] Fetching HF Daily Papers ({date or 'latest'}) ...")
    candidates = hf_daily.fetch_candidates(date=date)
    (out_dir / "candidates.json").write_text(
        json.dumps(candidates, ensure_ascii=False, indent=2)
    )
    print(f"      {len(candidates)} candidates -> {out_dir / 'candidates.json'}")
    if not candidates:
        print("      No papers for this date (weekend/holiday?). Done.")
        return out_dir

    selected = hf_daily.select_top(candidates, n=top)
    print(f"[2/3] Selected top {len(selected)} by upvotes:")
    for c in selected:
        print(f"      {c['upvotes']:>4}▲  {c['arxiv_id']}  {c['title'][:70]}")

    print("[3/3] Fetching arXiv HTML + figures ...")
    for c in selected:
        paper_dir = out_dir / c["arxiv_id"]
        paper_dir.mkdir(exist_ok=True)
        result = arxiv_fetch.fetch_html(c["arxiv_id"])
        if result is None:
            print(f"      {c['arxiv_id']}: no HTML version available, skipped")
            c["html_available"] = False
            continue
        html, base_url = result
        (paper_dir / "paper.html").write_text(html)
        figures = arxiv_fetch.extract_figures(html, base_url)
        if not skip_figures:
            figures = arxiv_fetch.download_figures(figures, paper_dir)
        c["html_available"] = True
        c["figures"] = figures
        print(f"      {c['arxiv_id']}: html ok, {len(figures)} figures")

    (out_dir / "selected.json").write_text(
        json.dumps(selected, ensure_ascii=False, indent=2)
    )
    print(f"Done. Output in {out_dir}")
    return out_dir


def main() -> None:
    ap = argparse.ArgumentParser(description="Tide ingestion pipeline")
    ap.add_argument("--date", help="YYYY-MM-DD (default: latest batch)")
    ap.add_argument("--top", type=int, default=5, help="papers to select")
    ap.add_argument("--skip-figures", action="store_true", help="don't download images")
    args = ap.parse_args()
    run(args.date, args.top, args.skip_figures)


if __name__ == "__main__":
    main()
