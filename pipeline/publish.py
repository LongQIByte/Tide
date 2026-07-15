"""Render ingested + interpreted papers into a static site.

Usage:
    python -m pipeline.publish --date YYYY-MM-DD

Reads  data/<date>/selected.json and deep_dive.{zh,en}.md per paper.
Writes site/index.html, site/<date>/<id>/{zh,en}.html and copies figures.

The abstract/background sections render as a readable article; the
figure-walkthrough section renders as a fullscreen slide deck (arrow keys,
like flipping through a talk).
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import shutil

import markdown
from PIL import Image

from pipeline.annotations import apply_annotations, load_annotations
from pipeline.math_render import protect_math
from pipeline.site_assets import CSS, DECK_JS, MATH_JAX

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
SITE_DIR = Path(__file__).resolve().parent.parent / "site"

METHOD_HEADING = {"zh": "## 方法图解", "en": "## Method, Figure by Figure"}

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
{body}
<footer>Tide · 理解是无法外包的 / Understanding cannot be outsourced</footer>
{math}
<script>{js}</script>
</body>
</html>
"""

TAGLINE_ZH = "资讯如潮汐。我们挑出值得研究的浪，并认真讲解它。"
TAGLINE_EN = "Information moves like the tide. We pick the waves worth studying."


def _md(text: str) -> str:
    return markdown.markdown(protect_math(text), extensions=["tables", "fenced_code"])


def _parse_slides(deck_md: str) -> list[dict]:
    """Split the method section into slides: image + caption + explanation."""
    slides = []
    for block in re.split(r"^---$", deck_md, flags=re.MULTILINE):
        block = block.strip()
        if not block:
            continue
        imgs = [
            re.sub(r"\.(png|jpe?g)$", ".webp", img)
            for img in re.findall(r"!\[[^\]]*\]\(([^)]+)\)", block)
        ]
        if not imgs:
            continue
        block = re.sub(r"!\[[^\]]*\]\([^)]+\)", "", block)
        cap_lines, rest = [], []
        for line in block.splitlines():
            if line.startswith(">"):
                cap_lines.append(line.lstrip("> ").strip())
            else:
                rest.append(line)
        slides.append(
            {
                "img": imgs[0],
                "imgs": imgs,
                "caption": " ".join(c for c in cap_lines if c),
                "html": _md("\n".join(rest).strip()),
            }
        )
    return slides


def _to_webp(src: Path, dest: Path, quality: int = 85) -> None:
    """Store figures as WebP: ~7-14x smaller than arXiv PNGs, no visible loss."""
    if dest.exists() and dest.stat().st_mtime >= src.stat().st_mtime:
        return
    Image.open(src).convert("RGB").save(dest, "WEBP", quality=quality)


def _render_deck(slides: list[dict], lang: str) -> str:
    title = "方 法 图 解" if lang == "zh" else "M E T H O D"
    n = len(slides)
    cta_b = "进入方法图解" if lang == "zh" else "Enter the figure walkthrough"
    cta_s = (
        f"{n} 张论文原图 · 全屏放映 · ← → 翻页 · Esc 退出"
        if lang == "zh"
        else f"{n} figures from the paper · fullscreen · flip with ← → · Esc to exit"
    )
    close_label = "✕ 退出" if lang == "zh" else "✕ Exit"
    hint = (
        "← → 翻页 · ↑ ↓ 滚动讲解 · Esc 退出"
        if lang == "zh"
        else "← → flip · ↑ ↓ scroll notes · Esc exit"
    )
    slide_parts = []
    for s in slides:
        imgs = s.get("imgs") or [s["img"]]
        stage_class = "stage multi" if len(imgs) > 1 else "stage"
        stage_imgs = "".join(f'<img src="{img}" alt="">' for img in imgs)
        slide_parts.append(
            f'<div class="slide"><div class="{stage_class}">{stage_imgs}</div>'
            f'<div class="note"><p class="cap">{s["caption"]}</p>{s["html"]}</div></div>'
        )
    slide_html = "".join(slide_parts)
    dots = "".join('<button class="dot"></button>' for _ in slides)
    launcher = (
        f'<button class="launcher" id="launcher">'
        f'<img class="thumb" src="{slides[0]["img"]}" alt="">'
        f'<span class="cta"><span class="play"><svg width="14" height="16" viewBox="0 0 14 16"><path d="M1 1.5v13l12-6.5z" fill="currentColor"/></svg></span>'
        f"<span><b>{cta_b}</b><span>{cta_s}</span></span></span>"
        f"</button>"
    )
    deck = (
        f'<section class="deck" id="deck">'
        f'<div class="deck-top"><span class="t">{title}</span>'
        f'<span class="count"><b>1</b> / {n}</span>'
        f'<button class="close">{close_label}</button></div>'
        f'<div class="slides">{slide_html}</div>'
        f'<button class="nav prev">‹</button><button class="nav next">›</button>'
        f'<div class="deck-bottom">{dots}</div>'
        f'<div class="deck-hint">{hint}</div>'
        f"</section>"
    )
    return launcher, deck


def render_paper(date: str, paper: dict, lang: str) -> str | None:
    paper_dir = DATA_DIR / date / paper["arxiv_id"]
    md_file = paper_dir / f"deep_dive.{lang}.md"
    if not md_file.exists():
        return None
    raw = md_file.read_text()

    heading = METHOD_HEADING[lang]
    if f"\n{heading}\n" in raw:
        article_md, deck_md = raw.split(f"\n{heading}\n", 1)
        slides = _parse_slides(deck_md)
    else:
        article_md, slides = raw, []
    annotations = load_annotations(paper_dir, lang)
    article_html = apply_annotations(_md(article_md), annotations)
    for slide in slides:
        slide["html"] = apply_annotations(slide["html"], annotations)

    other = "en" if lang == "zh" else "zh"
    other_label = "English" if lang == "zh" else "中文"
    switch = f'<div class="lang-switch"><a href="{other}.html">{other_label}</a></div>'
    back = "← 今日潮汐" if lang == "zh" else "← Today's tide"
    bits = []
    pub = (paper.get("published_at") or "")[:10]
    if pub:
        bits.append(("发表于" if lang == "zh" else "Published") + f" {pub}")
    if paper.get("organization"):
        bits.append(paper["organization"])
    authors = [a for a in (paper.get("authors") or []) if a]
    if authors:
        shown = ", ".join(authors[:3])
        if len(authors) > 3:
            shown += " 等" if lang == "zh" else " et al."
        bits.append(shown)
    meta_line = f'<p class="meta paper-meta">{" · ".join(bits)}</p>' if bits else ""
    article = (
        f'<main class="article">{switch}'
        f'<p class="meta"><a href="../../index.html">{back}</a></p>'
        f"{meta_line}"
        f"<article>{article_html}</article></main>"
    )
    if slides:
        launcher, deck = _render_deck(slides, lang)
        heading_html = "<h2>方法图解</h2>" if lang == "zh" else "<h2>Method, Figure by Figure</h2>"
        article = article.replace("</article></main>", f"{heading_html}{launcher}</article></main>")
    else:
        deck = ""
    return PAGE.format(
        lang=lang,
        title=paper["title"],
        css=CSS,
        js=DECK_JS if slides else "",
        math=MATH_JAX,
        home="../../index.html",
        tagline=TAGLINE_ZH if lang == "zh" else TAGLINE_EN,
        body=article + deck,
    )


def render_index(days: list[tuple[str, list[dict]]]) -> str:
    sections = []
    for date, papers in days:
        cards = []
        for p in papers:
            has_dive = (DATA_DIR / date / p["arxiv_id"] / "deep_dive.zh.md").exists()
            link = f'{date}/{p["arxiv_id"]}/zh.html' if has_dive else p["arxiv_url"]
            note = "" if has_dive else '<span class="badge">深潜未生成 · 链接原文</span>'
            org = (
                f'<span class="badge">{p["organization"]}</span>'
                if p.get("organization")
                else ""
            )
            vote = (
                '<span class="badge">✦ 编辑精选</span>'
                if p.get("source") == "manual"
                else f'<span class="badge">▲ {p["upvotes"]}</span>'
            )
            pub = (p.get("published_at") or "")[:10]
            if pub:
                vote += f'<span class="badge">📅 {pub}</span>'
            cards.append(
                f'<div class="card"><h3><a href="{link}">{p["title"]}</a></h3>'
                f'{vote}{org}{note}'
                f'<p class="abs">{p["abstract"]}</p></div>'
            )
        sections.append(
            f"<h2 class='day'>潮汐 · {date}</h2>" + "".join(cards)
        )
    body = '<main class="article">' + "".join(sections) + "</main>"
    return PAGE.format(
        lang="zh", title="Tide 潮汐", css=CSS, js="", home="index.html",
        math=MATH_JAX, tagline=TAGLINE_ZH, body=body,
    )


def publish(dates: list[str] | None = None) -> Path:
    if not dates:
        dates = sorted(
            (d.name for d in DATA_DIR.iterdir()
             if d.is_dir() and (d / "selected.json").exists()),
            reverse=True,
        )
    days = []
    for date in dates:
        day_dir = DATA_DIR / date
        papers = json.loads((day_dir / "selected.json").read_text())
        days.append((date, papers))
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
            for img in paper_dir.glob("fig*_*.webp"):
                shutil.copy(img, out_paper / img.name)
            for img in paper_dir.glob("fig*_*.png"):
                _to_webp(img, out_paper / (img.stem + ".webp"))

    (SITE_DIR / "index.html").write_text(render_index(days))
    print(f"Site written to {SITE_DIR} ({len(days)} day(s))")
    return SITE_DIR


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", help="publish one date only (default: all in data/)")
    args = ap.parse_args()
    publish([args.date] if args.date else None)


if __name__ == "__main__":
    main()
