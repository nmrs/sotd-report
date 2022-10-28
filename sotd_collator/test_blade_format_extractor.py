from unittest import TestCase


from blade_format_extractor import BladeFormatExtractor


class TestBladeFormatExtractor(TestCase):

    blade_format_cases = [
        {'comment': """- **Prep:** Chiseled Face Midnight Stag bar soap  and cold water  
- **Brush:** Tadé NOS vintage boar 22 mm  
- **Razor:** KAI Captain Standard CAP-J7 kamisori shavette  
- **Blade:** KAI Captain Titan Mild Protouch MG  
- **Lather:** Chiseled Face - *Midnight Stag* - shaving soap  
- **Post-Shave:** Chiseled Face - *Midnight Stag* - Aftershave  
- **additional care:** Chiseled Face - *Midnight Stag* - ASB  
- **Fragrance:** Southern Witchcrafts - *Valley of Ashes* - EDP  
- AA tags: #RawHoggin  #SubstantialStag  """,
         'expected_result': 'AC',
         },

    ]


    def test_get_razor_name_cases(self):
        bfe = BladeFormatExtractor()
        for case in self.blade_format_cases:
            bf = bfe.get_name(case['comment'])
            self.assertEqual(case['expected_result'], bf)
