import json
import tempfile
import unittest
from pathlib import Path

from pipeline.annotations import apply_annotations, load_annotations


class AnnotationTests(unittest.TestCase):
    def test_wraps_terms_in_text_nodes_with_tooltip(self):
        html = "<article><p>开环执行牺牲了闭环反应能力。</p></article>"
        annotations = [
            {"term": "开环", "definition": "先计划一段动作，再按计划执行。"},
            {"term": "闭环", "definition": "根据执行过程中的反馈持续修正动作。"},
        ]

        rendered = apply_annotations(html, annotations)

        self.assertIn('class="note-term"', rendered)
        self.assertIn("开环", rendered)
        self.assertIn("先计划一段动作，再按计划执行。", rendered)
        self.assertIn("闭环", rendered)
        self.assertIn("根据执行过程中的反馈持续修正动作。", rendered)

    def test_does_not_annotate_links_code_or_existing_markup(self):
        html = (
            '<article><p><a href="/开环">开环</a> '
            "<code>闭环</code> 开环</p></article>"
        )
        annotations = [{"term": "开环", "definition": "解释"}]

        rendered = apply_annotations(html, annotations)

        self.assertEqual(rendered.count('class="note-term"'), 1)
        self.assertIn('<a href="/开环">开环</a>', rendered)
        self.assertIn("<code>闭环</code>", rendered)

    def test_does_not_annotate_math_spans(self):
        html = (
            r'<p><span class="math math-inline">\( E_t \)</span> '
            "E_t</p>"
        )
        annotations = [{"term": "E_t", "definition": "视觉演化误差"}]

        rendered = apply_annotations(html, annotations)

        self.assertEqual(rendered.count('class="note-term"'), 1)
        self.assertIn(r'<span class="math math-inline">\( E_t \)</span>', rendered)

    def test_load_annotations_returns_empty_list_when_file_missing(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(load_annotations(Path(tmp), "zh"), [])

    def test_load_annotations_reads_language_specific_file(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "annotations.zh.json"
            path.write_text(
                json.dumps([{"term": "开环", "definition": "解释"}]),
                encoding="utf-8",
            )

            self.assertEqual(
                load_annotations(Path(tmp), "zh"),
                [{"term": "开环", "definition": "解释"}],
            )


if __name__ == "__main__":
    unittest.main()
