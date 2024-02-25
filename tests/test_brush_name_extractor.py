from unittest import TestCase
from brush_name_extractor import BrushNameExtractor
from razor_parser import RazorParser

from sotd_collator.razor_name_extractor import RazorNameExtractor


class TestBrushNameExtractor(TestCase):
    razor_name_cases = [
        {
            "comment": {
                "body": """**February 1, 2024**  

* **Brush:** [Stirling x Zenith 510SE-XL](https://imgur.com/a/wzrZdDK)  
* **Razor:** Blackland Blackbird  
* **Blade:** Gillette Silver Blue   
* **Lather:** Red House Farm \u2013 Lumos  
* **Post Shave:** Stirling Soap Co. \u2013 Christmas Eve   

What can be brighter than a glow in the dark soap? The answer is a lot of things, but not for this theme. Here is to hoping winter actually becomes winter with some snow that I will enjoy for skiing.""",
            },
            "expected_result": "Stirling x Zenith 510SE-XL",
        },
    ]

    def test_get_brush_name_cases(self):
        rn = BrushNameExtractor()
        for case in self.razor_name_cases:
            r_name = rn.get_name(case["comment"])
            self.assertEqual(case["expected_result"], r_name)


if __name__ == "__main__":
    rne = TestBrushNameExtractor()
    rne.test_get_brush_name_cases()
