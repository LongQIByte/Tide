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

import markdown
from PIL import Image

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
SITE_DIR = Path(__file__).resolve().parent.parent / "site"

METHOD_HEADING = {"zh": "## 方法图解", "en": "## Method, Figure by Figure"}

CSS = """
:root {
  --ink: #1c2b36; --ink-soft: #4a5d6b; --sea: #0e6e8c; --sea-deep: #0a4f66;
  --foam: #f6f9fa; --sand: #fffdf8; --line: #dfe8ec;
  --night: #0b1e28; --night-2: #10293a; --moon: #dcebf2; --moon-soft: #9fb9c6;
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
header.site .wrap, main.article { max-width: 780px; margin: 0 auto; }
header.site h1 { margin: 0; font-size: 1.9rem; letter-spacing: .04em; }
header.site h1 a { color: #fff; text-decoration: none; }
header.site p { margin: .4rem 0 0; opacity: .82; font-size: .95rem; }
main.article { padding: 2.5rem 1.5rem 3rem; }
h1, h2, h3 { line-height: 1.4; color: var(--sea-deep); }
article h1 { font-size: 1.55rem; }
main.article h2 {
  font-size: 1.25rem; margin-top: 2.6rem; padding-left: .7rem;
  border-left: 4px solid var(--sea);
}
a { color: var(--sea); }
blockquote {
  margin: 1.2rem 0; padding: .9rem 1.2rem; background: var(--foam);
  border-left: 4px solid var(--line); color: var(--ink-soft);
  font-size: .95rem;
}
img { max-width: 100%; }
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

/* ---------- deck launcher (inline, in the article flow) ---------- */
.launcher {
  position: relative; display: block; width: 100%; overflow: hidden;
  border: none; border-radius: 14px; cursor: pointer; padding: 0;
  margin: 1.4rem 0 2.2rem; text-align: left; color: var(--moon);
  background: linear-gradient(180deg, var(--night-2), var(--night));
  box-shadow: 0 10px 34px rgba(10,79,102,.25);
  transition: transform .25s ease, box-shadow .25s ease;
  font: inherit;
}
.launcher:hover { transform: translateY(-2px);
  box-shadow: 0 16px 44px rgba(10,79,102,.35); }
.launcher .thumb {
  display: block; width: 100%; height: 240px; object-fit: cover;
  object-position: top; opacity: .9;
  -webkit-mask-image: linear-gradient(180deg, #000 30%, transparent 100%);
          mask-image: linear-gradient(180deg, #000 30%, transparent 100%);
  background: #fff; border: none; border-radius: 0; padding: 10px;
}
.launcher .cta {
  display: flex; align-items: center; gap: .9rem;
  padding: 1.05rem 1.4rem 1.15rem;
}
.launcher .play {
  flex: 0 0 auto; width: 2.6rem; height: 2.6rem; border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  background: var(--moon); color: var(--night); padding-left: .25rem;
}
.launcher .cta b { font-size: 1.02rem; letter-spacing: .02em; }
.launcher .cta span { display: block; color: var(--moon-soft);
  font-size: .84rem; margin-top: .15rem; }
.launcher .cta span.play { display: flex; margin-top: 0; color: var(--night); }

/* ---------- figure deck (fullscreen slideshow overlay) ---------- */
.deck {
  position: fixed; inset: 0; z-index: 50; display: none;
  background:
    radial-gradient(1200px 500px at 50% -10%, #17435a 0%, transparent 60%),
    linear-gradient(180deg, var(--night-2), var(--night) 55%);
  color: var(--moon); flex-direction: column;
}
.deck.open { display: flex; }
.deck-top {
  display: flex; align-items: center; gap: 1rem;
  padding: 1rem 1.6rem; font-size: .9rem; color: var(--moon-soft);
}
.deck-top .t { letter-spacing: .12em; }
.deck-top .count { margin-left: auto; font-variant-numeric: tabular-nums; }
.deck-top button {
  background: none; border: 1px solid rgba(220,235,242,.28); color: var(--moon-soft);
  border-radius: 99px; padding: .2rem .9rem; font: inherit; font-size: .82rem;
  cursor: pointer;
}
.deck-top button:hover { color: var(--moon); border-color: var(--moon); }
.slides { flex: 1; min-height: 0; position: relative; }
.slide {
  position: absolute; inset: 0; display: flex; flex-direction: column;
  padding: 0 4.5rem; opacity: 0; visibility: hidden;
  transform: translateX(24px); transition: opacity .35s ease, transform .35s ease,
             visibility .35s;
}
.slide.active { opacity: 1; visibility: visible; transform: none; }
.slide .stage {
  flex: 1; min-height: 0; display: flex; align-items: center;
  justify-content: center; padding: .2rem 0 1rem;
}
.slide .stage img {
  max-width: min(100%, 1100px); max-height: 100%;
  background: #fff; border-radius: 10px; padding: 14px;
  box-shadow: 0 18px 60px rgba(0,0,0,.5);
}
.slide .note {
  flex: 0 0 auto; max-height: 38svh; overflow-y: auto;
  max-width: 860px; margin: 0 auto; width: 100%;
  padding: 0 .2rem 1.6rem; font-size: .98rem; line-height: 1.85;
  scrollbar-width: thin; scrollbar-color: rgba(220,235,242,.3) transparent;
}
.slide .note .cap {
  color: var(--moon-soft); font-size: .84rem; font-style: italic;
  border-left: 3px solid rgba(220,235,242,.25); padding-left: .8rem;
  margin: 0 0 .9rem;
}
.slide .note h1, .slide .note h2, .slide .note h3, .slide .note h4 {
  color: #cfe6f0; font-size: 1.02rem; margin: 1.3em 0 .4em;
}
.slide .note strong { color: #eef7fb; }
.slide .note code { background: rgba(220,235,242,.12); color: var(--moon); }
.slide .note a { color: #8fd0e8; }
.slide .note blockquote { background: rgba(220,235,242,.07);
  border-left-color: rgba(220,235,242,.25); color: var(--moon-soft); }
.deck .nav {
  position: absolute; top: 50%; transform: translateY(-50%);
  width: 3rem; height: 3rem; border-radius: 50%;
  border: 1px solid rgba(220,235,242,.25); background: rgba(11,30,40,.55);
  color: var(--moon); font-size: 1.3rem; line-height: 1; cursor: pointer;
  transition: all .2s; backdrop-filter: blur(4px);
}
.deck .nav:hover { border-color: var(--moon); background: rgba(23,67,90,.75); }
.deck .nav[disabled] { opacity: .25; cursor: default; }
.deck .prev { left: 1rem; }
.deck .next { right: 1rem; }
.deck-bottom {
  display: flex; align-items: center; justify-content: center; gap: .55rem;
  padding: .8rem 0 1.1rem;
}
.dot { width: .5rem; height: .5rem; border-radius: 50%;
  background: rgba(220,235,242,.25); cursor: pointer; transition: all .25s;
  border: none; padding: 0; }
.dot.active { background: var(--moon); transform: scale(1.25); }
.deck-hint { position: absolute; bottom: .9rem; right: 1.4rem;
  font-size: .75rem; color: rgba(220,235,242,.4); }
@media (max-width: 720px) {
  .slide { padding: 0 1rem; }
  .deck .nav { display: none; }
  .slide .note { max-height: 44svh; }
}
"""

DECK_JS = """
(function () {
  const deck = document.getElementById('deck');
  const launcher = document.getElementById('launcher');
  if (!deck || !launcher) return;
  const slides = deck.querySelectorAll('.slide');
  const dots = deck.querySelectorAll('.dot');
  const cur = deck.querySelector('.count b');
  const prev = deck.querySelector('.prev');
  const next = deck.querySelector('.next');
  let i = 0;
  function go(n) {
    i = Math.max(0, Math.min(slides.length - 1, n));
    slides.forEach((s, k) => s.classList.toggle('active', k === i));
    dots.forEach((d, k) => d.classList.toggle('active', k === i));
    cur.textContent = i + 1;
    prev.disabled = i === 0;
    next.disabled = i === slides.length - 1;
    slides[i].querySelector('.note').scrollTop = 0;
  }
  prev.onclick = () => go(i - 1);
  next.onclick = () => go(i + 1);
  dots.forEach((d, k) => d.onclick = () => go(k));
  function open() {
    deck.classList.add('open');
    document.body.style.overflow = 'hidden';
    if (deck.requestFullscreen) deck.requestFullscreen().catch(() => {});
    go(i);
  }
  function close() {
    deck.classList.remove('open');
    document.body.style.overflow = '';
    if (document.fullscreenElement) document.exitFullscreen();
  }
  launcher.onclick = open;
  deck.querySelector('.close').onclick = close;
  document.addEventListener('fullscreenchange', () => {
    if (!document.fullscreenElement && deck.classList.contains('open')) {
      deck.classList.remove('open');
      document.body.style.overflow = '';
    }
  });
  document.addEventListener('keydown', (e) => {
    if (!deck.classList.contains('open')) return;
    if (e.key === 'ArrowRight' || e.key === ' ') { e.preventDefault(); go(i + 1); }
    else if (e.key === 'ArrowLeft') { e.preventDefault(); go(i - 1); }
    else if (e.key === 'ArrowDown' || e.key === 'ArrowUp') {
      e.preventDefault();
      const note = slides[i].querySelector('.note');
      note.scrollBy({ top: e.key === 'ArrowDown' ? 120 : -120, behavior: 'smooth' });
    }
    else if (e.key === 'Escape') { close(); }
  });
})();
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
{body}
<footer>Tide · 理解是无法外包的 / Understanding cannot be outsourced</footer>
<script>{js}</script>
</body>
</html>
"""

TAGLINE_ZH = "资讯如潮汐。我们挑出值得研究的浪，并认真讲解它。"
TAGLINE_EN = "Information moves like the tide. We pick the waves worth studying."


def _md(text: str) -> str:
    return markdown.markdown(text, extensions=["tables", "fenced_code"])


def _parse_slides(deck_md: str) -> list[dict]:
    """Split the method section into slides: image + caption + explanation."""
    slides = []
    for block in re.split(r"^---$", deck_md, flags=re.MULTILINE):
        block = block.strip()
        if not block:
            continue
        img_m = re.search(r"!\[[^\]]*\]\(([^)]+)\)", block)
        if not img_m:
            continue
        block = block.replace(img_m.group(0), "", 1)
        cap_lines, rest = [], []
        for line in block.splitlines():
            if line.startswith(">"):
                cap_lines.append(line.lstrip("> ").strip())
            else:
                rest.append(line)
        slides.append(
            {
                "img": re.sub(r"\.(png|jpe?g)$", ".webp", img_m.group(1)),
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
    slide_html = "".join(
        f'<div class="slide"><div class="stage"><img src="{s["img"]}" alt=""></div>'
        f'<div class="note"><p class="cap">{s["caption"]}</p>{s["html"]}</div></div>'
        for s in slides
    )
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

    other = "en" if lang == "zh" else "zh"
    other_label = "English" if lang == "zh" else "中文"
    switch = f'<div class="lang-switch"><a href="{other}.html">{other_label}</a></div>'
    back = "← 今日潮汐" if lang == "zh" else "← Today's tide"
    article = (
        f'<main class="article">{switch}'
        f'<p class="meta"><a href="../../index.html">{back}</a></p>'
        f"<article>{_md(article_md)}</article></main>"
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
        home="../../index.html",
        tagline=TAGLINE_ZH if lang == "zh" else TAGLINE_EN,
        body=article + deck,
    )


def render_index(date: str, papers: list[dict]) -> str:
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
        cards.append(
            f'<div class="card"><h3><a href="{link}">{p["title"]}</a></h3>'
            f'<span class="badge">▲ {p["upvotes"]}</span>{org}{note}'
            f'<p class="abs">{p["abstract"]}</p></div>'
        )
    body = (
        "<main class=\"article\">"
        f"<h2 style='margin-top:0;border:none;padding:0'>今日潮汐 · {date}</h2>"
        + "".join(cards)
        + "</main>"
    )
    return PAGE.format(
        lang="zh", title=f"今日潮汐 {date}", css=CSS, js="", home="index.html",
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
            _to_webp(img, out_paper / (img.stem + ".webp"))

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
