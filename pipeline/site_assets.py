from __future__ import annotations

from pathlib import Path


ASSET_DIR = Path(__file__).resolve().parent.parent / "assets"

CSS = (ASSET_DIR / "site.css").read_text(encoding="utf-8")
DECK_JS = (ASSET_DIR / "deck.js").read_text(encoding="utf-8")
MATH_JAX = r"""
<script>
window.MathJax = {
  tex: {
    inlineMath: [['\\(', '\\)']],
    displayMath: [['\\[', '\\]']]
  },
  options: {
    skipHtmlTags: ['script', 'noscript', 'style', 'textarea', 'pre', 'code']
  }
};
</script>
<script async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-chtml.js"></script>
""".strip()
