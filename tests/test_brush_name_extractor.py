from unittest import TestCase
from brush_name_extractor import BrushNameExtractor
from razor_parser import RazorParser

from sotd_collator.razor_name_extractor import RazorNameExtractor


class TestBrushNameExtractor(TestCase):
    test_cases = [
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
            "comment": {
                "body": """*Razor*: Blackland - **Dart** (Machined)  
*Blade*: **Gillette - Nacet** (19)  
*Lather*: **Williams Mug Soap**  
*Brush*: **Whipped Dog - Boar** 24mm  
*Post*: Afta - Fresh  

----

**Ultra Nightmare Mode**

[Video](https://youtu.be/F_lmuUAVHKE)  

**General Notes / Exec Summary / TL;DR**  
Apparently 60 secs of loading is too short for a soak of only a few mins.  Lather too thin, giving a rough shave.

**Razor and Blade Notes**  
blade and razor seem fine, but shave was rough ... probably due to thin lather.  However, no irritation after shave.

*During the Shave Feel*:  
&nbsp; *Cheeks*: A little irritating  
&nbsp; *Neck*: A little irritating  

*After the Shave Closeness*:  
&nbsp; *Cheeks*: Very Close Shave  
&nbsp; *Neck*: Few hairs are showing some tip length (with most being cut flush)  

**Soap Notes**  
First and second pass too thin.  3rd was better.

For today's face-lather, I bloomed soap (cool water) with 2 tsp water for just a few mins as I prepped for the shave, 60 sec load with barely-damp brush.   This gave me enough soap to go all three passes.  Lather was thin and airy on the first and second passes, but was doable, though I didn't like it ... was rough.   However, the third pass was almost a slick, creamy lather.  

Because I'd like to nail down a good face lather, I think next I will keep the same short bloom (which is more convenient) and load for longer, maybe 90 secs.  

Scent strength  
&nbsp;Day 1-2: 3-4/10  
&nbsp;Day 4-5: 2-3/10  
&nbsp;Day 6-7: 2/10  
&nbsp;Day 8-10: 1/10  
&nbsp;Day 11-~: 0/10 (can't smell it any more while lathering)

Best Lathers So Far:

* Bloomed soap (cool water) for 26 mins, 30 sec load with barely damp brush, then ended up adding to a total of 2 tsp water.  Looked more like other soaps this time as it became more elastic and hydrated.  Had a little cushion, bubbles were very minimal, and was well-slick.


**Brush Notes**  
tips slow to split, but still comfy while I wait.

----

**Ending of Blades Ledger**

Use this to document how long our blades last for this month, and what about them made us pitch 'em.  I created a Google Form with just a few questions, if anyone is interested:

[Ending of Blades Ledger](https://docs.google.com/forms/d/e/1FAIpQLSdYqXSDujvoO1hVl_wSKMeETWdxFnYJCrqr0zU7FStBdIMrfg/viewform)

I'll keep this as my footer each day so you have the link.  I'll take it down if no one shows interest.

""",
            },
            "expected_result": "Whipped Dog - Boar** 24mm",
        },
    ]

    def test_get_brush_name_cases(self):
        rn = BrushNameExtractor()
        for case in self.test_cases:
            r_name = rn.get_name(case["comment"])
            self.assertEqual(case["expected_result"], r_name)


if __name__ == "__main__":
    rne = TestBrushNameExtractor()
    rne.test_get_brush_name_cases()
