from unittest import TestCase


from blade_format_extractor import BladeFormatExtractor


class TestBladeFormatExtractor(TestCase):
    # {
    #     "author": "Quadricwan",
    #     "body": "[Little Blue finds a home](http://imgur.com/SOJuNYv)  \n\n-Soap: 42  \n-Brush: Little Blue (26mm Envy White)  \n-Blade: Personna Lab Blue  \n-Razor: ATT Atlas S1  \n-Post: 42  \n\n\nAfter putzing around at the border for nearly two weeks, this fine little brush from u/praise_the_fireborn finally arrived,  just in time for the June soapstravaganza.  \n\nSo excited to get an Envy White here to Canada, and it doesn't disappoint. The only comparable Badger I've used was a much pricier Kent I traded away because it wasn't worth the coin. This is much nicer - soft,  dense, and lathers wonderfully. I've another small Badger on the way,  looking forward to seeing how they compare.  \n\nWish I could say the whole shave was great. Sadly,  these Personna blades seem to fall into the growing crowd of popular blades that don't agree with me. Lots of post shave irritation. ",
    #     "created_utc": "2016-05-31 04:52:31",
    #     "id": "d3q7gek",
    #     "url": "https://www.reddit.com/r/Wetshaving/comments/4lu5sx/comment/d3q7gek/"
    # },


    blade_format_cases = [
        {
            'comment': 
            {
                'body': """
- **Prep:** Chiseled Face Midnight Stag bar soap  and cold water  
- **Brush:** Tadé NOS vintage boar 22 mm  
- **Razor:** KAI Captain Standard CAP-J7 kamisori shavette  
- **Blade:** KAI Captain Titan Mild Protouch MG  
- **Lather:** Chiseled Face - *Midnight Stag* - shaving soap  
- **Post-Shave:** Chiseled Face - *Midnight Stag* - Aftershave  
- **additional care:** Chiseled Face - *Midnight Stag* - ASB  
- **Fragrance:** Southern Witchcrafts - *Valley of Ashes* - EDP  
- AA tags: #RawHoggin  #SubstantialStag  
""",
            },
            'expected_result': 'AC',
        }
    ]


    def test_get_razor_name_cases(self):
        bfe = BladeFormatExtractor()
        for case in self.blade_format_cases:
            bf = bfe.get_name(case["comment"])
            self.assertEqual(case['expected_result'], bf)
