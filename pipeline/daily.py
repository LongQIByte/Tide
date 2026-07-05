"""One-command orchestration: ingest -> interpret top N -> (optionally) publish.

Usage:
    python -m pipeline.daily --date YYYY-MM-DD [--top N] [--prune] [--publish]

Idempotent: papers that already have a deep_dive are skipped, so re-running
a date (or a whole week in CI) only does the missing work.
"""

from __future__ import annotations

import argparse
import traceback
from datetime import date as _date

from . import interpret, run


def process_date(date: str, top: int, prune: bool) -> int:
    """Returns the number of papers successfully deep-dived for the date."""
    out_dir = run.run(date=date, top=top, skip_figures=False)
    selected_file = out_dir / "selected.json"
    if not selected_file.exists():
        return 0

    import json

    selected = json.loads(selected_file.read_text())
    done = 0
    for paper in selected:
        pid = paper["arxiv_id"]
        paper_dir = out_dir / pid
        if (paper_dir / "deep_dive.zh.md").exists():
            print(f"  {pid}: deep dive exists, skipping")
            done += 1
            continue
        if not paper.get("html_available", True) or not (paper_dir / "paper.html").exists():
            print(f"  {pid}: no arXiv HTML, skipping deep dive")
            continue
        try:
            interpret.deep_dive(date, pid, prune=prune)
            done += 1
        except Exception:
            print(f"  {pid}: deep dive FAILED, continuing with the rest")
            traceback.print_exc()
    return done


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", help="YYYY-MM-DD (default: today)")
    ap.add_argument("--top", type=int, default=5)
    ap.add_argument("--prune", action="store_true",
                    help="keep only committable files (md + webp figures)")
    ap.add_argument("--publish", action="store_true",
                    help="rebuild the whole static site afterwards")
    args = ap.parse_args()

    date = args.date or _date.today().isoformat()
    n = process_date(date, args.top, args.prune)
    print(f"{date}: {n} deep dive(s) ready")
    if args.publish:
        from . import publish

        publish.publish()


if __name__ == "__main__":
    main()
