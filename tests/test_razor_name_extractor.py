from unittest import TestCase

from sotd_collator.razor_name_extractor import RazorNameExtractor
from sotd_collator.razor_name_extractor import RazorAlternateNamer


class TestRazorNameExtractor(TestCase):
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
            "expected_result": "Karve CB (Plate C)",
            "expected_result_principal": "Karve Christopher Bradley",
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
            "expected_result": "Maggard MR5 w/ V2 OC",
            "expected_result_principal": "Maggard V2",
        },
        {
            "comment": {
                "body": r"""**// Brush** \- Dogwood Handcrafts - SHD

**// Razor** \- Maggard MR 5 w/ V2 OC

**// Blade** \- Voskhod (4)

**// Lather** \- Turtleship Shave Co. - Bay Rum

**// Post** \- Pinaud Clubman""",
            },
            "expected_result": "Maggard MR 5 w/ V2 OC",
            "expected_result_principal": "Maggard V2",
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
            "expected_result": "Chani",
            "expected_result_principal": None,
        },
        {
            "comment": {
                "body": r"""
**// Razor** \- GC 2.0
""",
            },
            "expected_result": "GC 2.0",
            "expected_result_principal": "Greencult GC 2.0",
        },
        {
            "comment": {
                "body": r"""
**// Razor** \- Game Changer 68
""",
            },
            "expected_result": "Game Changer 68",
            "expected_result_principal": "Razorock Game Changer",
        },
        {
            "comment": {
                "body": r"""
**// Razor** \- GC
""",
            },
            "expected_result": "GC",
            "expected_result_principal": "Razorock Game Changer",
        },
        {
            "comment": {
                "body": r"""
**// Razor** \- Gamechanger 68
""",
            },
            "expected_result": "Gamechanger 68",
            "expected_result_principal": "Razorock Game Changer",
        },
        {
            "comment": {
                "body": """
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
            },
            "expected_result": "Gillette Labs UK 2023 Exfoliating Razor Neon Night Edition FlexDisc #41",
            "expected_result_principal": "Cartridge / Disposable",
        },
        {
            "comment": {
                "author": "Enndeegee",
                "body": "* razor: no name vintage Gillette old type clone (aggressive)\n* Brush: zenith red handle 27mm boar\n* Lather: barrister and Mann : reserve cool\n\n\nFormat almost back to normal to help u/jimm262 but I realise my plethora of random shit like the various no name old type clones I own probably won't show up anyway.",
                "created_utc": "2024-01-24 01:52:08",
                "id": "kjbm31v",
                "url": "https://www.reddit.com/r/Wetshaving/comments/19eb698/comment/kjbm31v/",
                "razor": "no name vintage Gillette old type clone (aggressive)",
                "brush": "zenith red handle 27mm boar",
            },
            "expected_result": "no name vintage Gillette old type clone (aggressive)",
            "expected_result_principal": "Clone of some other razor",
        },
        {
            # This comment isn't a SOTD report. Don't match follow on comments where people are replying
            # to a previous post or just talking conversationally.
            "comment": {
                "author": "djundjila",
                "body": "## [Smoke 'em if you got 'em](https://imgur.com/Cz9dzR6.jpeg)\n\n* **Prep:** Klar - Aktiv Kohle - activated charcoal facial soap\n* **Brush:** Djundjila Brushworks - Haverford #BICOLOR\n* **Razor:** Hensonford - Henson AL13 Mild aluminium head on Djundjila Razorworks Haverford zamac handle #FRANKENRAZOR\n* **Blade:**  RK - Stainless Double Edge Blades  o\n* **Lather:** [Moon Soaps - Havana - Soap](https://trythatsoap.com/collection/2262/?product_type=soap)\n* **Post Shave:** [Summer Break Soaps - Valedictorian - Aftershave](https://trythatsoap.com/collection/2312/?product_type=aftershave)\n* **Fragrance:** [Stirling Soap Co. - Haverford - Eau de Toilette](https://trythatsoap.com/collection/1450/?product_type=eaudetoilette)\n\nu/Newtothethis appreciation day! One year and almost three weeks ago, we were asked to lather on our cans, the implication being man cans. This was [rightfully criticised by](https://reddit.com/r/Wetshaving/comments/nuxr24/tuesday_lather_games_sotd_thread_jun_08_2021/h11cllx/?context=0) u/Newtothethis who promptly created today's challenge in these words:\n\n\"*Next year, y'all should lather on your knee as to simulate the inconvenience of lathering so far away from the region you are actually shaving.*\"\n\nI'd say mission accomplished, the inconvenience has been [adequately simulated](https://imgur.com/ySPgFfV.jpeg).\n\nI'll keep the shave description and #FOF-fery short because I had a beast of a day and I just want to go pass out in bed. For today's shave I followed my man u/Teufelskraft's lead and created an aluminum-zamac-clay hybrid #FRANKENRAZOR. This was my first try of Moon Soap's Havana soap. The base is much firmer than the one of Moon Soap's Union. I spread a good wad of soap on the bottom of my Captain's Choice heavy copper bowl and immediately the scent off it was intoxicating and delicious. It reminded me of HoM Tobacconist, that's how good it smells. I picked up the soap with a damp brush and lathered on my knee, as per instructions. The base is easy to dial in and I had three very comfy passes with the Hensonford frankenrazor. The Valedictorian splash is my favourite SBS scent to date and while tobacco-centric, it adds earthy, citrussy, sweet, smoky and woodsy notes. Simply a fantastic scent! I topped it all up with my secret/not-so-secret obsession, Haverford EdT. This sweet and gourmand fresh baked cookie scent will never not make me happy.\n\n**Stirling Soap**\n\nI can say only good things about Stirling. For instance, they have the best sample size in the business. Varen and Haverford are godly scents (I know that Haverford is a dupe), Boat Drinks makes me happy and Pharaoh's Dreamsicle makes my mouth water.\n\n* Themes fulfilled: 27/30\n* Hardware vendors: 4/2\n* Software sponsors: 12/15\n* Different soaps: 27/30\n* Different soap brands: 27/30\n* Post-shave products: 27/30\n* Different fragrances: 27/30\n* Hardware Scavenger Hunt Tags: 40/40\n* Additional Scavenger Hunt Tags: 14 (+ #FRANKENRAZOR)\n* Art of Wetshaving points: 27/30\n* Daily challenges completed: 27/30",
                "created_utc": "2022-06-27 20:12:47",
                "id": "idzsde8",
                "url": "https://www.reddit.com/r/Wetshaving/comments/vloh9w/comment/idzsde8/",
                "razor": "Hensonford - Henson AL13 Mild aluminium head on Djundjila Razorworks Haverford zamac handle #FRANKENRAZOR",
                "blade": "RK - Stainless Double Edge Blades  o",
                "brush": "Djundjila Brushworks - Haverford #BICOLOR",
            },
            "expected_result": "Hensonford - Henson AL13 Mild aluminium head on Djundjila Razorworks Haverford zamac handle #FRANKENRAZOR",
            "expected_result_principal": "Henson AL13",
        },
        {
            # This comment isn't a SOTD report. Don't match follow on comments where people are replying
            # to a previous post or just talking conversationally.
            "comment": {
                "body": """How do you like the CB? I've been trying to decide between the CB and the Overlander myself.""",
            },
            "expected_result": None,
            "expected_result_principal": None,
        },
    ]

    def test_get_razor_name_cases(self):
        rn = RazorNameExtractor()
        for case in self.razor_name_cases:
            r_name = rn.get_name(case["comment"])
            self.assertEqual(case["expected_result"], r_name)

    def test_get_principal_name_cases(self):
        rn = RazorNameExtractor()
        arn = RazorAlternateNamer()
        r_aname = None
        for case in self.razor_name_cases:
            r_name = rn.get_name(case["comment"])
            if r_name:
                r_aname = arn.get_principal_name(r_name)
                self.assertEqual(case["expected_result_principal"], r_aname)


if __name__ == "__main__":
    rne = TestRazorNameExtractor()
    rne.test_get_principal_name_cases()