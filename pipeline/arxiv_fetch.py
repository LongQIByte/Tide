"""Fetch arXiv full text (official HTML) and extract figures with captions."""

from __future__ import annotations

import re
import time
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin

import requests

USER_AGENT = "Tide/0.1 (https://github.com/JavanTang/Tide)"
ARXIV_DELAY_SECONDS = 3  # arXiv etiquette: >=3s between requests
_last_request_at = 0.0


def _polite_get(url: str) -> requests.Response:
    global _last_request_at
    wait = ARXIV_DELAY_SECONDS - (time.monotonic() - _last_request_at)
    if wait > 0:
        time.sleep(wait)
    resp = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=60)
    _last_request_at = time.monotonic()
    return resp


def fetch_html(arxiv_id: str) -> tuple[str, str] | None:
    """Return (html, base_url) for the paper, trying arxiv.org then ar5iv."""
    for url in (
        f"https://arxiv.org/html/{arxiv_id}v1",
        f"https://arxiv.org/html/{arxiv_id}",
        f"https://ar5iv.labs.arxiv.org/html/{arxiv_id}",
    ):
        resp = _polite_get(url)
        if resp.status_code == 200 and "<html" in resp.text[:1000].lower():
            return resp.text, resp.url
    return None


class _FigureParser(HTMLParser):
    """Collect <figure> blocks: image URLs + caption text."""

    def __init__(self, base_url: str):
        super().__init__()
        self.base_url = base_url
        self.figures: list[dict] = []
        self._depth = 0  # nesting level inside <figure>
        self._current: dict | None = None
        self._in_caption = False
        self._caption_parts: list[str] = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "figure":
            self._depth += 1
            if self._depth == 1:
                self._current = {"images": [], "caption": ""}
        elif self._depth > 0 and self._current is not None:
            if tag == "img" and attrs.get("src"):
                # arXiv HTML uses two src conventions: "<id>vN/x1.png" (joins
                # against the page dir) and bare "x1.png" (joins against the
                # page URL as a dir). Record both candidates; download tries
                # them in order.
                s = attrs["src"]
                cands = [urljoin(self.base_url.rstrip("/") + "/", s),
                         urljoin(self.base_url, s)]
                self._current["images"].append(
                    cands[0] if cands[0] == cands[1] else cands
                )
            elif tag == "figcaption":
                self._in_caption = True

    def handle_endtag(self, tag):
        if tag == "figcaption":
            self._in_caption = False
        elif tag == "figure" and self._depth > 0:
            self._depth -= 1
            if self._depth == 0 and self._current is not None:
                self._current["caption"] = re.sub(
                    r"\s+", " ", " ".join(self._caption_parts)
                ).strip()
                if self._current["images"]:
                    self.figures.append(self._current)
                self._current = None
                self._caption_parts = []

    def handle_data(self, data):
        if self._in_caption:
            self._caption_parts.append(data)


def extract_figures(html: str, base_url: str) -> list[dict]:
    parser = _FigureParser(base_url)
    parser.feed(html)
    return parser.figures


def download_figures(figures: list[dict], dest_dir: Path) -> list[dict]:
    """Download figure images next to the paper; returns figures with local paths."""
    dest_dir.mkdir(parents=True, exist_ok=True)
    out = []
    for i, fig in enumerate(figures, 1):
        local_paths = []
        for j, url in enumerate(fig["images"], 1):
            candidates = url if isinstance(url, list) else [url]
            suffix = Path(candidates[0].split("?")[0]).suffix or ".png"
            path = dest_dir / f"fig{i}_{j}{suffix}"
            saved = None
            for cand in candidates:
                try:
                    resp = _polite_get(cand)
                    resp.raise_for_status()
                    path.write_bytes(resp.content)
                    saved = str(path)
                    break
                except requests.RequestException:
                    continue
            local_paths.append(saved)
        out.append({**fig, "local_paths": local_paths})
    return out
