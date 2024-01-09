from unittest import TestCase

from razor_name_extractor import RazorNameExtractor
from razor_name_extractor import RazorAlternateNamer


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
         'expected_result_principal': 'Karve CB',
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
            'expected_result_principal': 'Maggard V2',
        },
        {
            'comment': """**// Brush** \- Dogwood Handcrafts - SHD

**// Razor** \- Maggard MR 5 w/ V2 OC

**// Blade** \- Voskhod (4)

**// Lather** \- Turtleship Shave Co. - Bay Rum

**// Post** \- Pinaud Clubman""",
            'expected_result': 'Maggard MR 5 w/ V2 OC',
            'expected_result_principal': 'Maggard V2',
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
            'expected_result': 'Chani',
            'expected_result_principal': None,
        },
        {
            'comment': """
**// Razor** \- GC 2.0
""",
            'expected_result': 'GC 2.0',
            'expected_result_principal': 'Greencult GC 2.0',
        },
        {
            'comment': """
**// Razor** \- Game Changer 68
""",
            'expected_result': 'Game Changer 68',
            'expected_result_principal': 'Razorock Game Changer',
        },
        {
            'comment': """
**// Razor** \- GC
""",
            'expected_result': 'GC',
            'expected_result_principal': 'Razorock Game Changer',
        },
        {
            'comment': """
**// Razor** \- Gamechanger 68
""",
            'expected_result': 'Gamechanger 68',
            'expected_result_principal': 'Razorock Game Changer',
        },
        {
            'comment': """
[**SOTD 20231225 Maestri by IschiaPP @ Forio**](https://ischiapp.blogspot.com/2023/12/sotd-20231225.html)    
* Pre: Oleolito LCC Olio Prebarba Medicato  
Homemade by Dr IschiaPP
* Brush: Bat71 Cashmere  
Olive Wood, Abalone Shell Inlay, Yaqi SK07 aka Maggard Beige, 24x50x115mm
* Soap: Frankincense Giardini La Mortella Foro Afeitado 2019 Exclusive IschiaPP
* Razor: Gillette Labs UK 2023 Exfoliating Razor Neon Night Edition FlexDisc #41
* After: Oleotintura LCC Trattamento Urto Dopobarba Medicato  
Homemade by Dr IschiaPP
  
Full size: 1200x1200px  
Soundtrack: Joe Hisaishi - Merry go Round of Life  
from Howl's Moving Castle Miyazaki (by Grissini Project)
""",
            'expected_result': 'Gillette Labs UK 2023 Exfoliating Razor Neon Night Edition FlexDisc #41',
            'expected_result_principal': 'Cartridge / Disposable',
        },
        {
            # This comment isn't a SOTD report. Don't match follow on comments where people are replying 
            # to a previous post or just talking conversationally.
            'comment': """How do you like the CB? I've been trying to decide between the CB and the Overlander myself.""",
            'expected_result': None,
            'expected_result_principal': None,
        },
    ]


    def test_get_razor_name_cases(self):
        rn = RazorNameExtractor()
        for case in self.razor_name_cases:
            r_name = rn.get_name(case['comment'])
            self.assertEqual(case['expected_result'], r_name)

    def test_get_principal_name_cases(self):
        rn = RazorNameExtractor()
        arn = RazorAlternateNamer()
        r_aname = None
        for case in self.razor_name_cases:
            r_name = rn.get_name(case['comment'])
            if r_name:
                r_aname = arn.get_principal_name(case['comment'])
                self.assertEqual(case['expected_result_principal'], r_aname)


if __name__ == '__main__':
    rne = TestRazorNameExtractor()
    rne.test_get_principal_name_cases()
