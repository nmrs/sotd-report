from unittest import TestCase
from sotd_collator.karve_plate_extractor import KarvePlateExtractor


class TestKarvePlateExtractor(TestCase):
    plate_name_cases = [
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
            "expected_result": "C SB",
        },
        {
            "comment": {
                "body": """SOTD - Aug 28

* Lather - M&M Gael Laoch
* Brush - Doglaration B7
* Razor - SS Karve Plate F
* Blade - GSB (254)
* Post - Gael Laoch
* Frag - Creed Royal Oud
    """,
            },
            "expected_result": "F SB",
        },
        {
            "comment": {
                "body": """**[Aug. 1, 2020 - Into the Stag - Day 1](https://i.imgur.com/JTt6010.jpg)**

* **Prep:** Hot Shower
* **Brush:** Stirling 24mm Fan
* **Razor:** Karve A Plate
* **Blade:** Nacet (1)
* **Lather:** [Chiseled Face - Midnight Stag - Soap](https://trythatsoap.com/collection/32/?product_type=soap)

* **Post Shave:** [Chiseled Face - Midnight Stag - Aftershave](https://trythatsoap.com/collection/32/?product_type=aftershave)


* **Fragrance:** [Chiseled Face - Midnight Stag - Eau de Parfum](https://trythatsoap.com/collection/32/?product_type=eaudeparfum)

So it begins... started with a virgin Stag set today.
""",
            },
            "expected_result": "A SB",
        },
        {
            "comment": {
                "body": """
**Aug. 31, 2020 - AA with Proraso Blue All the Way**

* **Prep:** Proraso - Aloe and Vitamin E - Pre-shave
* **Brush:** Decalration Grooming - Jefferson Unicorn Ivory B9A
* **Razor:** Karve Christopher Bradley OC B
* **Blade:** Gillette Silver Blue (26)
* **Lather:** [Proraso - Aloe and Vitamin E - Cream](https://trythatsoap.com/collection/1518/?product_type=cream)

* **Post Shave:** Proraso - Aloe and Vitamin E - Balm


One blade. One razor. One pre-shave. One cream. One brush. One balm.  Done.
""",
            },
            "expected_result": "B OC",
        },
        {
            "comment": {
                "body": """
    * **Brush:** Restored Barber Handle w/28mm Maggards 2 band badger
    * **Razor:** Karve CB Brass OC-F
    * **Blade:**  Astra SP (5)
    * **Lather:** Spearhead - Seaforth Spiced
    * **Post Shave:** Lucky Tiger splash
    * **Post Shave:** House of Mammoth - Hygge splash
    I gave some blood this morning, thankfully just in the form of weepers.  I'm not an open comb kind of guy, but since this CB came with an F plate, I figured I had to try it.  Honestly, it wasn't as aggressive as I thought it would be but it was definitely more than I typically use, thus the blood donation.  My face was definitely a little raw after the shave so some calming Lucky Tiger was perfect.  If anyone wants to try the F plate, this might be a good passaround for those who are curious.

    Time to Tuesday.  Time to get more coffee in my veins.  Try to enjoy your day and remember to be kind to one another.
    """,
            },
            "expected_result": "F OC",
        },
    ]

    def test_get_name(self):
        kpe = KarvePlateExtractor()
        for case in self.plate_name_cases:
            p_name = kpe.get_name(case["comment"])
            self.assertEqual(case["expected_result"], p_name)

if __name__ == "__main__":
    TestKarvePlateExtractor().test_get_name()