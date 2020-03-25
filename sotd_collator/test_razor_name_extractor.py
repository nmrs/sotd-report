from unittest import TestCase

from razor_name_extractor import RazorNameExtractor


class TestRazorNameExtractor(TestCase):
    razor_name_cases = [
        {'comment': """**[Feb. 21, 2020 - Forgotten Friday](https://i.imgur.com/AiXQGG1.jpg)**  

* **Prep:** None  
* **Brush:** Washington Blue Steel B6  
* **Razor:** Karve CB (Plate C)  
* **Blade:** Gillette Nacet (3)  
* **Lather:** [Declaration Grooming - Sweet Lemon - Soap](https://trythatsoap.com/collection/70/?product_type=soap)  
* **Post Shave:** [Declaration Grooming - Sweet Lemon - Aftershave](https://trythatsoap.com/collection/70/?product_type=aftershave)  

Better late than never.""",
         'expected_result': 'Karve CB (Plate C)',
         },
        {
            'comment': """***I Can't Stands No More : 2/28/20***

* **Brush** \- Maggard 24mm Synthetic
* **Razor** \- Maggard MR5 w/ V2 OC
* **Blade** \- Rapira (Fresh)
* **Lather** \- Barrister and Mann - Ravish
* **Post** \- Barrister and Mann - Ravish Splash
""",
            'expected_result': 'Maggard MR5 w/ V2 OC',
        },
        {
            'comment': """**// Brush** \- Dogwood Handcrafts - SHD

**// Razor** \- Maggard MR 5 w/ V2 OC

**// Blade** \- Voskhod (4)

**// Lather** \- Turtleship Shave Co. - Bay Rum

**// Post** \- Pinaud Clubman""",
            'expected_result': 'Maggard MR 5 w/ V2 OC',
        }
    ]

    def test_get_razor_name_cases(self):
        rn = RazorNameExtractor()
        for case in self.razor_name_cases:
            r_name = rn.get_razor_name(case['comment'])
            self.assertEqual(case['expected_result'], r_name)
