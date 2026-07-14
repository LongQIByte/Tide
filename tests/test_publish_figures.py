import unittest

import pipeline.publish as publish


class PublishFigureTests(unittest.TestCase):
    def test_parse_slides_keeps_multiple_images_in_one_figure(self):
        slides = publish._parse_slides(
            "![left](fig4_1.webp)\n\n"
            "![right](fig4_2.webp)\n\n"
            "> Figure 4 caption.\n\n"
            "Explanation text."
        )

        self.assertEqual(slides[0]["imgs"], ["fig4_1.webp", "fig4_2.webp"])
        self.assertEqual(slides[0]["img"], "fig4_1.webp")
        self.assertNotIn("![right]", slides[0]["html"])

    def test_render_deck_outputs_all_stage_images(self):
        launcher, deck = publish._render_deck(
            [
                {
                    "img": "fig4_1.webp",
                    "imgs": ["fig4_1.webp", "fig4_2.webp"],
                    "caption": "Figure 4 caption.",
                    "html": "<p>Explanation text.</p>",
                }
            ],
            "zh",
        )

        self.assertIn('src="fig4_1.webp"', launcher)
        self.assertIn('class="stage multi"', deck)
        self.assertIn('src="fig4_1.webp"', deck)
        self.assertIn('src="fig4_2.webp"', deck)


if __name__ == "__main__":
    unittest.main()
