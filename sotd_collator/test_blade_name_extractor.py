from unittest import TestCase

from blade_name_extractor import BladeNameExtractor


class TestBladeNameExtractor(TestCase):
    razor_name_cases = [
        {'comment': """**[Feb. 21, 2020 - Forgotten Friday](https://i.imgur.com/AiXQGG1.jpg)**  

* **Prep:** None  
* **Brush:** Washington Blue Steel B6  
* **Razor:** Karve CB (Plate C)  
* **Blade:** Gillette Nacet (3)  
* **Lather:** [Declaration Grooming - Sweet Lemon - Soap](https://trythatsoap.com/collection/70/?product_type=soap)  
* **Post Shave:** [Declaration Grooming - Sweet Lemon - Aftershave](https://trythatsoap.com/collection/70/?product_type=aftershave)  

Better late than never.""",
         'expected_result': 'Gillette Nacet',
         },
        {
            'comment': """***I Can't Stands No More : 2/28/20***

* **Brush** \- Maggard 24mm Synthetic
* **Razor** \- Maggard MR5 w/ V2 OC
* **Blade** \- Rapira (Fresh)
* **Lather** \- Barrister and Mann - Ravish
* **Post** \- Barrister and Mann - Ravish Splash
""",
            'expected_result': 'Rapira Fresh',
        },
        {
            'comment': """**// Brush** \- Dogwood Handcrafts - SHD

**// Razor** \- Maggard MR 5 w/ V2 OC

**// Blade** \- Voskhod (4)

**// Lather** \- Turtleship Shave Co. - Bay Rum

**// Post** \- Pinaud Clubman""",
            'expected_result': 'Voskhod',
        },
        {
            'comment': """* **Prep:** Cup of Coffee  
* **Brush:** Sawdust Creations 26 mm Timberwolf  
* **Razor:** [Chani](https://imgur.com/a/usfOaJp)  

* **Lather:** [Summer Break Soaps - Bell Ringer - Soap](https://trythatsoap.com/collection/1183/?product_type=soap)  

* **Post Shave:** [Summer Break Soaps - Bell Ringer - Aftershave](https://trythatsoap.com/collection/1183/?product_type=aftershave)

* **Post Shave:** Mod Cabin - Bare Essentials - Beard Oil  
* **Fragrance:** Creed - Green Irish Tweed - Eau de Toilette  

Stay safe and have a great day!""",
            'expected_result': None,
        },
                {
            'comment': """**// Brush** \- Dogwood Handcrafts - SHD

**// Razor** \- Maggard MR 5 w/ V2 OC

**// Blade** \- Voskhod (4)

**// Lather** \- Turtleship Shave Co. - Bay Rum

**// Post** \- Pinaud Clubman""",
            'expected_result': 'Voskhod',
        },
        {
            # This comment isn't a SOTD report. Don't match follow on comments where people are replying 
            # to a previous post or just talking conversationally.
            'comment': """Do you like the Astra SPs or SSs more?""",
            'expected_result': None,
        },
    ]


    def test_get_blade_name_cases(self):
        ne = BladeNameExtractor()
        for case in self.razor_name_cases:
            r_name = ne.get_name(case['comment'])
            self.assertEqual(case['expected_result'], r_name)
