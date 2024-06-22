from functools import cached_property, lru_cache
import os
import re
import yaml

from base_parser import BaseParser


class SoapParser(BaseParser):
    """
    Amalgamate names
    """

    _raw = {
        # "345 Soap Co.": {"patterns": ["345"], "scents": {}},
        # "Ariana & Evans": {
        #     "patterns": [r"\ba ?(and|&|\+) ?e\b", r"arian+a.*evan"],
        #     "scents": {
        #         "Kaizen": {"patterns": [r"\bkaizen\b"]},
        #     },
        # },
        # "Arko": {"patterns": [r"\barko\b"], "scents": {}},
        # "Arsenal Grooming": {"patterns": [r"arsenal grooming"], "scents": {}},
        # "Art of Shaving": {
        #     "patterns": [r"art of shaving"],
        #     "scents": {
        #         "Oud": {"patterns": [r"art of shaving.*\boud\b"]},
        #     },
        # },
        # "Asylum Shave Works": {
        #     "patterns": ["asylum shave works", r"\basw\b"],
        #     "scents": {},
        # },
        # "Australian Private Reserve": {
        #     "patterns": [r"\bapr\b", "australian private reserve"],
        #     "scents": {},
        # },
        # "Abbate Y La Mantia": {
        #     "patterns": [r"\baylm\b", r"abbate y la mantia"],
        #     "scents": {},
        # },
        # "Ach Brito": {
        #     "patterns": [r"\bach.*brito\b"],
        #     "scents": {
        #         "Lavanda": {
        #             "patterns": [r"\bach.*brito\b.*lavanda"],
        #             "format": "Cream",
        #         }
        #     },
        # },
        # "Ballenclaugh": {"patterns": [r"ballenclaugh"], "scents": {}},
        # "Barrister and Mann": {
        #     "patterns": [r"\bb ?(and|&|\+) ?m\b", r"barrister (and|\+|&) mann"],
        #     "scents": {
        #         "42": {"patterns": [r"\bb ?(and|&|\+) ?m\b.*42", "barris.*42"]},
        #         "Bay Rum": {
        #             "patterns": [r"\bb ?(and|&|\+) ?m\b.*bay rum", "barris.*bay rum"]
        #         },
        #         "Beaudelaire": {
        #             "patterns": [r"\bb ?(and|&|\+) ?m\b.*be?audel", "barris.*be?audel"]
        #         },
        #         "Braeburn": {"patterns": ["braeburn"]},
        #         "Behold the Whatsis!": {"patterns": [r"\bwhatsis\b"]},
        #         "Cheshire": {
        #             "patterns": [r"\bb ?(and|&|\+) ?m\b.*cheshire", "barris.*cheshire"]
        #         },
        #         "Fern": {"patterns": [r"\bb ?(and|&|\+) ?m\b.*fern", "barris.*fern"]},
        #         "Lavender": {
        #             "patterns": [r"\bb ?(and|&|\+) ?m\b.*lavender", "barris.*lavender"]
        #         },
        #         "Le Grand Chypre": {"patterns": ["grand chyp", "grand cyph"]},
        #         "Le Petit Chypre": {"patterns": ["petite? chyp"]},
        #         "Lyssa": {
        #             "patterns": [r"\bb ?(and|&|\+) ?m\b.*lyssa", "barris.*lyssa"]
        #         },
        #         "Nordost": {"patterns": ["nordost"]},
        #         "Passiflora": {"patterns": ["passiflora"]},
        #         "Paganini's Violin": {"patterns": ["pagan.*violin"]},
        #         "Sandalwood": {
        #             "patterns": [
        #                 r"\bb ?(and|&|\+) ?m\b.*sandalwood",
        #                 "barris.*sandalwood",
        #             ]
        #         },
        #         "Seville": {"patterns": ["seville"]},
        #         "Soapmakers of Awesometown": {"patterns": ["awesometown"]},
        #         "Spice": {
        #             "patterns": [r"\bb ?(and|&|\+) ?m\b.*spice", "barris.*spice"]
        #         },
        #         "The Full Measure of Man": {"patterns": ["full measure of man"]},
        #         "Waves": {"patterns": [r"\bb ?(and|&|\+) ?m\b.*wave", "barris.*wave"]},
        #     },
        # },
        # "Catie's Bubbles": {
        #     "patterns": [r"\bcb\b", "catie'?s"],
        #     "scents": {
        #         "DFTR": {"patterns": [r"\bdftr\b"]},
        #         "Glace Herbe": {"patterns": [r"glac.*herb"]},
        #         "Le Marche du Rasage": {"patterns": [r"march.*rasag"]},
        #         "Porch Drinks": {"patterns": ["porch drinks"]},
        #         "Two to Mango": {"patterns": ["two to mango"]},
        #     },
        # },
        # "Chicago Grooming Co.": {
        #     "patterns": [r"chicago groom"],
        #     "scents": {
        #         "Armonia": {"patterns": ["armonía"]},
        #         "AG 1889": {"patterns": ["chic.*1889"]},
        #         "Jacmel Vetiveria": {"patterns": ["jacmel vetiveria"]},
        #         "Montrose Beach": {"patterns": ["montrose beach"]},
        #         "Shiloh": {"patterns": ["chica.*shiloh"]},
        #         "Windy City Barbershop": {"patterns": ["windy.*barber"]},
        #     },
        # },
        # "Chiseled Face": {
        #     "patterns": [r"\bcfg?\b", "chiseled face"],
        #     "scents": {
        #         "Bespoke #1": {
        #             "patterns": [r"\bcfg?\b.*bespoke", "chiseled face.*bespoke"]
        #         },
        #         "Black Rose": {
        #             "patterns": [r"\bcfg?\b.*black rose", "chiseled face.*black rose"]
        #         },
        #         "Cryogen": {
        #             "patterns": [r"\bcfg?\b.*cryogen", "chiseled face.*cryogen"]
        #         },
        #         "Ghost Town Barber": {"patterns": ["ghost town barber"]},
        #         "Sherlock": {
        #             "patterns": [r"\bcfg?\b.*sherlock", "chiseled face.*sherlock"]
        #         },
        #         "Summer Storm": {
        #             "patterns": [
        #                 r"\bcfg?\b.*summer storm",
        #                 "chiseled face.*summer storm",
        #             ]
        #         },
        #         "Trade Winds": {
        #             "patterns": [
        #                 r"\bcfg?\b.*trade ?winds",
        #                 "chiseled face.*trade ?winds",
        #             ]
        #         },
        #     },
        # },
        # "Declaration Grooming": {
        #     "patterns": [r"\bdg\b", "declaration grooming", "l&l grooming"],
        #     "scents": {
        #         "Admiral": {
        #             "patterns": [r"\bdg\b.*admiral", "declaration grooming.*admiral"]
        #         },
        #         "Cerberus": {"patterns": ["cerberus"]},
        #         "Dayman": {"patterns": ["dayman"]},
        #         "Dirtyver": {"patterns": ["dirtyver"]},
        #         "Gratiot League Square": {"patterns": ["gratiot league square"]},
        #         "Persephone": {
        #             "patterns": [
        #                 r"\bdg\b.*persephone",
        #                 "declaration grooming.*persephone",
        #             ]
        #         },
        #         "Son et Lumiere": {"patterns": [r"\bson\b.*lumiere"]},
        #         "Trismegistus": {"patterns": ["trismegistus"]},
        #         "Vide Poche": {
        #             "patterns": [r"\bdg\b.*vide", "declaration grooming.*vide"]
        #         },
        #         "Yuzu/Rose/Patchouli": {"patterns": ["yuzu.*patchoul"]},
        #     },
        # },
        # "Dr. Jon's": {
        #     "patterns": ["dr.? joh?n"],
        #     "scents": {
        #         "Dr. Strangelove": {"patterns": [r"\bdr\b.*strangelove"]},
        #         "Flowers in the Dark": {"patterns": ["flowers.*dark"]},
        #     },
        # },
        # "Eleven": {
        #     "patterns": ["eleven"],
        #     "scents": {
        #         "5": {"patterns": [r"eleven.*\b(5|five)\b"]},
        #         "Blue Spruce": {"patterns": ["eleven.*blue spruce"]},
        #         "Line and Basil": {"patterns": ["eleven.*lime.*basil"]},
        #     },
        # },
        # "Goodfellas' Smile": {
        #     "patterns": ["goodfella.*smile"],
        #     "scents": {
        #         "Orange Empire": {"patterns": ["orange empire"]},
        #     },
        # },
        # "Grooming Dept": {
        #     "patterns": ["grooming dep"],
        #     "scents": {
        #         "Boomer": {"patterns": ["grooming dep.*boomer"]},
        #     },
        # },
        # "House of Mammoth": {
        #     "patterns": [r"\bhom\b", "house.*mammoth"],
        #     "scents": {
        #         "Almond Leather": {
        #             "patterns": [
        #                 r"\bhom\b.*almond leather",
        #                 "house.*mammoth.*almond leather",
        #             ]
        #         },
        #         "Avocado (Cream)": {
        #             "patterns": [
        #                 r"\bhom\b.*av(a|o)cado",
        #                 "house.*mammoth.*av(a|o)cado",
        #             ],
        #             "format": "Cream",
        #         },
        #         "Embrace": {
        #             "patterns": [r"\bhom\b.*embrace", "house.*mammoth.*embrace"]
        #         },
        #         "Hygge": {"patterns": ["hygge"]},
        #         "Indigo": {"patterns": [r"\bhom\b.*indigo", "house.*mammoth.*indigo"]},
        #         "Rumble": {"patterns": [r"\bhom\b.*rumble", "house.*mammoth.*rumble"]},
        #         "Shire": {"patterns": [r"\bhom\b.*shire", "house.*mammoth.*shire"]},
        #         "Smash": {"patterns": [r"\bhom\b.*smash", "house.*mammoth.*smash"]},
        #         "Sonder": {"patterns": ["sonder"]},
        #     },
        # },
        # "Henri et Victoria": {
        #     "patterns": ["henri.*victor"],
        #     "scents": {
        #         "Coeur de Vetiver": {"patterns": ["henri.*victor.*vetiv"]},
        #         "Cognac and Cuban Cigars": {"patterns": ["henri.*victor.*cognac"]},
        #         "Costa": {"patterns": ["henri.*victor.*costa"]},
        #         "Lime": {"patterns": ["henri.*victor.*lime"]},
        #     },
        # },
        # "Hendrix Classics & Co": {
        #     "patterns": ["hendrix classics"],
        #     "scents": {
        #         "Magique": {"patterns": ["hendrix.*magique"]},
        #         "Just One Riot": {"patterns": ["just one riot"]},
        #     },
        # },
        # "L&L Grooming": {
        #     "patterns": [r"l(\sand\s|&)l"],
        #     "scents": {
        #         "Marshlands": {"patterns": [r"l(\sand\s|&)l.*marshlands"]},
        #         "Mayflower": {"patterns": [r"l(\sand\s|&)l.*mayflower"]},
        #     },
        # },
        # "London Razors": {
        #     "patterns": ["london razor"],
        #     "scents": {
        #         "Coffee & Contemplation": {"patterns": ["coffee.*contemplat"]},
        #     },
        # },
        # "MacDuffs Soap Co.": {
        #     "patterns": ["macduff"],
        #     "scents": {
        #         "Morning Ritual": {"patterns": ["macduff.*morn.*rit"]},
        #         "Wild Rose Country": {"patterns": ["macduff.*wild rose"]},
        #     },
        # },
        # "Maggard Razor": {
        #     "patterns": ["macduff"],
        #     "scents": {
        #         "Orange Menthol": {"patterns": ["orange menthol"]},
        #     },
        # },
        # "Mäurer & Wirtz": {
        #     "patterns": ["tabac"],
        #     "scents": {
        #         "Sir Irisch Moos": {
        #             "patterns": [r"\bmoos\b"],
        #         },
        #         "Tabac": {
        #             "patterns": ["tabac"],
        #         },
        #     },
        # },
        # "Moon Soaps": {
        #     "patterns": ["moon soap"],
        #     "scents": {"Amaretto Speciale": {"patterns": ["moon.*amaretto"]}},
        # },
        # "Murphy & McNeil": {
        #     "patterns": ["murphy.*ma?cneil"],
        #     "scents": {},
        # },
        # "Mystic Water": {
        #     "patterns": ["mystic water"],
        #     "scents": {
        #         "Lily of the Valley": {"patterns": ["mystic.*lily"]},
        #     },
        # },
        # "Noble Otter": {
        #     "patterns": ["noble otter", r"\bno\b"],
        #     "scents": {
        #         "Barrbarr": {"patterns": ["barrbarr"]},
        #         "Batters Up": {"patterns": ["batter'?s up"]},
        #         "Firefighter": {
        #             "patterns": ["noble otter.*firefighter", r"\bno\b.*firefighter"]
        #         },
        #         "Lonestar": {"patterns": ["lonestar"]},
        #         "Monoi de Tahiti": {"patterns": ["mono.*tahiti"]},
        #         "Northern Elixir": {"patterns": ["northern elixir"]},
        #         "Rawr": {"patterns": [r"\brawr\b"]},
        #         "Tis the Season": {"patterns": ["tis the season"]},
        #         "Two Kings": {
        #             "patterns": [
        #                 r"noble otter.*(2|two) kings",
        #                 r"\bno\b.*(2|two) kings",
        #             ],
        #         },
        #         "茉莉綠茶 (Jasmine Green Tea)": {
        #             "patterns": [
        #                 "jasmine green",
        #                 r"noble otter.*\u8309",
        #                 r"\bno\b.*\u8309",
        #             ]
        #         },
        #     },
        # },
        # "Oaken Lab": {
        #     "patterns": ["oaken lab"],
        #     "scents": {
        #         "Serious Moonlight": {"patterns": ["serious moonlight"]},
        #     },
        # },
        # "PAA": {
        #     "patterns": ["paa", "phoenix artisan"],
        #     "scents": {
        #         "CaD": {"patterns": [r"paa.*\bcad\b", r"phoenix artisan.*\bcad\b"]},
        #         "Doppelgänger": {"patterns": ["paa.*dopp", "phoenix artisan.*dopp"]},
        #         "Droid Black": {"patterns": ["paa.*droid", "phoenix artisan.*droid"]},
        #     },
        # },
        # "Palmolive": {
        #     "patterns": ["palmolive"],
        #     "default format": "Cream",
        #     "scents": {
        #         "Classic": {"patterns": ["palmolive"], "format": "Cream"},
        #         "Sensitive": {"patterns": ["palmolive.*sensit"], "format": "Cream"},
        #     },
        # },
        # "Phoenix & Beau": {
        #     "patterns": [r"phoenix.*\bb"],
        #     "scents": {},
        # },
        # "Pre de Provence": {
        #     "patterns": ["pre de prov"],
        #     "scents": {},
        # },
        # "Proraso": {
        #     "patterns": ["proraso"],
        #     "default format": "Cream",
        #     "scents": {
        #         "Blue (Cream)": {
        #             "patterns": ["proraso.*blue", "proraso.*aloe", "proraso.*protect"],
        #             "format": "Cream",
        #         },
        #         "Cypress & Vetyver (Cream)": {
        #             "patterns": ["proraso.*cypress", "proraso.*vety"],
        #             "format": "Cream",
        #         },
        #         "Green (Cream)": {
        #             "patterns": [
        #                 "proraso",
        #                 r"^(?!\btea\b).*proraso.*green",
        #                 r"^(?!\btea\b).*proraso.*eucal",
        #                 r"^(?!\btea\b).*proraso.*menthol",
        #                 r"^(?!\btea\b).*proraso.*refresh",
        #             ],
        #             "format": "Cream",
        #         },
        #         "Red (Cream)": {
        #             "patterns": [
        #                 "proraso.*red",
        #                 "proraso.*sandal",
        #                 "proraso.*nourish",
        #                 "proraso.*course",
        #             ],
        #             "format": "Cream",
        #         },
        #         "White (Cream)": {
        #             "patterns": [
        #                 "proraso.*white",
        #                 "proraso.*tea",
        #                 "proraso.*sensitive",
        #             ],
        #             "format": "Cream",
        #         },
        #     },
        # },
        # "Razorock": {
        #     "patterns": ["razorock"],
        #     "scents": {},
        # },
        # "Red House Farm": {
        #     "patterns": ["red ?house"],
        #     "scents": {},
        # },
        # "Rex Supply Co.": {
        #     "patterns": ["rex supply"],
        #     "scents": {
        #         "1977": {"patterns": ["rex.*1977"]},
        #     },
        # },
        # "Rock Bottom Soap": {
        #     "patterns": ["rock ?bottom"],
        #     "scents": {},
        # },
        # "Saponificio Varesino": {
        #     "patterns": ["saponificio"],
        #     "scents": {},
        # },
        # "Sebum": {
        #     "patterns": ["sebum"],
        #     "scents": {},
        # },
        # "Shannon's Soaps": {
        #     "patterns": [r"shannon'?s"],
        #     "scents": {},
        # },
        # "Smitten Soapery": {
        #     "patterns": ["smitten"],
        #     "scents": {},
        # },
        # "Southern Witchcrafts": {
        #     "patterns": [r"south.*witch\s?cr", r"\bsw\b"],
        #     "scents": {
        #         "Boonana": {"patterns": ["boonana"]},
        #         "Labyrinth": {
        #             "patterns": [r"south.*witch\s?cr.*labyr", r"\bsw\b.*labyr"]
        #         },
        #         "Pomona": {"patterns": ["pomona"]},
        #         "Valley of Ashes": {"patterns": [r"valley.*\bash"]},
        #     },
        # },
        # "Spearhead Shaving Co.": {
        #     "patterns": ["spearhead", "seaforth"],
        #     "scents": {
        #         "Seaforth! 3 Scots": {
        #             "patterns": ["spearhead.*scots", "seaforth.*scots"]
        #         },
        #         "Seaforth! Black Watch": {"patterns": ["black ?watch"]},
        #         "Seaforth! Fleur de France": {"patterns": ["fleur de france"]},
        #         "Seaforth! Heather": {
        #             "patterns": ["spearhead.*heather", "seaforth.*heather"]
        #         },
        #         "Seaforth! Roman Spice": {"patterns": ["roman spice"]},
        #         "Seaforth! Sea Ice Lime": {"patterns": ["sea ice lime"]},
        #         "Seaforth! Sea Spice Lime": {"patterns": ["sea spice lime"]},
        #         "Seaforth! Spiced": {
        #             "patterns": ["spearhead.*spiced", "seaforth.*spiced"]
        #         },
        #     },
        # },
        # "Stirling Soap Co.": {
        #     "patterns": ["st(i|e)rling"],
        #     "scents": {},
        # },
        # "St. James of London": {
        #     "patterns": ["st.? james"],
        #     "scents": {"Mandarin & Patchouli": {"patterns": ["st.? james.*mandarin"]}},
        # },
        # "Strike Gold Shave": {
        #     "patterns": ["strike gold"],
        #     "scents": {},
        # },
        # "Storybook Soapworks": {
        #     "patterns": ["storybook"],
        #     "scents": {},
        # },
        # "Sudsy Soapery": {
        #     "patterns": ["sudsy"],
        #     "scents": {
        #         "White Sage and Lime": {
        #             "patterns": ["sudsy.*sage.*lime"],
        #         },
        #     },
        # },
        # "Summer Break Soaps": {
        #     "patterns": ["summer break"],
        #     "scents": {"Prom King": {"patterns": ["prom king"]}},
        # },
        # "SUPPLY": {
        #     "patterns": ["supply"],
        #     "scents": {
        #         "Lavender and Lemon (Cream)": {
        #             "patterns": ["supply.*lav.*lem"],
        #             "format": "Cream",
        #         }
        #     },
        # },
        # "Talent Soap Factory": {
        #     "patterns": ["(tsf|talent.*fact)"],
        #     "scents": {},
        # },
        # "Tallow + Steel": {
        #     "patterns": ["tallow.*steel"],
        #     "scents": {
        #         "Boreal": {"patterns": ["tallow.*steel.*boreal"]},
        #         "Dark Two": {"patterns": ["tallow.*steel.*dark.*(two|2)"]},
        #         "Sasq'ets": {"patterns": ["tallow.*steel.*sasq"]},
        #         "Sarsaparilla": {"patterns": ["tallow.*steel.*illa"]},
        #     },
        # },
        # "Taylor of Old Bond Street": {
        #     "patterns": ["(tobs|taylor.*bond)"],
        #     "scents": {
        #         "Jermyn Street": {"patterns": ["(tobs|taylor.*bond).*jermyn"]},
        #         "Sandalwood": {
        #             "patterns": ["(tobs|taylor.*bond).*sandal"],
        #             "format": "Soap",
        #         },
        #         "Sandalwood Shaving Cream": {
        #             "patterns": ["(tobs|taylor.*bond).*sandal.*cream"],
        #             "format": "Cream",
        #         },
        #         "St. James": {"patterns": ["(tobs|taylor.*bond).*james"]},
        #     },
        # },
        # "The Club": {
        #     "patterns": ["the club"],
        #     "scents": {
        # "Boo!!": {"patterns": [r"club.*boo"]},
        # "Boca Negra": {"patterns": [r"club.*boca"]},
        # "Dirty Ginger": {"patterns": [r"club.*ginger"]},
        # "Khalifa": {"patterns": ["khalifa"]},
        # "Low Scent Skeleton": {"patterns": [r"club.*skele"]},
        # "Signature": {"patterns": [r"club.*signat"]},
        # "The Graveyand": {"patterns": [r"club.*grave"]},
        # "Vanille Vendetta": {"patterns": [r"club.*vanil"]},
        # "Fruit de la Passion": {"patterns": [r"club.*passion"]},
        # },
        # },
        # "The Goodfellas Smile": {
        #     "patterns": ["goodfella"],
        #     "scents": {
        #         "Chronos": {"patterns": [r"goodfell.*chrono"]},
        #     },
        # },
        # "The Holy Black": {
        #     "patterns": ["holy.*black"],
        #     "scents": {
        #         "Gunpowder Spice": {"patterns": [r"holy.*black.*gunp"]},
        #         "Coconut Creeper": {"patterns": [r"holy.*black.*creep"]},
        #         "The Galleon!": {"patterns": [r"holy.*black.*gall"]},
        #     },
        # },
        # "The Shave Mercantile": {
        #     "patterns": ["shave.*mercan"],
        #     "scents": {
        #         "Limeade": {"patterns": [r"shave.*mercan.*limeade"]},
        #     },
        # },
        # "Through the Fire Fine Crafts": {
        #     "patterns": ["through.*fire"],
        #     "scents": {
        #         "Northern Lights": {"patterns": [r"through.*fire.*north.*light"]},
        #     },
        # },
        # "Truefitt & Hill": {
        #     "patterns": ["truefitt"],
        #     "scents": {
        #         "No. 10 Finest Shaving Cream": {
        #             "patterns": [r"truefitt.*10"],
        #             "format": "Cream",
        #         },
        #     },
        # },
        # "Turtleship  Shave Co.": {
        #     "patterns": ["turtleship"],
        #     "scents": {
        #         "Tejava": {"patterns": [r"turtle.*tejava"]},
        #     },
        # },
        # "Van Der Hagen": {
        #     "patterns": ["hag(e|a)n"],
        #     "scents": {
        #         "Scented Luxury": {"patterns": [r"hag(e|a)n.*lux"]},
        #     },
        # },
        # "Vitos": {
        #     "patterns": ["vitos"],
        #     "scents": {
        #         "Extra Super": {"patterns": [r"vitos.*extra"]},
        #     },
        # },
        # "West Coast Shaving": {
        #     "patterns": [r"(wcs|west.*coast)"],
        #     "scents": {
        #         "Bergamot": {"patterns": [r"(wcs|west.*coast).*bergamot"]},
        #         "Fougere": {"patterns": [r"(wcs|west.*coast).*foug"]},
        #         "Jojoba Oriental": {"patterns": [r"(wcs|west.*coast).*jojoba"]},
        #     },
        # },
        # "WestMan Shaving": {
        #     "patterns": ["westman"],
        #     "scents": {
        #         "Alma": {"patterns": [r"westman.*alma"]},
        #         "Nirvana": {"patterns": [r"westman.*nirvana"]},
        #         "Utopia": {"patterns": [r"westman.*utopia"]},
        #     },
        # },
        # "Wet Shaving Products": {
        #     "patterns": [r"(wet shav|wsp)"],
        #     "scents": {
        #         "Formula T Gaelic Tweed": {"patterns": [r"(wet shav|wsp).*gaelic"]},
        #         "Olympus Shaving Cream": {
        #             "patterns": [r"(wet shav|wsp).*olympus"],
        #             "format": "Cream",
        #         },
        #     },
        # },
        # "Whispers from the Woods": {
        #     "patterns": ["whispers.*woods"],
        #     "scents": {
        #         "Pomelo": {"patterns": [r"whispers.*pomel"]},
        #     },
        # },
        # "Wickham Soap Co.": {
        #     "patterns": ["wickham"],
        #     "scents": {
        #         "Club Cola": {"patterns": [r"wickham.*cola"]},
        #     },
        # },
        # "Williams": {
        #     "patterns": ["williams"],
        #     "scents": {
        #         "Mug Soap": {"patterns": [r"william.*mug"]},
        #     },
        # },
        # "Wilkinson Sword": {
        #     "patterns": ["wilkinson"],
        #     "scents": {
        #         "Black Soap": {"patterns": [r"wlkinson.*black"]},
        #     },
        # },
        # "Wholly Kaw": {
        #     "patterns": ["wholly.*kaw"],
        #     "scents": {
        #         "1776": {"patterns": [r"wholly.*kaw.*1776"]},
        #         "Amber Bomba": {"patterns": [r"wholly.*kaw.*amber bomb"]},
        #         "Fern Concerto": {"patterns": [r"wholly.*kaw.*fern concert"]},
        #         "Man From Mayfaire": {"patterns": [r"wholly.*kaw.*mayfa"]},
        #         "Aranceto": {"patterns": [r"wholly.*kaw.*aranc"]},
        #         "Dark Vetiver": {"patterns": [r"wholly.*kaw.*vetiv"]},
        #         "Fougere Bouquet": {"patterns": [r"wholly.*kaw.*bouquet"]},
        #         "Fougere Mania": {"patterns": [r"wholly.*kaw.*mania"]},
        #         "King of Bourbon": {"patterns": [r"wholly.*kaw.*bourbon"]},
        #         "King of Oud": {"patterns": [r"wholly.*kaw.*oud"]},
        #         "Merchant of Tobacco": {"patterns": [r"wholly.*kaw.*merchant"]},
        #         "Monaco Royale": {"patterns": [r"wholly.*kaw.*monaco"]},
        #         "Nightcap": {"patterns": [r"wholly.*kaw.*night.*cap"]},
        #         "PasteurVision": {"patterns": [r"wholly.*kaw.*past"]},
        #         "Rebelle": {"patterns": [r"wholly.*kaw.*rebel"]},
        #         "Tempest": {"patterns": [r"wholly.*kaw.*tempest"]},
        #         "Timmerman Red Label 1869": {"patterns": [r"wholly.*kaw.*timmer"]},
        #         "Transition": {"patterns": [r"wholly.*kaw.*transition"]},
        #         "Yuzu, Rose, Patchouli": {"patterns": [r"wholly.*kaw.*yuzu"]},
        #     },
        #     "Xabons Xavieiro": {
        #         "patterns": ["xabon"],
        #         "scents": {
        #             "Koko Nud": {"patterns": [r"xabon.*koko"]},
        #         },
        #     },
        # },
        # "Zingari Man": {
        #     "patterns": ["zingari"],
        #     "scents": {
        #         "Amir": {"patterns": ["zingari.*amir"]},
        #         "Bon Monsieur": {"patterns": ["zingari.*monsieur"]},
        #         "Mousse Illuminee": {"patterns": ["zingari.*illuminee"]},
        #         "No. 1": {"patterns": ["zingari.*no.*1"]},
        #         "The Brewer": {"patterns": ["zingari.*brew"]},
        #         "The Gatherer": {"patterns": ["zingari.*gather"]},
        #         "The Highlander": {"patterns": ["zingari.*highlander"]},
        #         "The Magician": {"patterns": ["zingari.*magic"]},
        #         "The Master": {"patterns": ["zingari.*master"]},
        #         "The Royal": {"patterns": ["zingari.*royal"]},
        #         "The Wandereer": {"patterns": ["zingari.*wander"]},
        #         "The Watchman": {"patterns": ["zingari.*watch", "watchman"]},
        #         "Unscented": {"patterns": ["zingari.*unscent"]},
        #     },
        # },
    }

    @cached_property
    def __soaps_from_yaml(self):
        with open(f"{os.getcwd()}/sotd_collator/soaps.yaml", "r") as f:
            return yaml.load(f, Loader=yaml.SafeLoader)

    @cached_property
    def __mapper(self):
        output = {}

        data = None

        # for brand, brand_map in self._raw.items():
        for brand, brand_map in self.__soaps_from_yaml.items():
            scents = brand_map["scents"] if "scents" in brand_map else {}
            for scent, property_map in scents.items():
                for pattern in property_map["patterns"]:
                    format = (
                        property_map["format"] if "format" in property_map else "Soap"
                    )
                    name = f"{brand} - {scent}".strip()
                    # if format != "Soap":
                    #     name = f"{name} ({format})"

                    output[pattern] = {
                        "brand": brand,
                        "scent": scent,
                        "name": name,
                        "format": format,
                    }
        return output

    @cached_property
    def __brand_map(self):
        output = {}
        # for brand, property_map in self._raw.items():
        for brand, property_map in self.__soaps_from_yaml.items():
            for pattern in property_map["patterns"]:
                output[pattern] = {
                    "brand": brand,
                    "default format": (
                        property_map["default format"]
                        if "default format" in property_map
                        else "Soap"
                    ),
                }
        return output

    @lru_cache(maxsize=None)
    def _get_value(self, input_string: str, field: str) -> str:

        input_string = input_string.replace("*", "")
        regexes = sorted(self.__mapper.keys(), key=len, reverse=True)
        for alt_name_re in regexes:
            if re.search(alt_name_re, input_string, re.IGNORECASE):
                property_map = self.__mapper[alt_name_re]
                if field in property_map:
                    return property_map[field]

        map = self.split_name(input_string)
        # we didn't find an exact scent, try to match at least brand by regex
        regexes = sorted(self.__brand_map.keys(), key=len, reverse=True)
        for alt_name_re in regexes:
            match = re.search(alt_name_re, input_string, re.IGNORECASE)
            if match:
                property_map = self.__brand_map[alt_name_re]
                brand = property_map["brand"]
                scent = map["scent"] if map is not None else None
                if scent is None:
                    # strip brand out of input string and scent is what is left at the end
                    scent = (
                        input_string.replace(match.group(0), "")
                        .strip()
                        .removeprefix("-")
                        .removesuffix(".")
                        .strip()
                    )

                name = f"{brand} - {scent}"
                format = map["format"] if map is not None and "format" in map else None
                if format is None:
                    if re.search(r"\bcream\b", name, re.IGNORECASE):
                        format = "Cream"
                    elif re.search(r"\bfoam", name, re.IGNORECASE):
                        format = "Foam"

                if format is None:
                    format = (
                        property_map["default format"]
                        if "default format" in property_map
                        else "Soap"
                    )
                # if format != "Soap":
                #     name = f"{name} ({format})"

                map = {
                    "brand": brand,
                    "scent": scent,
                    "name": name,
                    "format": format,
                }

                return map[field]

        # return None
        map = self.split_name(input_string)
        return map[field] if map is not None else None

    def split_name(self, input_string: str):

        match = re.search(r"\(\d{1,3}\)", input_string)
        if match:
            input_string = input_string.replace(match.group(0), "")

        input_string = input_string.replace("—", "-").replace("–", "-")
        parts = input_string.split(" - ")
        while "   " in input_string:
            input_string.replace("   ", "  ")

        if len(parts) < 2:
            parts = input_string.split("  ")

        result = {}
        if len(parts) > 1:

            scent = parts[1].strip().removesuffix(".").strip()
            suffixes = ["soap", "soap", "shaving soap", "-"]
            for suffix in suffixes:
                match = re.search(suffix, scent, re.IGNORECASE)
                if match:
                    scent = scent.replace(match.group(0), "")

            result["brand"] = parts[0].strip()
            result["scent"] = scent
            result["name"] = f"{parts[0].strip()} - {scent}"
            # result["format"] = "Soap"

            if len(parts) > 2:
                if re.search("soap", parts[2], re.IGNORECASE):
                    result["format"] = "Soap"
                elif re.search("cream", parts[2], re.IGNORECASE):
                    result["format"] = "Cream"
                elif re.search("foam", parts[2], re.IGNORECASE):
                    result["format"] = "Foam"
                else:
                    result["format"] = "Soap"
            else:
                if re.search("soap", parts[1], re.IGNORECASE):
                    result["format"] = "Soap"
                elif re.search("cream", parts[1], re.IGNORECASE):
                    result["format"] = "Cream"
                elif re.search("foam", parts[1], re.IGNORECASE):
                    result["format"] = "Foam"
                else:
                    result["format"] = "Soap"

            return result

        return None


if __name__ == "__main__":

    class CustomDumper(yaml.Dumper):
        def represent_data(self, data):
            if isinstance(data, str) and ("\\" in data or "?" in data):
                return self.represent_scalar("tag:yaml.org,2002:str", data, style="'")

            return super(CustomDumper, self).represent_data(data)

    rp = SoapParser()
    raw = None
    with open(f"{os.getcwd()}/sotd_collator/soaps.yaml", "r") as f:
        raw = yaml.load(f, Loader=yaml.SafeLoader)

    with open(f"{os.getcwd()}/sotd_collator/soaps.yaml", "w") as f:
        yaml.dump(raw, f, default_flow_style=False, Dumper=CustomDumper)

    # print(arn.all_entity_names)
