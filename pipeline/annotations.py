from __future__ import annotations

import html as html_lib
import json
import re
from html.parser import HTMLParser
from pathlib import Path


def load_annotations(paper_dir: Path, lang: str) -> list[dict]:
    path = paper_dir / f"annotations.{lang}.json"
    if not path.exists():
        return []

    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, list):
        return []

    annotations = []
    for item in raw:
        if not isinstance(item, dict):
            continue
        term = str(item.get("term", "")).strip()
        definition = str(item.get("definition", "")).strip()
        if term and definition:
            annotations.append({"term": term, "definition": definition})
    return annotations


def apply_annotations(html: str, annotations: list[dict]) -> str:
    terms = _normalize_annotations(annotations)
    if not terms:
        return html
    parser = _AnnotationParser(terms)
    parser.feed(html)
    parser.close()
    return parser.rendered


def _normalize_annotations(annotations: list[dict]) -> list[dict]:
    seen = set()
    normalized = []
    for item in annotations:
        term = str(item.get("term", "")).strip()
        definition = str(item.get("definition", "")).strip()
        if not term or not definition or term in seen:
            continue
        seen.add(term)
        normalized.append({"term": term, "definition": definition})
    return sorted(normalized, key=lambda item: len(item["term"]), reverse=True)


class _AnnotationParser(HTMLParser):
    _SKIP_TAGS = {"a", "button", "code", "pre", "script", "style", "textarea", "svg"}

    def __init__(self, annotations: list[dict]):
        super().__init__(convert_charrefs=False)
        self._out: list[str] = []
        self._skip_stack: list[str] = []
        self._definitions = {item["term"]: item["definition"] for item in annotations}
        pattern = "|".join(re.escape(item["term"]) for item in annotations)
        self._term_re = re.compile(pattern)

    @property
    def rendered(self) -> str:
        return "".join(self._out)

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self._out.append(self.get_starttag_text())
        if self._should_skip_tag(tag, attrs):
            self._skip_stack.append(tag.lower())

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self._out.append(self.get_starttag_text())

    def handle_endtag(self, tag: str) -> None:
        self._out.append(f"</{tag}>")
        lower = tag.lower()
        if self._skip_stack and self._skip_stack[-1] == lower:
            self._skip_stack.pop()

    def handle_data(self, data: str) -> None:
        if self._skip_stack:
            self._out.append(data)
            return
        self._out.append(self._term_re.sub(self._render_term, data))

    def handle_entityref(self, name: str) -> None:
        self._out.append(f"&{name};")

    def handle_charref(self, name: str) -> None:
        self._out.append(f"&#{name};")

    def handle_comment(self, data: str) -> None:
        self._out.append(f"<!--{data}-->")

    def handle_decl(self, decl: str) -> None:
        self._out.append(f"<!{decl}>")

    def _should_skip_tag(self, tag: str, attrs: list[tuple[str, str | None]]) -> bool:
        lower = tag.lower()
        if lower in self._SKIP_TAGS:
            return True
        if lower != "span":
            return False
        classes = " ".join(value or "" for name, value in attrs if name == "class")
        return "math" in classes.split()

    def _render_term(self, match: re.Match[str]) -> str:
        term = match.group(0)
        definition = self._definitions[term]
        safe_term = html_lib.escape(term)
        safe_definition = html_lib.escape(definition)
        aria = html_lib.escape(f"{term}: {definition}", quote=True)
        return (
            f'<span class="note-term" tabindex="0" aria-label="{aria}">'
            f'<span class="note-label">{safe_term}</span>'
            f'<span class="note-popover">{safe_definition}</span>'
            "</span>"
        )
