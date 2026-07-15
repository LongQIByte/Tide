import tempfile
import unittest
from pathlib import Path

import pipeline.publish as publish


class PublishMathTests(unittest.TestCase):
    def test_render_paper_preserves_inline_latex_for_mathjax(self):
        original_data_dir = publish.DATA_DIR
        try:
            with tempfile.TemporaryDirectory() as tmp:
                publish.DATA_DIR = Path(tmp) / "data"
                paper_dir = publish.DATA_DIR / "2026-07-06" / "paper-1"
                paper_dir.mkdir(parents=True)
                (paper_dir / "deep_dive.zh.md").write_text(
                    "# 标题\n\n"
                    r"计算“\( E_t = 1 - \text{CosSim}(\Delta \hat{z}^v_t, \Delta z^v_t) \)”",
                    encoding="utf-8",
                )

                html = publish.render_paper(
                    "2026-07-06",
                    {"arxiv_id": "paper-1", "title": "Test Paper"},
                    "zh",
                )

                self.assertIsNotNone(html)
                self.assertIn('class="math math-inline"', html)
                self.assertIn("&#92;( E_t", html)
                self.assertIn("&#92;)</span>", html)
                self.assertIn(r"\text{CosSim}", html)
                self.assertIn("cdn.jsdelivr.net/npm/mathjax@3", html)
                self.assertNotIn("“( E_t", html)
        finally:
            publish.DATA_DIR = original_data_dir


if __name__ == "__main__":
    unittest.main()
