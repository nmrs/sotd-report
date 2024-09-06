from unittest import TestCase
from soap_parser import SoapParser

from sotd_collator.soap_name_extractor import SoapNameExtractor


class TestSoapNameExtractor(TestCase):
    test_cases = [
        {
            "comment": {
                "body": """**SOTD Aug. 14, 2024**
        * **Prep** : Warm shower
        * **Brush**: Frank Shaving 24mm G7 synthetic
        * **Razor**: RazoRock Game Changer .84-P
        * **Blade**: Gillette Silver Blue (2)
        * **Lather**: Face
        * **Lather**: BM Cheshire
        * **Post Shave**: Thayers Rose Petal + Tend Skin
        * **Post Shave**: Pink Woolf Oudh and Sandalwood Aftershave Balm
        """
            },
            "expected_result": "BM Cheshire",
        },
        {
            "comment": {
                "body": """* **Prep:** Splash of Cool Water  
* **Razor:** Timeless - Stainless Steel .68 - Open Comb  
* **Blade:** Gillette - Nacet (Marathon) (565)  
* **Lather:** Chiseled Face - Midnight Stag (2024a)  
* **Brush:** Declaration Grooming - B13 Dogwood/Briar Hybrid 28mm (42 uses)  
* **Post Shave:** Chiseled Face - Midnight Stag (White Label)  
* **Fragrance:** Chiseled Face - Midnight Stag  

----

**Austere August: Day: 21**  
*Sgrdddy's Ultra Nightmare Mode*  
*Midnight Stag Challenge* $SubstantialStag  

[Gear Pic](https://i.imgur.com/nE6X6nl.jpeg) :: [Video](https://youtu.be/VcCHkHxBgRY)

#### \u4dc0 General Notes  
Quick bowl lather today

#### \u4dc0 Razor and Blade Notes
*^(Timeless - Stainless Steel .68 - Open Comb ::: Gillette - Nacet - M \u2039565 uses\u203a)*

Same: First pass has some tugginess to it.  But no irritation that lasts longer than a little tuggy stroke.  Latter passes feel fine and give a reasonably close shave. 3 pretty quick passes.

stopped shorter than usual, because needed to be quick.

#### \u4dc0 Soap Notes
*^(Chiseled Face - Midnight Stag - 2024a)*



I just love all the aspects of this scent!

Scent Strength: 6/10, nicely present during shaving.

Lather... 10 swirl load was plenty for the passes I need

simple bowl lather 

It was a bit airy on pass one, so I had to add some water.

Hydration: Perfect *(for me)*

Bowl: [Roger Quintero 3D Printed Bowl](https://www.thingiverse.com/thing:3392930)  
I use the XL version of this bowl.

#### \u4dc0 Brush Notes
*^(Declaration Grooming - B13 Dogwood/Briar Hybrid 28mm \u203942 uses\u203a)*

Soft and comfy as usual

----
*During the Shave Feel*:  
&nbsp; *Cheeks*: Just a little tugging  
&nbsp; *Neck*: Just a little tugging  
*After the Shave Closeness*:  
&nbsp; *Cheeks*: Close Shave  
&nbsp; *Neck*: Several hairs are showing some tip length (still a pretty good shave)  

----

**Shavers Map** - [here it is](http://www.freezingcode.com/shaving/shaversMap.cfm) *and also in the sub's sidebar.*

**Ending of Blades Ledger** - [entry form](https://docs.google.com/forms/d/e/1FAIpQLSdYqXSDujvoO1hVl_wSKMeETWdxFnYJCrqr0zU7FStBdIMrfg/viewform) and [the data spreadsheet](https://docs.google.com/spreadsheets/d/1y-oqIPSHKcb0EYd9OxL2n-R4Y6yxqid6-NGYS_4_ljU/edit?usp=sharing)
"""
            },
            "expected_result": "Chiseled Face - Midnight Stag (2024a)",
        },
    ]

    def test_get_soap_name_cases(self):
        sn = SoapNameExtractor()
        for case in self.test_cases:
            s_name = sn.get_name(case["comment"])
            self.assertEqual(case["expected_result"], s_name)


if __name__ == "__main__":
    sne = TestSoapNameExtractor()
    sne.test_get_soap_name_cases()
