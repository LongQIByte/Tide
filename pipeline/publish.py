"""Render ingested + interpreted papers into a static site.

Usage:
    python -m pipeline.publish --date YYYY-MM-DD

Reads  data/<date>/selected.json and deep_dive.{zh,en}.md per paper.
Writes site/index.html, site/<date>/<id>/{zh,en}.html and copies figures.
"""

from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

import markdown

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
SITE_DIR = Path(__file__).resolve().parent.parent / "site"

CSS = """
:root {
  --ink: #1c2b36; --ink-soft: #4a5d6b; --sea: #0e6e8c; --sea-deep: #0a4f66;
  --foam: #f6f9fa; --sand: #fffdf8; --line: #dfe8ec;
}
* { box-sizing: border-box; }
body {
  margin: 0; color: var(--ink); background: var(--sand);
  font-family: "Charter", "Songti SC", "Noto Serif SC", Georgia, serif;
  line-height: 1.85; font-size: 17px;
}
header.site {
  background: linear-gradient(160deg, var(--sea-deep), var(--sea));
  color: #fff; padding: 2.2rem 1.5rem 2rem;
}
header.site .wrap, main { max-width: 780px; margin: 0 auto; }
header.site h1 { margin: 0; font-size: 1.9rem; letter-spacing: .04em; }
header.site h1 a { color: #fff; text-decoration: none; }
header.site p { margin: .4rem 0 0; opacity: .82; font-size: .95rem; }
main { padding: 2.5rem 1.5rem 4rem; }
h1, h2, h3 { line-height: 1.4; color: var(--sea-deep); }
article h1 { font-size: 1.55rem; }
h2 {
  font-size: 1.25rem; margin-top: 2.6rem; padding-left: .7rem;
  border-left: 4px solid var(--sea);
}
a { color: var(--sea); }
blockquote {
  margin: 1.2rem 0; padding: .9rem 1.2rem; background: var(--foam);
  border-left: 4px solid var(--line); color: var(--ink-soft);
  font-size: .95rem;
}
img { max-width: 100%; border: 1px solid var(--line); border-radius: 6px;
      background: #fff; padding: 6px; margin: 1rem 0 .2rem; }
hr { border: none; border-top: 1px dashed var(--line); margin: 2.5rem 0; }
code { background: var(--foam); padding: .1em .35em; border-radius: 4px;
       font-size: .88em; }
.meta { color: var(--ink-soft); font-size: .92rem; }
.lang-switch { float: right; font-size: .85rem; }
.card {
  border: 1px solid var(--line); border-radius: 10px; background: #fff;
  padding: 1.2rem 1.4rem; margin: 1.2rem 0;
}
.card h3 { margin: 0 0 .4rem; font-size: 1.12rem; }
.card h3 a { text-decoration: none; }
.card .abs { color: var(--ink-soft); font-size: .93rem; margin: .5rem 0 0;
             display: -webkit-box; -webkit-line-clamp: 3;
             -webkit-box-orient: vertical; overflow: hidden; }
.badge { display: inline-block; background: var(--foam); color: var(--sea-deep);
         border: 1px solid var(--line); border-radius: 99px;
         padding: .05rem .6rem; font-size: .8rem; margin-right: .4rem; }
footer { text-align: center; color: var(--ink-soft); font-size: .85rem;
         padding: 2rem 0 3rem; }
"""

PAGE = """<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title} · Tide</title>
<style>{css}</style>
</head>
<body>
<header class="site"><div class="wrap">
<h1><a href="{home}">🌊 Tide</a></h1>
<p>{tagline}</p>
</div></header>
<main>{body}</main>
<footer>Tide · 理解是无法外包的 / Understanding cannot be outsourced</footer>
</body>
</html>
"""

TAGLINE_ZH = "资讯如潮汐。我们挑出值得研究的浪，并认真讲解它。"
TAGLINE_EN = "Information moves like the tide. We pick the waves worth studying."


def render_paper(date: str, paper: dict, lang: str) -> str | None:
    paper_dir = DATA_DIR / date / paper["arxiv_id"]
    md_file = paper_dir / f"deep_dive.{lang}.md"
    if not md_file.exists():
        return None
    body = markdown.markdown(
        md_file.read_text(), extensions=["tables", "fenced_code"]
    )
    other = "en" if lang == "zh" else "zh"
    other_label = "English" if lang == "zh" else "中文"
    switch = f'<div class="lang-switch"><a href="{other}.html">{other_label}</a></div>'
    back = "← 今日潮汐" if lang == "zh" else "← Today's tide"
    body = f'{switch}<p class="meta"><a href="../../index.html">{back}</a></p><article>{body}</article>'
    return PAGE.format(
        lang=lang,
        title=paper["title"],
        css=CSS,
        home="../../index.html",
        tagline=TAGLINE_ZH if lang == "zh" else TAGLINE_EN,
        body=body,
    )


def render_index(date: str, papers: list[dict]) -> str:
    cards = []
    for p in papers:
        has_dive = (DATA_DIR / date / p["arxiv_id"] / "deep_dive.zh.md").exists()
        link = f'{date}/{p["arxiv_id"]}/zh.html' if has_dive else p["arxiv_url"]
        note = "" if has_dive else '<span class="badge">深潜未生成 · 链接原文</span>'
        org = f'<span class="badge">{p["organization"]}</span>' if p.get("organization") else ""
        cards.append(
            f'<div class="card"><h3><a href="{link}">{p["title"]}</a></h3>'
            f'<span class="badge">▲ {p["upvotes"]}</span>{org}{note}'
            f'<p class="abs">{p["abstract"]}</p></div>'
        )
    body = (
        f"<h2 style='margin-top:0;border:none;padding:0'>今日潮汐 · {date}</h2>"
        + "".join(cards)
    )
    return PAGE.format(
        lang="zh", title=f"今日潮汐 {date}", css=CSS, home="index.html",
        tagline=TAGLINE_ZH, body=body,
    )


def publish(date: str) -> Path:
    day_dir = DATA_DIR / date
    papers = json.loads((day_dir / "selected.json").read_text())
    out_day = SITE_DIR / date
    out_day.mkdir(parents=True, exist_ok=True)

    for p in papers:
        paper_dir = day_dir / p["arxiv_id"]
        out_paper = out_day / p["arxiv_id"]
        out_paper.mkdir(exist_ok=True)
        for lang in ("zh", "en"):
            html = render_paper(date, p, lang)
            if html is None:
                continue
            (out_paper / f"{lang}.html").write_text(html)
        for img in paper_dir.glob("fig*_*.*"):
            shutil.copy(img, out_paper / img.name)

    (SITE_DIR / "index.html").write_text(render_index(date, papers))
    print(f"Site written to {SITE_DIR}")
    return SITE_DIR


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", required=True)
    args = ap.parse_args()
    publish(args.date)


if __name__ == "__main__":
    main()
