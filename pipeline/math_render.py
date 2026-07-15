from __future__ import annotations

import html
import re


_FENCED_CODE_RE = re.compile(r"(^```.*?^```|^~~~.*?^~~~)", re.DOTALL | re.MULTILINE)
_INLINE_CODE_RE = re.compile(r"`+[^`\n]*`+")
_DISPLAY_MATH_RE = re.compile(r"\\\[(.+?)\\\]", re.DOTALL)
_INLINE_MATH_RE = re.compile(r"\\\((.+?)\\\)", re.DOTALL)


def protect_math(text: str) -> str:
    """Keep LaTeX delimiters intact before Python-Markdown consumes escapes."""
    parts: list[str] = []
    last = 0
    for match in _FENCED_CODE_RE.finditer(text):
        parts.append(_protect_segment(text[last:match.start()]))
        parts.append(match.group(0))
        last = match.end()
    parts.append(_protect_segment(text[last:]))
    return "".join(parts)


def _protect_segment(text: str) -> str:
    parts: list[str] = []
    last = 0
    for match in _INLINE_CODE_RE.finditer(text):
        parts.append(_protect_math_tokens(text[last:match.start()]))
        parts.append(match.group(0))
        last = match.end()
    parts.append(_protect_math_tokens(text[last:]))
    return "".join(parts)


def _protect_math_tokens(text: str) -> str:
    text = _DISPLAY_MATH_RE.sub(_render_display_math, text)
    return _INLINE_MATH_RE.sub(_render_inline_math, text)


def _render_display_math(match: re.Match[str]) -> str:
    return f'<div class="math math-display">&#92;[{_escape_math(match.group(1))}&#92;]</div>'


def _render_inline_math(match: re.Match[str]) -> str:
    return f'<span class="math math-inline">&#92;({_escape_math(match.group(1))}&#92;)</span>'


def _escape_math(value: str) -> str:
    return html.escape(value, quote=False)
