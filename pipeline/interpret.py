"""Deep-dive interpretation of one ingested paper (README's four-part shape).

Usage:
    python -m pipeline.interpret --date YYYY-MM-DD --id ARXIV_ID [--max-figures N]

Reads  data/<date>/<id>/paper.html + figures + selected.json entry.
Writes data/<date>/<id>/deep_dive.zh.md and deep_dive.en.md.
"""

from __future__ import annotations

import argparse
import json
import re
from html.parser import HTMLParser
from pathlib import Path

from . import llm

try:
    from PIL import Image
except ImportError:  # pillow only needed for --prune webp conversion
    Image = None

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
ZH_EN_SPLIT = "===EN==="  # legacy marker, still handled in _split_bilingual


# ---------- HTML text extraction ----------


class _SectionParser(HTMLParser):
    """Split arXiv LaTeXML HTML into (section_title, text) pairs."""

    def __init__(self):
        super().__init__()
        self.sections: list[tuple[str, str]] = []
        self._title_parts: list[str] = []
        self._text_parts: list[str] = []
        self._in_title = False
        self._in_section = False
        self._skip_depth = 0  # inside <figure>/<math> etc.

    def handle_starttag(self, tag, attrs):
        cls = dict(attrs).get("class", "")
        if tag == "section" and "ltx_section" in cls:
            self._flush()
            self._in_section = True
        elif self._in_section:
            if tag in ("figure", "math", "svg", "table"):
                self._skip_depth += 1
            elif tag in ("h2", "h3") and "ltx_title" in cls and not self._skip_depth:
                self._in_title = tag == "h2"

    def handle_endtag(self, tag):
        if tag in ("figure", "math", "svg", "table") and self._skip_depth:
            self._skip_depth -= 1
        elif tag == "h2":
            self._in_title = False

    def handle_data(self, data):
        if not self._in_section or self._skip_depth:
            return
        if self._in_title:
            self._title_parts.append(data)
        else:
            self._text_parts.append(data)

    def _flush(self):
        if self._title_parts or self._text_parts:
            title = re.sub(r"\s+", " ", "".join(self._title_parts)).strip()
            text = re.sub(r"\s+", " ", "".join(self._text_parts)).strip()
            self.sections.append((title, text))
        self._title_parts, self._text_parts = [], []

    def close(self):
        super().close()
        self._flush()


def extract_sections(html: str) -> list[tuple[str, str]]:
    p = _SectionParser()
    p.feed(html)
    p.close()
    return p.sections


def find_introduction(sections: list[tuple[str, str]]) -> str:
    for title, text in sections:
        if "introduction" in title.lower():
            return text
    return sections[0][1] if sections else ""


# ---------- LLM stages ----------


def translate_abstract(abstract: str) -> str:
    return llm.chat(
        "把下面这段论文摘要翻译成中文。只翻译，不总结、不增删内容，保留术语的英文原词"
        "（可在括号内附中文）。直接输出译文。\n\n" + abstract
    )


def analyze_introduction(title: str, abstract: str, intro: str) -> tuple[str, str]:
    """Background analysis in zh and en."""
    out = llm.chat(
        f"你在为 AI 资讯网站写论文深潜的「背景剖析」一节。论文标题：{title}\n\n"
        f"摘要：{abstract}\n\nIntroduction 原文：\n{intro[:12000]}\n\n"
        "基于 Introduction（不要编造原文没有的内容），用连贯的叙述讲清楚四件事：\n"
        "1. 技术背景：这类技术用在什么地方、要解决什么真实需求；\n"
        "2. 之前的问题：先前方法卡在哪里、为什么不够好；\n"
        "3. 本文的解法：这篇论文用什么思路解决这些问题；\n"
        "4. 切入角度：它与前人工作的关键差异。\n"
        "篇幅适中（400-700 字），面向懂技术但不熟悉这个子领域的读者，不堆术语。\n"
        f"把中文版本包在 <zh> 和 </zh> 标签之间，英文版本包在 <en> 和 </en> 标签之间输出。"
    )
    return _ensure_languages(*_split_bilingual(out))


def pick_key_figures(figures: list[dict], max_n: int) -> list[int]:
    """Ask the text model which figures best explain the method/framework."""
    numbered = "\n".join(
        f"[{i}] {f.get('caption') or '(no caption)'}" for i, f in enumerate(figures)
    )
    out = llm.chat(
        "下面是一篇论文所有插图的 caption 列表。选出最能讲清「方法/框架/流程如何工作」"
        f"的图（优先总体框架图、方法流程图；实验曲线和消融图靠后），最多选 {max_n} 张，"
        "按讲解顺序排列。只输出 JSON 数组，如 [0,2,5]。\n\n" + numbered
    )
    m = re.search(r"\[[\d,\s]*\]", out)
    if not m:
        return list(range(min(max_n, len(figures))))
    idx = [i for i in json.loads(m.group(0)) if 0 <= i < len(figures)]
    return idx[:max_n] or list(range(min(max_n, len(figures))))


def explain_figure(paper: dict, fig: dict, image_path: str) -> tuple[str, str]:
    """Poster-style detailed walkthrough of one figure, zh and en."""
    out = llm.chat_vision(
        f"这是论文《{paper['title']}》中的一张图。论文摘要：{paper['abstract'][:1500]}\n"
        f"图的原始 caption：{fig.get('caption') or '(无)'}\n\n"
        "请像讲解学术海报一样，把这张图讲得非常清楚、比原文 caption 详细得多：\n"
        "- 图中每个组件/板块/箭头代表什么，数据或信息按什么顺序流动；\n"
        "- 这张图揭示了方法具体是怎么做的（读者只看你的讲解就能明白方法如何运作）；\n"
        "- 如果是结果图，说清坐标、对比对象和结论。\n"
        "不要复述公式推导，重理解。用 markdown 段落（可用少量列表），不要加标题。\n"
        "直接给出定论式讲解：图中看不清或不确定的地方按 caption 处理或跳过，"
        "绝不要输出犹豫、自问自答或自我纠正的过程。\n"
        "把中文讲解包在 <zh> 和 </zh> 标签之间，英文讲解包在 <en> 和 </en> 标签之间输出。",
        image_path,
    )
    return _ensure_languages(*_split_bilingual(out))


def _split_bilingual(text: str) -> tuple[str, str]:
    # Tolerant tag split: models sometimes drop a closing tag, so split on
    # the <en> opener alone; _clean strips any leftover tag tokens.
    if "<en>" in text:
        zh, en = text.split("<en>", 1)
        return _clean(zh), _clean(en)
    # Fallbacks: legacy "===EN===" marker (possibly mangled), then a bare
    # separator line of ===/--- that models sometimes degrade it into.
    for pattern in (r"={2,}\s*EN\s*={2,}", r"^\s*[=-]{3,}\s*$"):
        parts = re.split(pattern, text, maxsplit=1, flags=re.MULTILINE)
        if len(parts) == 2:
            return _clean(parts[0]), _clean(parts[1])
    return _clean(text), _clean(text)


def _cjk_ratio(text: str) -> float:
    if not text:
        return 0.0
    cjk = sum(1 for ch in text if "一" <= ch <= "鿿")
    return cjk / len(text)


def _ensure_languages(zh: str, en: str) -> tuple[str, str]:
    """The model sometimes skips one language; translate to fill the gap."""
    if _cjk_ratio(en) > 0.15:
        en = llm.chat(
            "Translate the following into natural English. Keep all markdown "
            "structure. Output the translation only.\n\n" + en
        )
    if _cjk_ratio(zh) < 0.05 and zh.strip():
        zh = llm.chat(
            "把下面的内容翻译成中文，保留 markdown 结构，术语可保留英文。"
            "只输出译文。\n\n" + zh
        )
    return zh, en


def _clean(text: str) -> str:
    text = re.sub(r"</?(zh|en)>", "", text)
    # Drop leaked language labels like "**中文版本：**" / "English version:".
    text = re.sub(
        r"^\s*\**[（(]?(中文|英文|English|Chinese)\s*(版本|翻译|讲解|version)?\s*[：:）)]\**\s*$",
        "",
        text,
        flags=re.MULTILINE,
    )
    return text.strip()


# ---------- assembly ----------


def deep_dive(date: str, arxiv_id: str, max_figures: int = 5, prune: bool = False) -> None:
    day_dir = DATA_DIR / date
    paper_dir = day_dir / arxiv_id
    selected = json.loads((day_dir / "selected.json").read_text())
    paper = next(p for p in selected if p["arxiv_id"] == arxiv_id)
    html = (paper_dir / "paper.html").read_text()

    print(f"[1/4] Extracting introduction ...")
    intro = find_introduction(extract_sections(html))
    print(f"      intro length: {len(intro)} chars")

    print(f"[2/4] Translating abstract ...")
    abstract_zh = translate_abstract(paper["abstract"])

    print(f"[3/4] Analyzing introduction ...")
    background_zh, background_en = analyze_introduction(
        paper["title"], paper["abstract"], intro
    )

    figures = [f for f in paper.get("figures", []) if any(f.get("local_paths", []))]
    key_idx = pick_key_figures(figures, max_figures)
    print(f"[4/4] Explaining {len(key_idx)} key figures (of {len(figures)}): {key_idx}")
    fig_sections_zh, fig_sections_en = [], []
    kept_images = []
    for i in key_idx:
        fig = figures[i]
        img = next(p for p in fig["local_paths"] if p)
        zh, en = explain_figure(paper, fig, img)
        rel = _webp_name(Path(img))
        kept_images.append(paper_dir / rel)
        cap = fig.get("caption", "")
        fig_sections_zh.append(f"![{cap[:80]}]({rel})\n\n> {cap}\n\n{zh}")
        fig_sections_en.append(f"![{cap[:80]}]({rel})\n\n> {cap}\n\n{en}")
        print(f"      figure [{i}] done")

    zh_md = _render_zh(paper, abstract_zh, background_zh, fig_sections_zh)
    en_md = _render_en(paper, background_en, fig_sections_en)
    (paper_dir / "deep_dive.zh.md").write_text(zh_md)
    (paper_dir / "deep_dive.en.md").write_text(en_md)
    _convert_figures(figures, key_idx)
    if prune:
        _prune(paper_dir, kept_images)
    print(f"Done: {paper_dir}/deep_dive.zh.md, deep_dive.en.md")


def _webp_name(img: Path) -> str:
    return img.stem + ".webp"


def _convert_figures(figures: list[dict], key_idx: list[int]) -> None:
    """Convert the chosen figures to WebP next to the originals (~8x smaller)."""
    if Image is None:
        raise RuntimeError("pillow required: pip install pillow")
    for i in key_idx:
        src_img = Path(next(p for p in figures[i]["local_paths"] if p))
        dest = src_img.with_suffix(".webp")
        if not dest.exists():
            Image.open(src_img).convert("RGB").save(dest, "WEBP", quality=85)


def _prune(paper_dir: Path, kept_images: list[Path]) -> None:
    """Keep only what gets committed: deep_dive md + chosen webp figures."""
    keep = {p.name for p in kept_images} | {"deep_dive.zh.md", "deep_dive.en.md"}
    for f in paper_dir.iterdir():
        if f.name not in keep:
            f.unlink()


def _render_zh(paper, abstract_zh, background, fig_sections) -> str:
    figs = "\n\n---\n\n".join(fig_sections) or "（本文无可讲解的插图）"
    links = f"[arXiv]({paper['arxiv_url']})"
    if paper.get("hf_url"):
        links += f" · [HuggingFace]({paper['hf_url']}) · ▲{paper['upvotes']}"
    return f"""# {paper['title']}

{links}

## 摘要（原文）

> {paper['abstract']}

## 摘要（中译）

{abstract_zh}

## 背景剖析

{background}

## 方法图解

{figs}
"""


def _render_en(paper, background, fig_sections) -> str:
    figs = "\n\n---\n\n".join(fig_sections) or "(No figures to walk through.)"
    links = f"[arXiv]({paper['arxiv_url']})"
    if paper.get("hf_url"):
        links += f" · [HuggingFace]({paper['hf_url']}) · ▲{paper['upvotes']}"
    return f"""# {paper['title']}

{links}

## Abstract (verbatim)

> {paper['abstract']}

## Background

{background}

## Method, Figure by Figure

{figs}
"""


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", required=True)
    ap.add_argument("--id", required=True, help="arXiv id")
    ap.add_argument("--max-figures", type=int, default=5)
    ap.add_argument("--prune", action="store_true",
                    help="delete paper.html and unused figures afterwards")
    args = ap.parse_args()
    deep_dive(args.date, args.id, args.max_figures, args.prune)


if __name__ == "__main__":
    main()
