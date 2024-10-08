from unittest import TestCase
from razor_parser import RazorParser

from sotd_collator.razor_name_extractor import RazorNameExtractor


class TestRazorNameExtractor(TestCase):
    razor_name_cases = [
        #         {
        #             "comment": {
        #                 "body": """**[Feb. 21, 2020 - Forgotten Friday](https://i.imgur.com/AiXQGG1.jpg)**
        #                 * **Prep:** None
        #                 * **Brush:** Washington Blue Steel B6
        #                 * **Razor:** Karve CB (Plate C)
        #                 * **Blade:** Gillette Nacet (3)
        #                 * **Lather:** [Declaration Grooming - Sweet Lemon - Soap](https://trythatsoap.com/collection/70/?product_type=soap)
        #                 * **Post Shave:** [Declaration Grooming - Sweet Lemon - Aftershave](https://trythatsoap.com/collection/70/?product_type=aftershave)
        #                 Better late than never.""",
        #             },
        #             "expected_result": "Karve CB (Plate C)",
        #             "expected_result_principal": "Karve Christopher Bradley",
        #         },
        #         {
        #             "comment": {
        #                 "body": """***I Can't Stands No More : 2/28/20***
        #                 * **Brush** \- Maggard 24mm Synthetic
        #                 * **Razor** \- Maggard MR5 w/ V2 OC
        #                 * **Blade** \- Rapira (Fresh)
        #                 * **Lather** \- Barrister and Mann - Ravish
        #                 * **Post** \- Barrister and Mann - Ravish Splash
        #                 """,
        #             },
        #             "expected_result": "Maggard MR5 w/ V2 OC",
        #             "expected_result_principal": "Maggard V2",
        #         },
        #         {
        #             "comment": {
        #                 "body": """**// Brush** \- Dogwood Handcrafts - SHD
        #                 **// Razor** \- Maggard MR 5 w/ V2 OC
        #                 **// Blade** \- Voskhod (4)
        #                 **// Lather** \- Turtleship Shave Co. - Bay Rum
        #                 **// Post** \- Pinaud Clubman""",
        #             },
        #             "expected_result": "Maggard MR 5 w/ V2 OC",
        #             "expected_result_principal": "Maggard V2",
        #         },
        #         {
        #             "comment": {
        #                 "body": """* **Prep:** Cup of Coffee
        #                 * **Brush:** Sawdust Creations 26 mm Timberwolf
        #                 * **Razor:** [Chani](https://imgur.com/a/usfOaJp)
        #                 * **Lather:** [Summer Break Soaps - Bell Ringer - Soap](https://trythatsoap.com/collection/1183/?product_type=soap)
        #                 * **Post Shave:** [Summer Break Soaps - Bell Ringer - Aftershave](https://trythatsoap.com/collection/1183/?product_type=aftershave)
        #                 * **Post Shave:** Mod Cabin - Bare Essentials - Beard Oil
        #                 * **Fragrance:** Creed - Green Irish Tweed - Eau de Toilette
        #                 Stay safe and have a great day!""",
        #             },
        #             "expected_result": "Chani",
        #             "expected_result_principal": None,
        #         },
        #         {
        #             "comment": {
        #                 "body": """
        #                 **// Razor** \- GC 2.0
        #                 """,
        #             },
        #             "expected_result": "GC 2.0",
        #             "expected_result_principal": "Greencult GC 2.0",
        #         },
        #         {
        #             "comment": {
        #                 "body": """
        #                 **// Razor** \- Game Changer 68
        #                 """,
        #             },
        #             "expected_result": "Game Changer 68",
        #             "expected_result_principal": "RazoRock Game Changer",
        #         },
        #         {
        #             "comment": {
        #                 "body": """
        #                 **// Razor** \- GC
        #                 """,
        #             },
        #             "expected_result": "GC",
        #             "expected_result_principal": "RazoRock Game Changer",
        #         },
        #         {
        #             "comment": {
        #                 "body": """
        #                 **// Razor** \- Gamechanger 68
        #                 """,
        #             },
        #             "expected_result": "Gamechanger 68",
        #             "expected_result_principal": "RazoRock Game Changer",
        #         },
        #         {
        #             "comment": {
        #                 "body": """
        #                 [**SOTD 20231225 Maestri by IschiaPP @ Forio**](https://ischiapp.blogspot.com/2023/12/sotd-20231225.html)
        #                 * Pre: Oleolito LCC Olio Prebarba Medicato
        #                 Homemade by Dr IschiaPP
        #                 * Brush: Bat71 Cashmere
        #                 Olive Wood, Abalone Shell Inlay, Yaqi SK07 aka Maggard Beige, 24x50x115mm
        #                 * Soap: Frankincense Giardini La Mortella Foro Afeitado 2019 Exclusive IschiaPP
        #                 * Razor: Gillette Labs UK 2023 Exfoliating Razor Neon Night Edition FlexDisc #41
        #                 * After: Oleotintura LCC Trattamento Urto Dopobarba Medicato
        #                 Homemade by Dr IschiaPP
        #                 Full size: 1200x1200px
        #                 Soundtrack: Joe Hisaishi - Merry go Round of Life
        #                 from Howl's Moving Castle Miyazaki (by Grissini Project)
        #                 """,
        #             },
        #             "expected_result": "Gillette Labs UK 2023 Exfoliating Razor Neon Night Edition FlexDisc #41",
        #             "expected_result_principal": "Cartridge / Disposable" "",
        #         },
        #         {
        #             "comment": {
        #                 "author": "Enndeegee",
        #                 "body": """* razor: no name vintage Gillette old type clone (aggressive)
        #         * Brush: zenith red handle 27mm boar
        #         * Lather: barrister and Mann : reserve cool
        #         Format almost back to normal to help u/jimm262 but I realise my plethora of random shit like the various no name old type clones I own probably won't show up anyway.""",
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
        #             "comment": {
        #                 "author": "djundjila",
        #                 "body": """## [Smoke 'em if you got 'em](https://imgur.com/Cz9dzR6.jpeg)
        #         * **Prep:** Klar - Aktiv Kohle - activated charcoal facial soap
        #         * **Brush:** Djundjila Brushworks - Haverford #BICOLOR
        #         * **Razor:** Hensonford - Henson AL13 Mild aluminium head on Djundjila Razorworks Haverford zamac handle #FRANKENRAZOR
        #         * **Blade:**  RK - Stainless Double Edge Blades  o
        #         * **Lather:** [Moon Soaps - Havana - Soap](https://trythatsoap.com/collection/2262/?product_type=soap)
        #         * **Post Shave:** [Summer Break Soaps - Valedictorian - Aftershave](https://trythatsoap.com/collection/2312/?product_type=aftershave)
        #         * **Fragrance:** [Stirling Soap Co. - Haverford - Eau de Toilette](https://trythatsoap.com/collection/1450/?product_type=eaudetoilette)
        #         u/Newtothethis appreciation day! One year and almost three weeks ago, we were asked to lather on our cans, the implication being man cans. This was [rightfully criticised by](https://reddit.com/r/Wetshaving/comments/nuxr24/tuesday_lather_games_sotd_thread_jun_08_2021/h11cllx/?context=0) u/Newtothethis who promptly created today's challenge in these words:
        #         \"*Next year, y'all should lather on your knee as to simulate the inconvenience of lathering so far away from the region you are actually shaving.*\"
        #         I'd say mission accomplished, the inconvenience has been [adequately simulated](https://imgur.com/ySPgFfV.jpeg).
        #         I'll keep the shave description and #FOF-fery short because I had a beast of a day and I just want to go pass out in bed. For today's shave I followed my man u/Teufelskraft's lead and created an aluminum-zamac-clay hybrid #FRANKENRAZOR. This was my first try of Moon Soap's Havana soap. The base is much firmer than the one of Moon Soap's Union. I spread a good wad of soap on the bottom of my Captain's Choice heavy copper bowl and immediately the scent off it was intoxicating and delicious. It reminded me of HoM Tobacconist, that's how good it smells. I picked up the soap with a damp brush and lathered on my knee, as per instructions. The base is easy to dial in and I had three very comfy passes with the Hensonford frankenrazor. The Valedictorian splash is my favourite SBS scent to date and while tobacco-centric, it adds earthy, citrussy, sweet, smoky and woodsy notes. Simply a fantastic scent! I topped it all up with my secret/not-so-secret obsession, Haverford EdT. This sweet and gourmand fresh baked cookie scent will never not make me happy.
        #         **Stirling Soap**
        #         I can say only good things about Stirling. For instance, they have the best sample size in the business. Varen and Haverford are godly scents (I know that Haverford is a dupe), Boat Drinks makes me happy and Pharaoh's Dreamsicle makes my mouth water.
        #         * Themes fulfilled: 27/30
        #         * Hardware vendors: 4/2
        #         * Software sponsors: 12/15
        #         * Different soaps: 27/30
        #         * Different soap brands: 27/30
        #         * Post-shave products: 27/30
        #         * Different fragrances: 27/30
        #         * Hardware Scavenger Hunt Tags: 40/40
        #         * Additional Scavenger Hunt Tags: 14 (+ #FRANKENRAZOR)
        #         * Art of Wetshaving points: 27/30
        #         * Daily challenges completed: 27/30""",
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
        #             # test img link in razor
        #             "comment": {
        #                 "author": "djundjila",
        #                 "body": """## [Smoke 'em if you got 'em](https://imgur.com/Cz9dzR6.jpeg)
        #         * **Prep:** Klar - Aktiv Kohle - activated charcoal facial soap
        #         * **Brush:** Djundjila Brushworks - Haverford #BICOLOR
        #         * **Razor:** Hensonford - Henson AL13 Mild aluminium head on Djundjila Razorworks Haverford zamac handle #FRANKENRAZOR
        #         * **Blade:**  RK - Stainless Double Edge Blades  o
        #         * **Lather:** [Moon Soaps - Havana - Soap](https://trythatsoap.com/collection/2262/?product_type=soap)
        #         * **Post Shave:** [Summer Break Soaps - Valedictorian - Aftershave](https://trythatsoap.com/collection/2312/?product_type=aftershave)
        #         * **Fragrance:** [Stirling Soap Co. - Haverford - Eau de Toilette](https://trythatsoap.com/collection/1450/?product_type=eaudetoilette)
        #         u/Newtothethis appreciation day! One year and almost three weeks ago, we were asked to lather on our cans, the implication being man cans. This was [rightfully criticised by](https://reddit.com/r/Wetshaving/comments/nuxr24/tuesday_lather_games_sotd_thread_jun_08_2021/h11cllx/?context=0) u/Newtothethis who promptly created today's challenge in these words:
        #         \"*Next year, y'all should lather on your knee as to simulate the inconvenience of lathering so far away from the region you are actually shaving.*\"
        #         I'd say mission accomplished, the inconvenience has been [adequately simulated](https://imgur.com/ySPgFfV.jpeg).
        #         I'll keep the shave description and #FOF-fery short because I had a beast of a day and I just want to go pass out in bed. For today's shave I followed my man u/Teufelskraft's lead and created an aluminum-zamac-clay hybrid #FRANKENRAZOR. This was my first try of Moon Soap's Havana soap. The base is much firmer than the one of Moon Soap's Union. I spread a good wad of soap on the bottom of my Captain's Choice heavy copper bowl and immediately the scent off it was intoxicating and delicious. It reminded me of HoM Tobacconist, that's how good it smells. I picked up the soap with a damp brush and lathered on my knee, as per instructions. The base is easy to dial in and I had three very comfy passes with the Hensonford frankenrazor. The Valedictorian splash is my favourite SBS scent to date and while tobacco-centric, it adds earthy, citrussy, sweet, smoky and woodsy notes. Simply a fantastic scent! I topped it all up with my secret/not-so-secret obsession, Haverford EdT. This sweet and gourmand fresh baked cookie scent will never not make me happy.
        #         **Stirling Soap**
        #         I can say only good things about Stirling. For instance, they have the best sample size in the business. Varen and Haverford are godly scents (I know that Haverford is a dupe), Boat Drinks makes me happy and Pharaoh's Dreamsicle makes my mouth water.
        #         * Themes fulfilled: 27/30
        #         * Hardware vendors: 4/2
        #         * Software sponsors: 12/15
        #         * Different soaps: 27/30
        #         * Different soap brands: 27/30
        #         * Post-shave products: 27/30
        #         * Different fragrances: 27/30
        #         * Hardware Scavenger Hunt Tags: 40/40
        #         * Additional Scavenger Hunt Tags: 14 (+ #FRANKENRAZOR)
        #         * Art of Wetshaving points: 27/30
        #         * Daily challenges completed: 27/30""",
        #                 "created_utc": "2022-06-27 20:12:47",
        #                 "id": "idzsde8",
        #                 "url": "https://www.reddit.com/r/Wetshaving/comments/vloh9w/comment/idzsde8/",
        #                 "razor": "[Hensonford - Henson AL13 Mild aluminium head on Djundjila Razorworks Haverford zamac handle #FRANKENRAZOR](https://imgur.com/Cz9dzR6.jpeg)",
        #                 "blade": "RK - Stainless Double Edge Blades  o",
        #                 "brush": "Djundjila Brushworks - Haverford #BICOLOR",
        #             },
        #             "expected_result": "[Hensonford - Henson AL13 Mild aluminium head on Djundjila Razorworks Haverford zamac handle #FRANKENRAZOR](https://imgur.com/Cz9dzR6.jpeg)",
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
        #         {
        #             "comment": {
        #                 "body": """*Prep:* Splash of Cool Water
        #         *Razor:* **Weck - Sextoblade**
        #         *Blade:* **Kismet - Hair Shaper** (1)
        #         *Lather:* **Summer Break Soaps** - **Remote Learning**
        #         *Brush:* **Declaration Grooming - B13** Dogwood/Briar Hybrid 28mm (22 uses)
        #         *Post Shave:* Pre de Provence - No. 63
        #         ----
        #         [Gear Pic](https://i.imgur.com/zyG7MHU.jpg) :: [Video](https://youtu.be/LQWF4SJ9t48)
        #         #### \u4dc0 General Notes
        #         My first try with a Weck and the hair shaper blades as well. I also get a good slurry lather with a high-density badger by changing the water amount.
        #         Thanks /u/gcgallant for the Weck and blades and tips and all!!!!
        #         And Greg... I just realized that I've been pronouncing your last name, like a fop, with the accent on the last syllable. Maybe I had some kind of international impression on my brain when we first started communicating or something. If you pronounce it with the emphasis on the first, then I'm sorry (and I bet you've been chuckling to yourself for a while now).
        #         #### \u4dc0 Razor and Blade Notes
        #         *^(Weck - Sextoblade ::: Kismet - Hair Shaper \u20391 uses\u203a)*
        #         Well, I did get cut in 4-5 places.  But those were just mistakes on my part, since I don't have great straight technique yet.
        #         By the end of the shave, all but one of the cuts had sealed up, and the last one turned from a bleeder to a very slow weeper.
        #         The Weck and the Kismet definitely take some practice, and I think are less forgiving than the 3 straights I've tried so far. However, I saw in some forums that after one or two shaves, the Kismet might smooth out a little.
        #         I did feel a general irritation at the end of the shave, after the final rinse.  But, I put on a decent balm, and all the tenderness and raw-ness went away, even before I left the bathroom. Looking back at that, I was very surprised.
        #         But I got a close shave on my cheeks, and my neck was done pretty well too.  I didn't do a third pass, because of the irritation, and I didn't pursue every little bit of stubble on my neck, but I think my result was respectable.
        #         Razor and Blade Performance/Comfort Rating: 1 out of 5 (Poor)
        #         #### \u4dc0 Soap Notes
        #         *^(Summer Break Soaps - Remote Learning)*
        #         Them: Doritos
        #         Scent: nacho cheesy corn tortilla chips is the goal here.  I imagine that's a tough challenge.  While smelling the dry tub and the wet lather, what comes to me first is a cookie sweet type scent that reminds me of some cinnamon schoolbook cookies from Trader Joes.  It's a nice scent, so I don't mind if my  brain never switches away from that.
        #         If I know it is supposed to be corn chips, then I can definitely see that in the scent.  So that's cool.
        #         But even if I set my brain to try to find a cheesy note in there, I really can't.
        #         I think it might be more realistic with a hint-of-cumin type scent in there, but of course, that could make it hard on skin maybe.
        #         While I may not really get a Doritos scent from it, I think it's a great attempt, and I know that I like shaving with it anyway.
        #         Scent Strength: 4/10, present during shaving.
        #         Lather... Yesterday's lather was at fault because I wasn't able to load as much soap.  But I corrected that today by loading with a bit less water in the brush.  I'd still say it was a very wet brush, just not as much as before.
        #         The brush was able to pick up enough soap this time and it all worked out very well.
        #         It made me feel good about recommending the slurry lather method to folks with high-density badgers.  I thought it might take some special tweaking with the method, based on my first tries. But all it took was making sure the brush picked up enough soap, by not have quite so much water in the knot.
        #         Hydration: Perfect *(for me)*
        #         + 13 sec load with a Very Wet brush
        #         + = 5 passes of lather
        #         Bowl: No Bowl
        #         #### \u4dc0 Brush Notes
        #         *^(Declaration Grooming - B13 Dogwood/Briar Hybrid 28mm \u203922 uses\u203a)*
        #         Slurry lather doesn't give as much time to enjoy the brush, but it was as nice as usual.  I was wrong when I thought this brush would not hold enough water. I did shake out a little more than last time, but it was still plenty to get the job done.
        #         ----
        #         *During the Shave Feel*:
        #         &nbsp; *Cheeks*: Very irritating
        #         &nbsp; *Neck*: Very irritating
        #         *After the Shave Closeness*:
        #         &nbsp; *Cheeks*: Close Shave
        #         &nbsp; *Neck*: Several hairs are showing some tip length (still a pretty good shave)
        #         ----
        #         **Shavers Map** - [here it is](http://www.freezingcode.com/shaving/shaversMap.cfm) *and also in the sub's sidebar.*
        #         **Ending of Blades Ledger** - [entry form](https://docs.google.com/forms/d/e/1FAIpQLSdYqXSDujvoO1hVl_wSKMeETWdxFnYJCrqr0zU7FStBdIMrfg/viewform) and [the data spreadsheet](https://docs.google.com/spreadsheets/d/1y-oqIPSHKcb0EYd9OxL2n-R4Y6yxqid6-NGYS_4_ljU/edit?usp=sharing)""",
        #             },
        #             "expected_result": "Weck - Sextoblade",
        #             "expected_result_principal": "Weck Sextoblade",
        #         },
        #         {
        #             "comment": {
        #                 "body": """Trying to add in the detail required
        #  * Brush: yes
        # * Brush brand: Zenith
        # * Brush model: 80R
        #  * Brush colour: red
        # * Brush knot diameter: 27mm
        # * Brush hair length: 60mm
        # * Brush hair: boar bristle
        # * Brush hair treatment: bleached
        # * Brush preparation technique: wet bristles and then leave to stand while I get shit ready
        # * Razor: yes
        # * Razor brand: Gillette
        # * Razor model: rocket HD
        # * Razor material: plated brass
        # * Razor base plate style: safety bar
        # * Razor blade type: double edge
        # * Blade brand Gillette
        # * Blade model: London bridge
        # * Blade coating; none
        #  * Blade usage count: 1
        #  * Lather: yes
        # * shavinginct lather super category: other soap
        # * Lather medium: soap
        #  * Lather storage vessel: tub
        # * Lather method: face
        # * Lather brand: Wickham soaps
        #  * Lather base: unspecified vegan
        # * Lather name: Gothic Revival
        # * Lather scent notes: eucris dupe
        #  * Alum: no
        # * OSMA alum: no
        # * Aftershave care: yes
        # * Aftershave type: cream/lotion
        # * Aftershave brand: aveeno
        # * Aftershave name: sensitive baby cream
        # * Aftershave scent: unscented
        # * Fragrance: none""",
        #             },
        #             "expected_result": "Gillette rocket HD",
        #             "expected_result_principal": "Gillette Super Speed",
        #         },
        #         {
        #             "comment": {
        #                 "body": "* **Razor:** [Charcoal Goods Level 2 with Stinger Handle](https://imgur.com/a/Y8xahOa)"
        #             },
        #             "expected_result": "Charcoal Goods Level 2 with Stinger Handle",
        #             "expected_result_principal": "Charcoal Goods Level 2",
        #         },
        #         {
        #             "comment": {
        #                 "body": """**February 4, 2024**
        # * **Brush:** Maggard 24mm G5 Synthetic
        # * **Razor:** Blackland Era - Level 3 SB
        # * **Blade:** Bolzano Superinox (German) (3)
        # * **Lather:** Spearhead Shaving - Seaforth! Heather - Soap
        # * **Post Shave:** Brut - Splash On
        # * **Post Shave:** House of Mammoth/Declaration Grooming - Cerberus - Liniment
        # Tub kill! u/VisceralWatch"""
        #             },
        #             "expected_result": "Blackland Era - Level 3 SB",
        #             "expected_result_principal": "Blackland Era",
        #         },
        #         {
        #             "comment": {
        #                 "body": r"**Razor:** Blackland - [Blackbird, DE safety razor, Brass, 101 mm handle](https://imgur.com/40xVJdM) \- \"Brassbird\""
        #             },
        #             "expected_result": r"Blackland - Blackbird, DE safety razor, Brass, 101 mm handle \- \"Brassbird\"",
        #             "expected_result_principal": "Blackland Era",
        #         },
        #         {
        #             "comment": {"body": "Razorock is my favorite brand"},
        #             "expected_result": None,
        #             "expected_result_principal": None,
        #         },
        #         {
        #             "comment": {
        #                 "body": """*Razor*: Blackland - **Dart** (Machined)
        # *Blade*: **Gillette - Nacet** (4)
        # *Lather*: **Williams Mug Soap**
        # *Brush*: Whipped Dog - **Boar** (7th use)
        # *Post*: Afta - Fresh
        # ----
        # **Razor and Blade Notes**  another very close shave with no irritation.
        # *Cheek Feel During Shave*: Smooth
        # *Neck Feel During Shave*: Felt blade but comfortable
        # *Cheek Closeness After Shave*: Near BBS - About as close as I'll ever get
        # *Neck Closeness After Shave*: Cut flush to where I just see the tips (above average for me)
        # **Soap Notes**
        # 1 min load w/ .5 tsp wtr fm start = lather perhaps right on target if not justa bit thick. This gave me a lather that was drier (than yesterday's) on first pass and perfect by 3rd.  and I ended up wtih too much lather.  Will try 45s load next time with same 2tsp water.
        # Scent strength 3-4/10.
        # Slick as usual and very protective!  Only thing missing was more cushion/luxury.
        # Past attempts:
        # * 1 min of loading and 2.5 tsp of water was a little to thin.
        # """
        #             },
        #             "expected_result": "Blackland - **Dart** (Machined)",
        #             "expected_result_principal": "Blackland Dart",
        #         },
        # {
        #     "comment": {"body": "* **Razor:** Gillette - Flare Tip Super Speed 1950’s"},
        #     "expected_result": "Gillette - Flare Tip Super Speed 1950\u2019s",
        #     "expected_result_principal": "Gillette Super Speed",
        # },
        # {
        #     "comment": {
        #         "body": """**June 16, 2024** - **[Father\u2019s Day](https://imgur.com/a/qA0WDPw)**
        # * **Brush:**  Stirling - Synthetic 24mm
        # * **Razor:** Gillette - Flare Tip Super Speed 1950\u2019s
        # * **Blade:** Gillette - Super Blues
        # * **Lather:** Gillette - Shave Gel Island Breeze
        # * **Post Shave:** Brut - Signature Scent Splash
        # * **Fragrance** Brut - Signature Scent Cologne
        # **SOAP** - Gillette is old! [Like super old!](https://media4.giphy.com/media/EB3EJiPHzIP8k/giphy.gif?cid=6c09b9529x68w2lb9obnfkd25jebnj9ft4n6c8mhue4yq70f&ep=v1_internal_gif_by_id&rid=giphy.gif&ct=g)
        # So does that makes their shaving gel any good? [FAT NOOPE!](https://media0.giphy.com/media/JtLrtaN4VPoKXJRKGB/giphy.gif?cid=6c09b952unvruchp7cltj0w517dignv23kzljg95cskpgggx&ep=v1_internal_gif_by_id&rid=giphy.gif&ct=g)
        # It\u2019s awful and then some. I mean there is no hydrating your skin with a foamy gel filled with chemicals. But the brand label is old and today OLD is Theme! So I am pairing the rest of my set with old like Brut which is what my father used to use! What does it smell like? Well it smells like the color!!! Green. I don\u2019t think you could make anything that would literally smell like a color and they nailed it. [Green and old](https://media1.giphy.com/media/zwKkpZMJJ802k/giphy.gif?cid=6c09b95288id89vcef1bf1ld95vdewairzsc3ply78ps02l7&ep=v1_internal_gif_by_id&rid=giphy.gif&ct=g).
        # **RAZOR** - Another oldie from the 1950\u2019s TTO. Shaves like a hot knife on butter.. [clean as a whistle\u2026.](https://media4.giphy.com/media/NAj3Mh9ISQ2Ff9oBZO/giphy.gif?cid=6c09b952xl16rcm278ax9r4qify192k7hkxr4mqqjue9de8w&ep=v1_internal_gif_by_id&rid=giphy.gif&ct=g)
        # **THE THEME** - Why leg day on FATHER\u2019s DAY?? Why??? Well this is not my first rodeo but right when it\u2019s hot and sticky and humid! Okay pre shave and I set [myself up HERE](https://imgur.com/a/wtK6muM)!
        # And went to work. I wear my shorts low so not a big deal there. Thank goodness this was a one man show cause let\u2019s say if we had to shave our backs then another person would have to get involved and logistics would be tricky. HINT\u2026HINT\u2026 maybe next year who knows. [FINAL RESULT](https://imgur.com/a/cLkYjpF)!!
        # Yeah that was not fun. Razor kept getting clogged and took forever. Okay ready for the day so my kids can make fun of me all day for shaving my legs! Happy freaking Father\u2019s Day!
        # """
        #     },
        #     "expected_result": "Gillette - Flare Tip Super Speed 1950\u2019s",
        #     "expected_result_principal": "Gillette Super Speed",
        # },
        # {
        #     "comment": {
        #         "body": """**June 16, 2024** - **[Father\u2019s Day](https://imgur.com/a/qA0WDPw)**
        # * **Brush:**  Stirling - Synthetic 24mm
        # * **Razor:** Gillette - Flare Tip Super Speed 1950\u2019s
        # * **Blade:** Gillette - Super Blues
        # * **Lather:** Gillette - Shave Gel Island Breeze
        # * **Post Shave:** Brut - Signature Scent Splash
        # * **Fragrance** Brut - Signature Scent Cologne
        # """
        #     },
        #     "expected_result": "Gillette - Flare Tip Super Speed 1950\u2019s",
        #     "expected_result_principal": "Gillette Super Speed",
        # },
        #         {
        #             "comment": {
        #                 "body": """**June 1, 2024**
        # **\u2022 Brush:** Aurora Grooming LG24 Synthetic (\"Lux Emerald Green\")  #SUBBROOSH
        # **\u2022 Razor:**\u00a0Shumate Trusty (w/ orange scales, orange tang)  #RAINBOW  #RUSTYBUTTRUSTY
        # **\u2022 Lather:**\u00a0AA Shaving - Wapiti (smush courtesy of u/OnionMiasma!)
        # **\u2022 Post Shave:** Wholly Kaw - Ikigai
        # **\u2022 Fragrance:** Atelier Cologne - Bergemote Soleil
        # *\"Got me a movie, I want you to know...\"*
        # Losing your virginity can be awkward and fumbling. At least that's been my experience. This is my first Lather Games. It's also, because of the Daily Challenge, my first ever attempt to shave with a straight razor. The Shumate was purchased used (and ostensibly shave-ready) on Ebay. It didn't seem to pass the \"hair test,\" and after several minutes of careful stropping I went into the shave apprehensive.
        # In the end I'm proud of myself. Despite struggling with the angle of the blade, I managed to cleanly shave the flatter, accessible parts of my face\u2014sideburns and cheeks\u2014with only one nick, before bailing when I got to the jawline and chin. Too precarious for the time being. Whenever the blade was near the upper part of the face, near the eye sockets, I found myself thinking of the film *Un Chien Andalou*.
        # Lather, Post Shave, and Fragrance items were all used by me for the first time. Wapiti has a wonderful misty, atmospheric vibe, but also a note I can't quite place (like a more pleasant version of chlorine?) With Ikigai I get vanilla and musk more than any other notes.
        # **Brush Strokes** is a SOTD coda wherein I highlight a single work of art that, somehow or other, I perceive to be on-theme. Today's work is Tintoretto's [Presentation of the Virgin](https://imgur.com/a/TcLkDKW)*,* which hangs in the church of Madonna dell'Orto in Venice. It's a striking image that seems at once grounded and immediate, while also affording a distinct sensation of ascent, or possibly transcendence.
        # #ROTY
        # """
        #             },
        #             "expected_result": "Shumate Trusty",
        #             "expected_result_principal": "Shumate Trusty (w/ orange scales, orange tang)  #RAINBOW  #RUSTYBUTTRUSTY",
        #         },
        {
            "comment": {
                "body": """**August 31, 2024 \u2013 AA Mammoth Month**

\u2022\t\u2060**Brush**: r/wetshaving Zentih MOAR BOAR 31mm  
\u2022\t\u2060**Razor**: Blackland SS Osprey  
\u2022\t\u2060**Blade**: Personna Lab Blue (33)  
\u2022\t\u2060**Lather**: House of Mammoth \u2013 Sonder  
\u2022\t\u2060**Post Shave**: House of Mammoth \u2013 Sonder  
\u2022\t\u2060**Fragrance**: DR Harris \u2013 St James\u2019s 1684

[Ending point of the tubs](https://imgur.com/a/MFn08IB). Used 21g of soap for an average of ~.68 per shave, up from my midpoint and an increase of about .3 relative to beginning of month and last years AA. Balm used 9 grams so about .29g for the month, slightly down from the .35 in the first half. What a cool razor. I tweaked the setting a couple times in the monthly but am thinking 3-7 range is optimal for me. Haven\u2019t taken the brass insert out at all to see how that affects it. 3 piece adjustable is for sure unique. 

$MammothMonth24
"""
            },
            "expected_result": "Blackland SS Osprey",
            "expected_result_principal": "Blackland Osprey",
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
    rne.test_get_razor_name_cases()
    rne.test_get_principal_name_cases()
