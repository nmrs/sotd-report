from unittest import TestCase
from blade_usage_extractor import BladeUsageExtractor

from sotd_collator.blade_name_extractor import BladeNameExtractor


class TestBladeNameExtractor(TestCase):
    razor_name_cases = [
        {
            "comment": {
                "body": """**[Feb. 21, 2020 - Forgotten Friday](https://i.imgur.com/AiXQGG1.jpg)**

* **Prep:** None
* **Brush:** Washington Blue Steel B6
* **Razor:** Karve CB (Plate C)
* **Blade:** Gillette Nacet (3)
* **Lather:** [Declaration Grooming - Sweet Lemon - Soap](https://trythatsoap.com/collection/70/?product_type=soap)
* **Post Shave:** [Declaration Grooming - Sweet Lemon - Aftershave](https://trythatsoap.com/collection/70/?product_type=aftershave)

Better late than never.""",
            },
            "expected_name": "Gillette Nacet (3)",
            "expected_usage": 3,
        },
        {
            "comment": {
                "body": r"""***I Can't Stands No More : 2/28/20***

* **Brush** \- Maggard 24mm Synthetic
* **Razor** \- Maggard MR5 w/ V2 OC
* **Blade** \- Rapira (Fresh)
* **Lather** \- Barrister and Mann - Ravish
* **Post** \- Barrister and Mann - Ravish Splash
""",
            },
            "expected_name": "Rapira (Fresh)",
            "expected_usage": None,
        },
        {
            "comment": {
                "body": r"""**// Brush** \- Dogwood Handcrafts - SHD

**// Razor** \- Maggard MR 5 w/ V2 OC

**// Blade** \- Voskhod (4)

**// Lather** \- Turtleship Shave Co. - Bay Rum

**// Post** \- Pinaud Clubman""",
            },
            "expected_name": "Voskhod (4)",
            "expected_usage": 4,
        },
        {
            "comment": {
                "body": """* **Prep:** Cup of Coffee
* **Brush:** Sawdust Creations 26 mm Timberwolf
* **Razor:** [Chani](https://imgur.com/a/usfOaJp)

* **Lather:** [Summer Break Soaps - Bell Ringer - Soap](https://trythatsoap.com/collection/1183/?product_type=soap)

* **Post Shave:** [Summer Break Soaps - Bell Ringer - Aftershave](https://trythatsoap.com/collection/1183/?product_type=aftershave)

* **Post Shave:** Mod Cabin - Bare Essentials - Beard Oil
* **Fragrance:** Creed - Green Irish Tweed - Eau de Toilette

Stay safe and have a great day!""",
            },
            "expected_name": None,
            "expected_usage": None,
        },
        {
            "comment": {
                "body": r"""**// Brush** \- Dogwood Handcrafts - SHD

**// Razor** \- Maggard MR 5 w/ V2 OC

**// Blade** \- Voskhod (4)

**// Lather** \- Turtleship Shave Co. - Bay Rum

**// Post** \- Pinaud Clubman""",
            },
            "expected_name": "Voskhod (4)",
            "expected_usage": 4,
        },
        {
            # This comment isn't a SOTD report. Don't match follow on comments where people are replying
            # to a previous post or just talking conversationally.
            "comment": {
                "body": """Do you like the Astra SPs or SSs more?""",
            },
            "expected_name": None,
            "expected_usage": None,
        },
        {
            "comment": {
                "body": """February 17, 2024

Indian products

* Blade [365](https://www.reddit.com/r/Wetshavers_India/s/wSjU38Lgvg)

* Razor : Plearl L55
* Cream : Yardley Gold
* Brush : Hajamat Shaving brush
* Post shave : Alum and Nivea Replenishing Balm


Three pass shave WTG+WTG + ATG . The blade was on its third use. Nice shave""",
            },
            "expected_name": "365",
            "expected_usage": None,
        },
        {
            "comment": {
                "body": """February 17, 2024

* Blade [365](https://www.reddit.com/r/Wetshavers_India/s/wSjU38Lgvg) (12)
""",
            },
            "expected_name": "365 (12)",
            "expected_usage": 12,
        },
        {
            "comment": {
                "body": "* Blade GSB {2}",
            },
            "expected_name": "GSB {2}",
            "expected_usage": 2,
        },
        {
            "comment": {
                "body": "* Blade GSB (2)",
            },
            "expected_name": "GSB (2)",
            "expected_usage": 2,
        },
        {
            "comment": {
                "body": "* Blade GSB [3]",
            },
            "expected_name": "GSB [3]",
            "expected_usage": 3,
        },
        {
            "comment": {
                "body": """2/17/24

• Prep:  shower     
• Razor:  Henson ++     
• Blade:  Nacet (6x)
• Lather:  Pre de Provance No 63     
• Post shave:  Stirling Toner      
• Post:  Soap Commander Integrity balm.""",
            },
            "expected_name": "Nacet (6x)",
            "expected_usage": 6,
        },
    ]

    def test_get_blade_name_cases(self):
        ne = BladeNameExtractor()
        for case in self.razor_name_cases:
            r_name = ne.get_name(case["comment"])
            self.assertEqual(case["expected_name"], r_name)

    def test_get_blade_usage_cases(self):
        ne = BladeUsageExtractor()
        for case in self.razor_name_cases:
            r_usage = ne.get_name(case["comment"])
            self.assertEqual(case["expected_usage"], r_usage)


if __name__ == "__main__":
    bne = TestBladeNameExtractor()
    bne.test_get_blade_name_cases()
    bne.test_get_blade_usage_cases()
