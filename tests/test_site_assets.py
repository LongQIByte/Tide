import unittest

from pipeline.site_assets import CSS


class SiteAssetTests(unittest.TestCase):
    def test_deck_text_selection_uses_white_highlight(self):
        self.assertIn(".deck ::selection", CSS)
        self.assertIn("background: #fff;", CSS)
        self.assertIn("color: var(--night);", CSS)

    def test_deck_annotation_terms_are_white(self):
        self.assertIn(".deck .note-term", CSS)
        self.assertIn("color: #fff;", CSS)
        self.assertIn("background: transparent;", CSS)
        self.assertIn("border-bottom-color: rgba(255,255,255,.75);", CSS)


if __name__ == "__main__":
    unittest.main()
