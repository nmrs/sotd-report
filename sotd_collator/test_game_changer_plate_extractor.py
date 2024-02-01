from unittest import TestCase
from sotd_collator.game_changer_plate_extractor import GameChangerPlateExtractor


class TestGameChangerPlateExtractor(TestCase):
    plate_name_cases = [
        {
            "comment": {
                "body": r"""
**// Razor** \- GC 68
""",
            },
            "expected_result": ".68-P",
        },
        {
            "comment": {
                "body": r"""
**// Razor** \- Game Changer .68P
""",
            },
            "expected_result": ".68-P",
        },
        {
            "comment": {
                "body": r"""
**// Razor** \- Game Changer .76-P
""",
            },
            "expected_result": ".76-P",
        },
        {
            "comment": {
                "body": r"""
**// Razor** \- Game Changer 1.05
""",
            },
            "expected_result": "1.05-P",
        },
        {
            "comment": {
                "body": r"""
**// Razor** \- Game Changer 1.05 OC
""",
            },
            "expected_result": "1.05-P OC",
        },
        {
            "comment": {
                "body": r"""
**// Razor** \- Game Changer 1.05 open comb
""",
            },
            "expected_result": "1.05-P OC",
        },
        {
            "comment": {
                "body": r"""
**// Razor** \- Game Changer 1.05 jaws
""",
            },
            "expected_result": "1.05-P JAWS",
        },
    ]

    def test_get_name(self):
        pe = GameChangerPlateExtractor()
        for case in self.plate_name_cases:
            p_name = pe.get_name(case["comment"])
            self.assertEqual(case["expected_result"], p_name)


if __name__ == "__main__":
    tpe = TestGameChangerPlateExtractor()
    tpe.test_get_name()
