from unittest import TestCase
from razor_parser import RazorParser

from sotd_collator.razor_name_extractor import RazorNameExtractor


class TestRazorNameExtractor(TestCase):
    razor_name_cases = [
        #         {
        #             "comment": {
        #                 "body": """**[Feb. 21, 2020 - Forgotten Friday](https://i.imgur.com/AiXQGG1.jpg)**
        # * **Prep:** None
        # * **Brush:** Washington Blue Steel B6
        # * **Razor:** Karve CB (Plate C)
        # * **Blade:** Gillette Nacet (3)
        # * **Lather:** [Declaration Grooming - Sweet Lemon - Soap](https://trythatsoap.com/collection/70/?product_type=soap)
        # * **Post Shave:** [Declaration Grooming - Sweet Lemon - Aftershave](https://trythatsoap.com/collection/70/?product_type=aftershave)
        # Better late than never.""",
        #             },
        #             "expected_result": "Karve CB (Plate C)",
        #             "expected_result_principal": "Karve Christopher Bradley",
        #         },
        #         {
        #             "comment": {
        #                 "body": r"""***I Can't Stands No More : 2/28/20***
        # * **Brush** \- Maggard 24mm Synthetic
        # * **Razor** \- Maggard MR5 w/ V2 OC
        # * **Blade** \- Rapira (Fresh)
        # * **Lather** \- Barrister and Mann - Ravish
        # * **Post** \- Barrister and Mann - Ravish Splash
        # """,
        #             },
        #             "expected_result": "Maggard MR5 w/ V2 OC",
        #             "expected_result_principal": "Maggard V2",
        #         },
        #         {
        #             "comment": {
        #                 "body": r"""**// Brush** \- Dogwood Handcrafts - SHD
        # **// Razor** \- Maggard MR 5 w/ V2 OC
        # **// Blade** \- Voskhod (4)
        # **// Lather** \- Turtleship Shave Co. - Bay Rum
        # **// Post** \- Pinaud Clubman""",
        #             },
        #             "expected_result": "Maggard MR 5 w/ V2 OC",
        #             "expected_result_principal": "Maggard V2",
        #         },
        #         {
        #             "comment": {
        #                 "body": """* **Prep:** Cup of Coffee
        # * **Brush:** Sawdust Creations 26 mm Timberwolf
        # * **Razor:** [Chani](https://imgur.com/a/usfOaJp)
        # * **Lather:** [Summer Break Soaps - Bell Ringer - Soap](https://trythatsoap.com/collection/1183/?product_type=soap)
        # * **Post Shave:** [Summer Break Soaps - Bell Ringer - Aftershave](https://trythatsoap.com/collection/1183/?product_type=aftershave)
        # * **Post Shave:** Mod Cabin - Bare Essentials - Beard Oil
        # * **Fragrance:** Creed - Green Irish Tweed - Eau de Toilette
        # Stay safe and have a great day!""",
        #             },
        #             "expected_result": "Chani",
        #             "expected_result_principal": None,
        #         },
        #         {
        #             "comment": {
        #                 "body": r"""
        # **// Razor** \- GC 2.0
        # """,
        #             },
        #             "expected_result": "GC 2.0",
        #             "expected_result_principal": "Greencult GC 2.0",
        #         },
        #         {
        #             "comment": {
        #                 "body": r"""
        # **// Razor** \- Game Changer 68
        # """,
        #             },
        #             "expected_result": "Game Changer 68",
        #             "expected_result_principal": "RazoRock Game Changer",
        #         },
        #         {
        #             "comment": {
        #                 "body": r"""
        # **// Razor** \- GC
        # """,
        #             },
        #             "expected_result": "GC",
        #             "expected_result_principal": "RazoRock Game Changer",
        #         },
        #         {
        #             "comment": {
        #                 "body": r"""
        # **// Razor** \- Gamechanger 68
        # """,
        #             },
        #             "expected_result": "Gamechanger 68",
        #             "expected_result_principal": "RazoRock Game Changer",
        #         },
        #         {
        #             "comment": {
        #                 "body": """
        # [**SOTD 20231225 Maestri by IschiaPP @ Forio**](https://ischiapp.blogspot.com/2023/12/sotd-20231225.html)
        # * Pre: Oleolito LCC Olio Prebarba Medicato
        # Homemade by Dr IschiaPP
        # * Brush: Bat71 Cashmere
        # Olive Wood, Abalone Shell Inlay, Yaqi SK07 aka Maggard Beige, 24x50x115mm
        # * Soap: Frankincense Giardini La Mortella Foro Afeitado 2019 Exclusive IschiaPP
        # * Razor: Gillette Labs UK 2023 Exfoliating Razor Neon Night Edition FlexDisc #41
        # * After: Oleotintura LCC Trattamento Urto Dopobarba Medicato
        # Homemade by Dr IschiaPP
        # Full size: 1200x1200px
        # Soundtrack: Joe Hisaishi - Merry go Round of Life
        # from Howl's Moving Castle Miyazaki (by Grissini Project)
        # """,
        #             },
        #             "expected_result": "Gillette Labs UK 2023 Exfoliating Razor Neon Night Edition FlexDisc #41",
        #             "expected_result_principal": "Cartridge / Disposable",
        #         },
        #         {
        #             "comment": {
        #                 "author": "Enndeegee",
        #                 "body": "* razor: no name vintage Gillette old type clone (aggressive)\n* Brush: zenith red handle 27mm boar\n* Lather: barrister and Mann : reserve cool\n\n\nFormat almost back to normal to help u/jimm262 but I realise my plethora of random shit like the various no name old type clones I own probably won't show up anyway.",
        #                 "created_utc": "2024-01-24 01:52:08",
        #                 "id": "kjbm31v",
        #                 "url": "https://www.reddit.com/r/Wetshaving/comments/19eb698/comment/kjbm31v/",
        #                 "razor": "no name vintage Gillette old type clone (aggressive)",
        #                 "brush": "zenith red handle 27mm boar",
        #             },
        #             "expected_result": "no name vintage Gillette old type clone (aggressive)",
        #             "expected_result_principal": "Other DE Clone",
        #         },
        #         {
        #             # This comment isn't a SOTD report. Don't match follow on comments where people are replying
        #             # to a previous post or just talking conversationally.
        #             "comment": {
        #                 "author": "djundjila",
        #                 "body": "## [Smoke 'em if you got 'em](https://imgur.com/Cz9dzR6.jpeg)\n\n* **Prep:** Klar - Aktiv Kohle - activated charcoal facial soap\n* **Brush:** Djundjila Brushworks - Haverford #BICOLOR\n* **Razor:** Hensonford - Henson AL13 Mild aluminium head on Djundjila Razorworks Haverford zamac handle #FRANKENRAZOR\n* **Blade:**  RK - Stainless Double Edge Blades  o\n* **Lather:** [Moon Soaps - Havana - Soap](https://trythatsoap.com/collection/2262/?product_type=soap)\n* **Post Shave:** [Summer Break Soaps - Valedictorian - Aftershave](https://trythatsoap.com/collection/2312/?product_type=aftershave)\n* **Fragrance:** [Stirling Soap Co. - Haverford - Eau de Toilette](https://trythatsoap.com/collection/1450/?product_type=eaudetoilette)\n\nu/Newtothethis appreciation day! One year and almost three weeks ago, we were asked to lather on our cans, the implication being man cans. This was [rightfully criticised by](https://reddit.com/r/Wetshaving/comments/nuxr24/tuesday_lather_games_sotd_thread_jun_08_2021/h11cllx/?context=0) u/Newtothethis who promptly created today's challenge in these words:\n\n\"*Next year, y'all should lather on your knee as to simulate the inconvenience of lathering so far away from the region you are actually shaving.*\"\n\nI'd say mission accomplished, the inconvenience has been [adequately simulated](https://imgur.com/ySPgFfV.jpeg).\n\nI'll keep the shave description and #FOF-fery short because I had a beast of a day and I just want to go pass out in bed. For today's shave I followed my man u/Teufelskraft's lead and created an aluminum-zamac-clay hybrid #FRANKENRAZOR. This was my first try of Moon Soap's Havana soap. The base is much firmer than the one of Moon Soap's Union. I spread a good wad of soap on the bottom of my Captain's Choice heavy copper bowl and immediately the scent off it was intoxicating and delicious. It reminded me of HoM Tobacconist, that's how good it smells. I picked up the soap with a damp brush and lathered on my knee, as per instructions. The base is easy to dial in and I had three very comfy passes with the Hensonford frankenrazor. The Valedictorian splash is my favourite SBS scent to date and while tobacco-centric, it adds earthy, citrussy, sweet, smoky and woodsy notes. Simply a fantastic scent! I topped it all up with my secret/not-so-secret obsession, Haverford EdT. This sweet and gourmand fresh baked cookie scent will never not make me happy.\n\n**Stirling Soap**\n\nI can say only good things about Stirling. For instance, they have the best sample size in the business. Varen and Haverford are godly scents (I know that Haverford is a dupe), Boat Drinks makes me happy and Pharaoh's Dreamsicle makes my mouth water.\n\n* Themes fulfilled: 27/30\n* Hardware vendors: 4/2\n* Software sponsors: 12/15\n* Different soaps: 27/30\n* Different soap brands: 27/30\n* Post-shave products: 27/30\n* Different fragrances: 27/30\n* Hardware Scavenger Hunt Tags: 40/40\n* Additional Scavenger Hunt Tags: 14 (+ #FRANKENRAZOR)\n* Art of Wetshaving points: 27/30\n* Daily challenges completed: 27/30",
        #                 "created_utc": "2022-06-27 20:12:47",
        #                 "id": "idzsde8",
        #                 "url": "https://www.reddit.com/r/Wetshaving/comments/vloh9w/comment/idzsde8/",
        #                 "razor": "Hensonford - Henson AL13 Mild aluminium head on Djundjila Razorworks Haverford zamac handle #FRANKENRAZOR",
        #                 "blade": "RK - Stainless Double Edge Blades  o",
        #                 "brush": "Djundjila Brushworks - Haverford #BICOLOR",
        #             },
        #             "expected_result": "Hensonford - Henson AL13 Mild aluminium head on Djundjila Razorworks Haverford zamac handle #FRANKENRAZOR",
        #             "expected_result_principal": "Henson AL13",
        #         },
        #         {
        #             # This comment isn't a SOTD report. Don't match follow on comments where people are replying
        #             # to a previous post or just talking conversationally.
        #             "comment": {
        #                 "body": """How do you like the CB? I've been trying to decide between the CB and the Overlander myself.""",
        #             },
        #             "expected_result": None,
        #             "expected_result_principal": None,
        #         },
        {
            "comment": {
                "body": r"*Prep:* Splash of Cool Water  \n*Razor:* **Weck - Sextoblade**  \n*Blade:* **Kismet - Hair Shaper** (1)  \n*Lather:* **Summer Break Soaps** - **Remote Learning**  \n*Brush:* **Declaration Grooming - B13** Dogwood/Briar Hybrid 28mm (22 uses)  \n*Post Shave:* Pre de Provence - No. 63  \n\n----\n\n[Gear Pic](https://i.imgur.com/zyG7MHU.jpg) :: [Video](https://youtu.be/LQWF4SJ9t48)\n\n#### \u4dc0 General Notes  \nMy first try with a Weck and the hair shaper blades as well. I also get a good slurry lather with a high-density badger by changing the water amount.\n\nThanks /u/gcgallant for the Weck and blades and tips and all!!!!\n\nAnd Greg... I just realized that I've been pronouncing your last name, like a fop, with the accent on the last syllable. Maybe I had some kind of international impression on my brain when we first started communicating or something. If you pronounce it with the emphasis on the first, then I'm sorry (and I bet you've been chuckling to yourself for a while now).\n\n#### \u4dc0 Razor and Blade Notes\n*^(Weck - Sextoblade ::: Kismet - Hair Shaper \u20391 uses\u203a)*\n\nWell, I did get cut in 4-5 places.  But those were just mistakes on my part, since I don't have great straight technique yet. \n\nBy the end of the shave, all but one of the cuts had sealed up, and the last one turned from a bleeder to a very slow weeper.\n\nThe Weck and the Kismet definitely take some practice, and I think are less forgiving than the 3 straights I've tried so far. However, I saw in some forums that after one or two shaves, the Kismet might smooth out a little.\n\nI did feel a general irritation at the end of the shave, after the final rinse.  But, I put on a decent balm, and all the tenderness and raw-ness went away, even before I left the bathroom. Looking back at that, I was very surprised.\n\nBut I got a close shave on my cheeks, and my neck was done pretty well too.  I didn't do a third pass, because of the irritation, and I didn't pursue every little bit of stubble on my neck, but I think my result was respectable.\n\nRazor and Blade Performance/Comfort Rating: 1 out of 5 (Poor)\n\n#### \u4dc0 Soap Notes\n*^(Summer Break Soaps - Remote Learning)*\n\nThem: Doritos\n\nScent: nacho cheesy corn tortilla chips is the goal here.  I imagine that's a tough challenge.  While smelling the dry tub and the wet lather, what comes to me first is a cookie sweet type scent that reminds me of some cinnamon schoolbook cookies from Trader Joes.  It's a nice scent, so I don't mind if my  brain never switches away from that.\n\nIf I know it is supposed to be corn chips, then I can definitely see that in the scent.  So that's cool.\n\nBut even if I set my brain to try to find a cheesy note in there, I really can't.\n\nI think it might be more realistic with a hint-of-cumin type scent in there, but of course, that could make it hard on skin maybe.\n\nWhile I may not really get a Doritos scent from it, I think it's a great attempt, and I know that I like shaving with it anyway.\n\nScent Strength: 4/10, present during shaving.\n\nLather... Yesterday's lather was at fault because I wasn't able to load as much soap.  But I corrected that today by loading with a bit less water in the brush.  I'd still say it was a very wet brush, just not as much as before.\n\nThe brush was able to pick up enough soap this time and it all worked out very well.\n\nIt made me feel good about recommending the slurry lather method to folks with high-density badgers.  I thought it might take some special tweaking with the method, based on my first tries. But all it took was making sure the brush picked up enough soap, by not have quite so much water in the knot.\n\nHydration: Perfect *(for me)*\n\n+ 13 sec load with a Very Wet brush\n+ = 5 passes of lather\n\nBowl: No Bowl  \n\n#### \u4dc0 Brush Notes\n*^(Declaration Grooming - B13 Dogwood/Briar Hybrid 28mm \u203922 uses\u203a)*\n\nSlurry lather doesn't give as much time to enjoy the brush, but it was as nice as usual.  I was wrong when I thought this brush would not hold enough water. I did shake out a little more than last time, but it was still plenty to get the job done.\n\n----\n*During the Shave Feel*:  \n&nbsp; *Cheeks*: Very irritating  \n&nbsp; *Neck*: Very irritating  \n*After the Shave Closeness*:  \n&nbsp; *Cheeks*: Close Shave  \n&nbsp; *Neck*: Several hairs are showing some tip length (still a pretty good shave)  \n\n----\n\n**Shavers Map** - [here it is](http://www.freezingcode.com/shaving/shaversMap.cfm) *and also in the sub's sidebar.*\n\n**Ending of Blades Ledger** - [entry form](https://docs.google.com/forms/d/e/1FAIpQLSdYqXSDujvoO1hVl_wSKMeETWdxFnYJCrqr0zU7FStBdIMrfg/viewform) and [the data spreadsheet](https://docs.google.com/spreadsheets/d/1y-oqIPSHKcb0EYd9OxL2n-R4Y6yxqid6-NGYS_4_ljU/edit?usp=sharing)",
            },
            "expected_result": "Weck - Sextoblade",
            "expected_result_principal": "Weck Sextoblade",
        },
    ]

    def test_get_razor_name_cases(self):
        rn = RazorNameExtractor()
        for case in self.razor_name_cases:
            r_name = rn.get_name(case["comment"])
            self.assertEqual(case["expected_result"], r_name)

    def test_get_principal_name_cases(self):
        rn = RazorNameExtractor()
        rp = RazorParser()
        r_aname = None
        for case in self.razor_name_cases:
            r_name = rn.get_name(case["comment"])
            if r_name:
                r_aname = rp.get_value(r_name, "name")
                self.assertEqual(case["expected_result_principal"], r_aname)


if __name__ == "__main__":
    rne = TestRazorNameExtractor()
    rne.test_get_principal_name_cases()
