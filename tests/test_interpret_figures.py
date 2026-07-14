import unittest

import pipeline.interpret as interpret


class InterpretFigureTests(unittest.TestCase):
    def test_deep_dive_has_no_key_figure_limit(self):
        self.assertNotIn("max_figures", interpret.deep_dive.__code__.co_varnames)

    def test_all_local_images_are_retained(self):
        figures = [
            {"local_paths": ["fig1_1.png", None, "fig1_2.png"]},
            {"local_paths": ["fig2_1.png"]},
        ]
        entries = interpret.all_figure_images(figures)
        self.assertEqual([path for _, path in entries], [
            "fig1_1.png", "fig1_2.png", "fig2_1.png"
        ])


if __name__ == "__main__":
    unittest.main()
