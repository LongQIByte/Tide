import json
import tempfile
import unittest
from pathlib import Path

import pipeline.publish as publish


class PublishAnnotationTests(unittest.TestCase):
    def test_render_paper_applies_language_specific_annotations(self):
        original_data_dir = publish.DATA_DIR
        try:
            with tempfile.TemporaryDirectory() as tmp:
                publish.DATA_DIR = Path(tmp) / "data"
                paper_dir = publish.DATA_DIR / "2026-07-06" / "paper-1"
                paper_dir.mkdir(parents=True)
                (paper_dir / "deep_dive.zh.md").write_text(
                    "# 标题\n\n开环执行会降低闭环反应能力。",
                    encoding="utf-8",
                )
                (paper_dir / "annotations.zh.json").write_text(
                    json.dumps(
                        [
                            {"term": "开环", "definition": "先计划一段动作再执行。"},
                            {"term": "闭环", "definition": "根据反馈持续修正动作。"},
                        ],
                        ensure_ascii=False,
                    ),
                    encoding="utf-8",
                )

                html = publish.render_paper(
                    "2026-07-06",
                    {"arxiv_id": "paper-1", "title": "Test Paper"},
                    "zh",
                )

                self.assertIsNotNone(html)
                self.assertEqual(html.count('class="note-term"'), 2)
                self.assertIn("先计划一段动作再执行。", html)
                self.assertIn("根据反馈持续修正动作。", html)
        finally:
            publish.DATA_DIR = original_data_dir


if __name__ == "__main__":
    unittest.main()
