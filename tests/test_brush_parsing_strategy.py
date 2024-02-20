from unittest import TestCase
from brush_parser import BrushParser

from sotd_collator.blade_name_extractor import BladeNameExtractor


class TestBrushParser(TestCase):

    test_cases = [
        # {
        #     "input": "some random B8",
        #     "expected_result": {"name": "Declaration Grooming B8", "fiber": "Badger"},
        # },
        {  # https://www.reddit.com/r/Wetshaving/comments/18vr8n7/comment/kfu7f59/
            "input": "AP Shave Co. 24mm G5C Premium Synthetic fan Knot set in DS Cosmetics Jade Green handle",
            "expected_result": {
                "name": "AP Shave Co. Synthetic",
                "fiber": "Synthetic",
                "knot size": "24mm",
            },
        },
    ]

    def test_get_blade_name_cases(self):
        ps = BrushParser()
        for case in self.test_cases:
            for key, value in case["expected_result"].items():
                result = ps._get_value(case["input"], key)
                self.assertEqual(result, value)


if __name__ == "__main__":
    tbp = TestBrushParser()
    tbp.test_get_blade_name_cases()
