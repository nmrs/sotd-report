import datetime
from dateutil.relativedelta import relativedelta

from functools import cached_property, lru_cache

import pandas as pd
import praw

from sotd_collator.base_alternate_namer import BaseAlternateNamer
import re

from sotd_collator.sotd_post_locator import SotdPostLocator


class SoapAlternateNamer(BaseAlternateNamer):
    """
    Amalgamate names
    """

    RE_AND = r"\s*(?:&|and|\+)?\s*"

    _outliermap = {
        ("Declaration Grooming", "Cerberus"): [r"\bcerberus\b"],
        ("House of Mammoth", "Smash"): [r"\bhouse of mammoth.*barr.*mann\b"],
        ("Maurer & Wirtz", "Tabac"): ["^tabac"],
        ("Maurer & Wirtz", "Sir Irisch Moos"): [r"^sir\s*-?\s*irisc?h", r"^irisc?h\s+moos\b"],
        ("Noble Otter", "'Tis the Season'"): [r"^tis\s+the\s+season\b"],
        ("Spearhead Shaving Co.", "Sea Ice Lime"): [r"\bsea\s+ice\s+lime\b"],
        ("West Coast Shaving","Grapefroot"): [r'\bcbubs\/WCS\s+grapefroot\b'],
    }

    _raw = {
            "345 Soap Co.":
            [
                [r"\b345\b", r"\b345\s+soap(?:\s+co)?\b"],
                {
                },
            ],
            "Abbate Y La Mantia":
            [
                [r"\babbate.*mantia\b"],
                {
                    "Fufluns": [r"fufl[iu]ns"]
                },
            ],
            "Ariana & Evans":
            [
                [fr"\bariann?a{RE_AND}evan(?:s)?\b", fr"\ba{RE_AND}e\b"],
                {
                    "Asian Plum": [fr"\basian plum\b"],
                    "Peach & Cognac": [fr"\bpeach{RE_AND}cognac\b"],
                    "St. Barts": [r"\bst\.?\s+barts?\b"],
                    "SoCal Hipster": [r"\bsocal\s+hipster\b"],
                    "Vacanza Romana": [r"\bvacan[cz]a\s+romana\b"],
                    "Vanille de Tabac": [r"\bvanille\s+de\s+tabac\b"],
                },
            ],
            "Arko":
            [
                [r"\barko\b"],
                {
                    "Cool": [r"\\bcool\b"],
                    "Hydrate": [r"\bhydrate\b"],
                    "Shaving Soap": [r".*"],
                },
            ],
            "Asylum Shave Works":
            [
                [r"\basylum\s+shave\s+works\b"],
                {
                },
            ],
            "Azalea City Suds":
            [
                [r"\bazalea\s+city\b"],
                {
                },
            ],
            "Ballenclaugh Soaps":
            [
                [r"\bballenclaugh\s+soaps\b"],
                {
                },
            ],
            "Barrister & Mann":
            [
                [fr"\bb{RE_AND}?m\b", fr"\bbar\S*{RE_AND}?man\S*\b", r"\bbam\b"],
                {
                    "Adagio": [r"\badagio\b"],
                    "Bay Rum": [r"\bbay rum\b"],
                    "Braeburn": [r"\bbraeb?urn\b"],
                    "Beaudelaire": [r"\bbeaudela?ire\b"],
                    "Behold the Whatsis!": [r"\bbehold the whatsis\b"],
                    "Electric Mayhem": [r"electric mahem"],
                    "Fougere Gothique": [r"fougere gothique"],
                    "The Full Measure of Man": [r"\bfull measure of (?:a )?mann?\b"],
                    "Midnight Special": [r"\bmidnight\s+special\b"],
                    "Mûir(e) Wood": [r"muire?", r"murie"],
                    "Nocturne": [r"nocturne"],
                    "Nordost": [r"nordost"],
                    "Paganini's Violin": [r"paganini.*violin"],
                    "Passiflora": [r"passiflori?a"],
                    "Promises": [r"\bpromises\b"],
                    "Reserve Classic": [r"\b(?:\breserve\s+)?classic\b"],
                    "Reserve Cool": [r"\b(?:\breserve\s+)?cool\b"],
                    "Reserve Fern": [r"\b(?:\breserve\s+)?fern\b"],
                    "Reserve Lavender": [r"\b(?:\breserve\s+)?lavender\b"],
                    "Reserve Spice": [r"\b(?:\breserve\s+)?spice\b"],
                    "Reserve Waves": [r"\b(?:\breserve\s+)?waves\b"],
                    "Seville": [r"\bseville\b"],
                    "Soft Heart Series: Brew Ha-Ha": [r"\bsoft\s+heart.*\bbrew\b", r"brew\s+ha\b"],
                    "Soft Heart Series: Sandalwood": [r"\bsoft\s+heart.*\bsandalwood\b"],
                },
            ],
            "Black Ship Grooming Co.":
            [
                [r"\bblack\s+ship\b", r"\bblack\s+ship\s+grooming(?:\s+co\.?)?\b"],
                {
                },
            ],
            "Catie's Bubbles":
            [
                [r"\bcatie'?s?\s+bubbles\b", r"\bcb\b"],
                {
                    "'95 Liquid Labels": [r"95 liquid labels"],
                    "Menage a Lavande": [r"menage a lavande"],
                    "Pine Barrents": [r"pine barrens"],
                    "Two to Mango": [r"two to mango"],
                    "Valley of Fire": [r"valley of fire"],
                },
            ],
            "Cella":
            [
                [r"\bcella\b"],
                {
                    "Almond": [".*"],
                    "Aloe Vera": ["aloe", "bio", "blue", "green", "vera"],
                },
            ],
            "Central Texas Soaps":
            [
                [r"\bcentral\s+texas\s+soaps?\b"],
                {
                },
            ],
            "Chicago Grooming Co.":
            [
                [r"\bchicago\s+grooming\s+co\.?\/house\s+of\s+mammoth\b",
                 r"\bchicago\s+grooming(?:\s+co\.?)?\b",
                # it looks like the Oleo Soap Works Windy City Barbershop is the same soap (same label), so collapse them
                 r"\boleo\s+soap\s*works?\b"],
                {
                },
            ],
            "Chicago Grooming Co. / Xicano Shaver":
            [
                [r"\bchicago\s+grooming\s+co\.?\s*\/\s*xicano\s+shaver\b"],
                {
                },
            ],
            "Chiseled Face":
            [
                [r"\bchiseled\s*face\b", r"\bchiseled\s*face\s+groom(?:ing|atorium)\b", r"\bcf\b"],
                {
                    "Ghost Town Barber": [r"\bghost town barber(?:shop)?\b"]
                    # "Trade Winds": [r"\btrade\s+winds\s+"]
                },
            ],
            "The Club":
            [
                [r"\bthe\s+club\b"],
                {
                    "Black": [r"\bblack\b"]
                },
            ],
            "Col. Ichabod Conk":
            [
                [r"\bcol.?\s+(?:ichabod\s+)?conk\b"],
                {
                },
            ],
            "Crabtree & Evelyn":
            [
                [r"\bcrabtree\b"],
                {
                },
            ],
            "Declaration Grooming":
            [
                [r"\bdg\b",r"\bdeclaration\s+grooming\b", r"\bdeclaration\s+shaving\b",
                 r"\bdg\/cl\b",r"\bdeclaration\s+grooming\s*\/\s*chatillon\s+lux\b",
                 r"\bchatillon\s+lux\s*(?:and|\/|&)\s*declaration\s+grooming\b"],
                {
                    "88 Chestnut St": [r"\b88\s+chestnut\b"],
                    "Fake Yellow Light": [r"\bfake yellow light\b"],
                    "Massacre of the Innocents": [r"\bmassacre\s+of\s+the\s+innocents?\b"],
                    "Peaches + Scream": [r"\bpeaches\b"],
                    "Yuzu/Roze/Patchoili": [r"\byuzu.*patchouli"],
                },
            ],
            # "Declaration Grooming / Chatillon Lux":
            # [
            #     [r"\bdg\/cl\b",r"\bdeclaration\s+grooming\s*\/\s*chatillon\s+lux\b",
            #      r"\bchatillon\s+lux\s*(?:and|\/)\s*declaration\s+grooming\b"],
            #     {
            #     },
            # ],
            "Denton Majik":
            [
                [r"\bdenton\s*majic?k?\b"], {}
            ],
            "De Vergulde Hand":
            [
                [r"\bvergulde\b"],
                {
                    "Scheerzeepstaaf": [r"\bScheerzeepstaaf\b"]
                },
            ],
            "D.R. Harris & Co. Ltd.":
            [
                [r"\bd\.?r\.?\s+harris\b"], {}
            ],
            "Dr. Jon's":
            [
                [r"\bdr.?\s+jon'?s?\b"], {}
            ],
            "Eleven":
            [
                [r"\beleven(?:\s+shaving)?\b"], {}
            ],
            "Elysian":
            [
                [r"\belysian\b", r"\belysian\s+soap\s+shop\b"], {}
            ],
            "Fine Accoutrements":
            [
                [r"\bfine\s+accoutrements\b"],
                {
                },
            ],
            "First Line Shave":
            [
                [r"\bfirst\s+line\s+shaves?\b"],
                {
                    "Platinum": [r"platinum"]
                },
            ],
            "The Gentleman's Groom Room":
            [
                [r"\bgentlem(?:a|e)n'?s?\s+nod\b"],
                {
                },
            ],
            "Gentleman's Nod":
            [
                [r"\b(?:the\s+)?gentlem(?:a|e)n'?s?\s+nod\b"],
                {
                    "Juniper Reverie": [r"\bjuniper\s+reverie\b"],
                },
            ],
            "Green Mountain Soap":
            [
                [r"\bgreen\s+mountain\b"],
                {
                },
            ],
            "Grooming Dept":
            [
                [r"\bgrooming\s+dept\b", r"\bgrooming\s+department\b"],
                {
                    "Ardent": [r"\bardent\b"],
                    "Laundry II": [r"\blaundry\s*(?:ii|2|two)\b"],
                    "Wonderland": [r"\bwonderland\b"],
                },
            ],
            "HAGS":
            [
                [r"\bhags\b"],
                {
                },
            ],
            "Haslinger":
            [
                [r"\bhaslinger\b"],
                {
                },
            ],
            "Hendrix Classics & Co":
            [
                [r"\bhendrix\s+classics?\b", r"\bhendrix\s+c(?:&|and|\+)?c\b", 
                 r"\bhc(?:&|and|\+)?c\b", r"\bhendrix\s+classics\s*(?:&|and|\+)?\s+co\b"],
                {
                    "Barbershop": [r"\bbarbershop\b"],
                    "Empire State of Mind": [r"\bempire\s+state\b"],
                    "Ladies' Man": [r"\bladies'?\s+man\b"],
                },
            ],
            "Henri et Victoria":
            [
                [r"\bhenri\s+et\s+victoria\b", r"\bhev\b"],
                {
                },
            ],
            "Highland Soap Co.":
            [
                [r"\bhighland (?:soap )?co.?(?:mpany)\b"], {}
            ],
            "Highland Springs Soap Co.":
            [
                [r"\bhighland springs? (?:soap )?co.?(?:mpany)\b",
                 r"Highland Springs Soap Co\s*/\s*Australian Private Reserve",
                ],
                {
                },
            ],
            "Hoffman's Shave & Soap Co.":
            [
                [r"\bhoffman'?s?\b", r"\bhoffman'?s?\s+shave\s+(:?&|and|\+)\s+soap\s+co.?\b"],
                {
                },
            ],
            "The Holy Black":
            [
                [r"\bholy\s+black\b", r"\bthe\s+holy\s+black\b"], 
                {
                    "Artisan Line": [r"artisan line"]
                }
            ],
            "Hombres":
            [
                [r"\bhombres\b"],
                {
                    "Spaghetti Western": [r"spaghetti western"]
                },
            ],
            "House of Mammoth":
            [
                [r"\bhouse\s+of\s+mammoth\b", r"\bhoue\s+of\s+mammoth\b", r"\bhom\b", r"\bmammoth\b"],
                {
                    "Fu Dao": [r"\bfu\s+dao\b", "福"],
                    "Hygge": [r"\bhygg?ee?\b"],
                    "Indigo": [r"\bindigo\b"],
                    "Santa Noir": [r"\bsantal?\s+noire?\b"],
                    "Shire": [r"\bshire\b"],
                    "Tobacconist": [r"\bt[ao]bb?acc?onist\b"],
                    "Uitwaaien": [r"\bui?twaaien\b"],
                    "Voices": [r"\bvoices\b"],
                },
            ],
            "Imaginary Authors":
            [
                # clean up to split base and scent?
                [r"\bimaginary\s+authors\b", r"\bimaginary\s+authors\/noble\s+otter\b", 
                 r"\bnoble\s+otter\/imaginary\s+authors\b"],
                {
                },
            ],
            "La Toja":
            [
                [r"\b(?:la\s+)?toja\b"],
                {
                    "Shaving Soap Stick": [".*"]
                },
            ],
            "LEA":
            [
                [r"^lea\b"],
                {
                    "Stick": [r".*"]
                },
            ],
            "MacDuff's Soap Company":
            [
                [r"\bma?cduff'?s?\b", r"\bma?cduff'?s?\s+soap\s+co(?:mpany)?\b"],
                {
                    "American Vintage": [r"\bamerican\s+vintage\b"],
                    "Autumn Cabin": [r"\bautumn\s+cabin\b"],
                    "Birth of the Cool": [r"\bbirth\s+of\s+the\s+cool\b"],
                    "Santa's Cheer": ["santa"],
                },
            ],
            "Maggard Razors":
            [
                [r"\bmaggard\s+razors?\b"],
                {
                },
            ],
            "Martin de Candre":
            [
                [r"\bmartin\s+de\s+candre\b"],
                {
                    "Fougere": [r"\bfougere\b"]
                },
            ],
            "Master Soap Creations":
            [
                [r"\bmaster\s+soap\s+creations\b", r"\bmsc\b"],
                {
                    "Light Blue": [r"light\s+blue"]
                },
            ],
            "Maurer & Wirtz":
            [
                [r"\bmaur?er\s+(?:&|and|\+)?\s+wirtz\b", r"\btabac\b"],
                {
                    "Tabac": [r"\btabac\b", r".*"],
                    "Sir Irisch Moos": [r"\birisch\b"],
                },
            ],
            "Mickey Lee Soapworks":
            [
                [r"\bmickey\s+lee\s+soapworks\b"],
                {
                },
            ],
            "Mike's Natural Soaps":
            [
                [r"\bmike'?s\s+natural(?:\s+soaps?)?\b"],
                {
                },
            ],
            "Mitchell's Wool Fat":
            [
                [r"\bmitchell\'?s\s+wool\s+fat\b", r"\bmwf\b"],
                {
                    "Shaving Soap": [".*"]
                },
            ],
            "Moon Soaps": [ [r"\bmoon\s*soaps\b"], {} ],
            "Murphy & McNeil":
            [
                [r"\bmurphy\s+(?:&|and|\+)\s+mcneill?\b"],
                {
                    "Barbershop de Los Muertos 3": [r"\bbarbershop de los muertos 3\b"],
                    "Kells": [r"\bkells\b"],


                },
            ],
            "Muhle": [ [r"\bmuhle\b"], {} ],
            "Noberu of Sweden": [ [r"\bnoberu\s+of\s+sweden\b"], {} ],
            "Noble Otter":
            [
                [r"\bnoble\s*otter\b", r"\bnobel\s*otter\b", r"^\bno\b"],
                {
                    "Barrbarr": [r"\bbarr?\s*barr?\b"],
                    "Hamami": ["hamami"],
                    "Monoi de Tahiti": [r"\bmonoi de tahiti\b"],
                    "Neon Sun": [r"\bneon\s+sun\b"],
                    "The Noir Et Vanille": [r"\bnoir\s+et\s+vanille\b", r"\btnev\b"],
                    "Northern Elixer": [r"\bnorthern\s+elixir\b"],
                    "Orbit": [r"\borbit\b"],
                    "Rawr": [r"\brawr\b"],
                    "'Tis the Season": [r"\btis\s+the\s+season\b"],
                },
            ],
            "Oaken Lab":
            [
                [r"\boaken\s+labs?\b"],
                {
                },
            ],
            "Obsessive Soap Perfectionist":
            [
                [r"\bobsessive\s+soap\s+perfectionists?\b", r"\bosp\b"], {}
            ],
            "Pré de Provence":
            [
                [r"\bpr(?:é|e)\s+de\s+Provence\b"],
                {
                    "No. 63": [r"\bno\.?\s+(?:63|sixty\s*-?\s*three)\b"],
                },
            ],
            "Proraso":
            [
                [r"\bprorass?o\b", r"\bporass?o\b"],
                {
                    "Aloe and Vitamin E (Blue)": ["aloe", "blue", "protective"],
                    "Eucalyptus Oil and Menthol (Green)": ["eucalyptus", "menthol", "green", "classic", r"\bshave\s+cream\b"],
                    "Green Tea and Oat Sensitive Skin (White)" : ["green tea", r"\boat\b", "sensitive", "white"],
                    "Sandalwood with Shea Butter (Red)": ["sandalwood", "red", "rosso", "nourishing"],
                },
            ],
            "RazoRock":
            [
                [r"\brazorock\b"],
                {
                    "Blue Barbershop": [r"\bblue\s+barbershop\b"],
                    "XXX": [r"\bxxx\b"],
                },
            ],
            "Red House Farm":
            [
                [r"\bred\s+house\s+farms?\b"],
                {
                    "Nine Days Up Nort": ["up\s+nort"]
                },
            ],
            "Rex":
            [
                [r"\brex\b"], {}
            ],
            "Rock Bottom Soap":
            [
                [r"\brock\s+bottom\s+soap\b"], {}
            ],
            "Rockwell":
            [
                [r"\brockwell\b"], {}
            ],
            "Siliski Soaps":
            [
                [r"siliski", r"siliski\s+soaps?"], {}
            ],
            "Saponificio Varesino":
            [
                [r"\bsapon[io]ficio\s+varesino\b"], 
                {
                    "Manna di Sicilia": [r"\bmanna\s+di\s+sicilia\b"]
                }
            ],
            "Shannon's Soaps":
            [
                [r"\bshannon\'?s?\s+soaps?\b", r"\bshannon\'?s?\s+shaves?\b"], {}
            ],
            "Southern Witchcrafts":
            [
                [r"\bsouthern\s*witf?chcraft(?:s)?\b", r"\bsw\b"],
                {
                    "Boonana": [r"\bboonana\b"],
                    "Fougere Nemeta": [r"\bfougere\s+nem[ae]ta\b"],
                    "Valley of Ashes": [r"\bvalley\s+of\s+ashes\b"],
                    # "Grave Fruit": [r"grave\s*fruit"],
                },
            ],
            "Spearhead Shaving Co.":
            [
                [r"\bspearhead\b", r"\bsperahead\b", r"spearhead\s+soaps", r"spearhead\s+seaforth\b",
                 r"spearhead\s+shaving\s+co(?:mpany|\.)?", r"^seaforth\b"],
                {
                    'Black Watch': [r"\bblack\s*watch\b"],
                    'Fleur De France': [r"\bfleur\s+de\s+france\b"],
                    'Heather': [r"\bheather\b"],
                    'Sea Ice Lime': [r"\bsea\s+iced?\s+lime\b"],
                    'Sea Spice Lime': [r"\bsea\s+spiced?\s+lime\b"],
                    'Spiced': [r'\bseaforth\b[\s!]*\bspiced\b', r"\bspice\b"],
                },
            ],
            "Stirling Soap Co.":
            [
                [r"\bst[ie]rling\b", r"\bst[ie]rling\s+soaps?\s*(?:co(?:mpany)?)?\b"],
                {
                    "Almond Creme": [r"\balmond cre(?:me|am)\b"],
                    "Baker Street": [r"\bbaker\s+st(?:reet)?\b"],
                    "Barbershop": [r"\bbarbershop\b"],
                    "Executive Man": [r"\bexecutive\s+man\b"],
                    "Frankincense & Myrrh": [fr"\bfrankins?cense{RE_AND}myrrh\b"],
                    "Margaritas in the Arctic": [r"\bmargaritas\s+in\s+the\s+arc?tic\b"],
                    "Electric Sheep": [r"electric\s+shr?eep"],
                    "Pumpkin Spice": [r"\bpumpkin\s+spice\b"],
                    "SB-129": [r"\bsb-?129\b"],
                    "Sharp Dressed Man": [r"\bsharp\s+dressed\s+man\b", r"\bsharped-\s+dressed\s+man\b"],
                    "Vanilla Sandalwood": [r"\bvanilla\s+sandalwood\b"],
                },
            ],
            "Stone Cottage Soapworks ":
            [
                [r"\bstone\s+cottage(?:\s+(?:soaps?|soapworks?|shaving))?\b"],
                {
                },
            ],
            "Storybook Soapworks":
            [
                [r"\bstorybr?ook\s+soapworks\b"], {}
            ],
            "Strike Gold Shave":
            [
                [r"\bstrike\s+gold(?:\s+shave)?\b"],
                {
                },
            ],
            "Summer Break Soaps":
            [
                [r"\bsummer\s*break\s*soaps\b"],
                {
                    "Picture Day": [r'\bpicture\s+day\b'],
                    "Daydream": [r"\bday\s*dream\b"],
                    "Remote Learning": [r"\bremote\s+learning\b"],
                    "Teacher's Pet": [r"\bteacher'?s\s+pet\b"],
                    "Woodshop": [r"\bwood\s*shop\b"],
                },
            ],
            "Summer Break Soaps / London Razors":
            [
                [r"\blondon\s+razors?\b", r"\bsummer\s+break.*london\s+razors", 
                 r"\blondon\s+razors.*summer\s+break(?:\s+soaps)?\b"],
                {
                    "Bell Ringer": [r"bell\s*ringer"],
                    "But first... Coffee": [r'first\s*coffee'],
                    "But first... an experiment": [r'first\s*an\s*experiment'],
                    "Coffee & Contemplation": ['contemplation'],
                },
            ],
            "Talent Soap Factory":
            [
                [r"\btalent\s+soap\s+factory\b"],
                {
                    "Razberri & Tomato Leaf": [r"\brazz?berr?[iy]\s+(?:&|and|\+)?\s*tomato\b"],
                    "Where the Wild Things Were": [r"\bwhere\s+the\s+wild\s+things\b"],
                }
            ],
            "Taylor of Old Bond Street":
            [
                [r"\btaylor\s+of\s+old\s+bond\s+st(?:reet|\.)?\b", r"\btobs\b"],
                {
                    "Sandalwood": [r"\bsandalwood", r"sandlewoos"]
                }
            ],
            "Tcheon Fung Sing":
            [
                [r"\btcheon\s+fung\s+sing\b", r"\btfs\b"], {}
            ],
            "Through the Fire Fine Crafts":
            [
                [r"\bthrough\s+the\s+fire\b", r"\bthrough\s+the\s+fire\s+fine\s+crafts?\b"],
                {
                    "Razberri & Tomato Leaf": [r"\brazz?berr?[iy]\s+(?:&|and|\+)?\s*tomato\b"]
                }
            ],
            "Truefitt & Hill":
            [
                [r"\btruefitt\s+(?:&|and|\+)\s+hill\b"],
                {
                }
            ],
            "West Coast Shaving":
            [
                [r"\bwest\s+coast\s+shaving\b", r"\bwcs\b"],
                {
                    "Chypre": [r"\bchypre\b"]
                },
            ],
            "WestMan Shaving":
            [
                [r"\bwest\s*man\s+shaving\b"],
                {
                },
            ],
            "Wet Shaving Products":
            [
                [r"\bwet\s+shavings?(?:\s+products?)?\b"],
                {
                },
            ],
            "Whickham Soap Co.":
            [
                [r"\bwickham\s+soap\s+co\.?\b"],
                {
                },
            ],
            "Wholly Kaw":
            [
                [r"\wholly\s+kaw\b"],
                {
                    "1869 Timmermann Red Label": [r"\b1869\s+red\s+label\b"],
                    "Cedrati": [r"\bcedrati\b"],
                    "Club Yanka": [r"\bclub\s+yanka\b"],
                    "Denarius": [r"\bdenarius\b"],
                    # pull out "Mammoth Soaps" as scent maker?
                    "Iced Tea": [r"\biced?\s+tea\b"],
                    "King of Oud": [r"\bking\s+of\s+oud\b"],
                    "Dulci Tobacco": [r"\bdulci\s+tobacco\b"],
                    "Merchant of Tobacco": [r"\bmerchant\s+of\s+tobacco\b"],
                },
            ],
            "Zingari Man":
            [
                [r"\bzina?gari\b", r"\bzina?gari\s*man\b"],
                {
                    "Unscented": [r"\bunscented\b"],
                    "Barrel Proof": [r"\bbarrel\b"],
                    "Bon Monsieur": [r'\bbon\s+mons[ieu]+r\b'],
                    "Mousse Illuminee": [r"\bmouss?e?\s+il.+\b"],
                    "No. 1": [r"\bno.?\s*(?:one|1)\b"],
                    "The Blacksmith": [r"\b(?:the\s*)?blacksmith\b"],
                    "The Explorer": [r"\b(?:the\s*)?explorer\b"],
                    "The Gent": [r"\b(?:the\s*)?gent\b"],
                    "The Navigator": [r"\b(?:the\s*)?navigator\b"],
                    "The Nomad": [r"\b(?:the\s*)?nomad\b"],
                    "The Wanderer": [r"\b(?:the\s*)?w[a|o]nderer\b"],
                    "The Watchman": [r"\b(?:the\s*)?watchm[a|e]n\b"],

                },
            ],
    }

    @cached_property
    def _outliers(self):
        output = {}
        for primary_name, regexes in self._outliermap.items():
            for regex in regexes:
                output[regex] = primary_name
        return output


    @cached_property
    def _mapper(self):
        output = ({}, {})
        for brand, vals in self._raw.items():
            for brandRegex in vals[0]:
                output[0][brandRegex] = brand
                scentMap = output[1][brand] = {} 
                for scent, scentRegExes in vals[1].items():
                    for scentRegex in scentRegExes:
                        scentMap[scentRegex] = scent
                            
                
        return output
    
    def get_principal_name(self, name):
        brand = self.get_brand_and_scent(name)
        return f'{brand[0]} - {brand[1]}'
    
    def match_outlier(self, name):
        for regex in sorted(self._outliers.keys(), key=len, reverse=True):
            res = re.search(regex, name, re.IGNORECASE)
            if res:
                return self._outliers[regex]
        
        return None


    @lru_cache(maxsize=1024)
    def get_brand_and_scent(self, name) -> ():
        def prep_return(brand, scent):
            return (brand.strip().strip("-"), scent.strip().strip("-"))

        result = self.match_outlier(name)
        if result: return result

        name = self.preprocess(name)
        brandmap = self._mapper[0]
        for regex in sorted(brandmap.keys(), key=len, reverse=True):
            res = re.search(regex, name, re.IGNORECASE)
            if res:
                brand = brandmap[regex]
                pattern = re.compile(regex, re.IGNORECASE)
                scent = pattern.sub("", name)
                scentmap = self._mapper[1][brand]
                result = None
                for sregex in sorted(scentmap.keys(), key=len, reverse=True):
                    sres = re.search(sregex, scent, re.IGNORECASE)
                    if (sres):
                        result = scentmap[sregex]
                        break
                if result:
                    scent = result
                else:
                    scent = re.sub("^\s*-\s*", "", scent).strip()
                scent = self.postprocess(scent)
                result = prep_return(brand, scent)
                return result

        #if we didn't find a match, fallback to standard "Brand - Scent" structure
        pattern = re.compile(r'(?P<brand>[^-]+) - (?P<scent>[^-]+)')
        match = pattern.match(name)
        if match:
            return prep_return(match.group('brand'), match.group('scent'))
                

        return None

    # @lru_cache(maxsize=1024)
    # def get_scent(self, brand, name):
    #     val = self._mapper[1][brand]
    #     for alt_name_re in sorted(val.keys(), key=len, reverse=True):
    #         res = re.search(alt_name_re, name, re.IGNORECASE)
    #         if res:
    #             return val[alt_name_re]
    #     return None
    
    _preprocess_remove_patterns = [
        # remove usage counts -- e.g. "(4)" -- from the name
        r'\(\d+\)',
        # drop "- soap" suffix, etc.
        r'\s*-\s*(soap|cream|shaving soap|shave soap|premium shaving soap)',
        # drop "sample"
        r'\(?sample\)?',
        # drop (killed) and (almost gone)
        r'\((?:killed|almost gone)\)',
        # drop trailing "puck"
        r'puck$',
        #drop punction
        r"[\.\"]",
        #drop trailing apostrophe
        r"\'$",
    ]

    _postprocess_remove_patterns = [
        # drop anything in parens except: 
        #   (e) so we don't nuke B&M Mûir(e) Wood"
        #   (red), (green), (blue), (white) for the Proraso
        r"\((?!(?:e|red|green|blue|white)\))[^)]+\)",
        r"\bby$",
    ]
    
    def preprocess(self, name):
        # remove reddit links, converting "[sometext](somelink)"" into "sometext"
        name = re.sub(r"\[([^]]+)\]\([^)]+\)", r"\1", name)

        for pattern in self._preprocess_remove_patterns:
            p = re.compile(pattern, re.IGNORECASE)
            name = p.sub("", name)

        return name
    
    def postprocess(self, name):
        for pattern in self._postprocess_remove_patterns:
            p = re.compile(pattern, re.IGNORECASE)
            name = p.sub("", name)

        return name.strip()

if __name__ == "__main__":

    def grouped(comments) -> pd.DataFrame:
        raw_unlinked = {"original": [], "name": [], "user_id": [], "brand": [], "scent": []}
        sp = SoapAlternateNamer()
        matcher = SoapAlternateNamer()
        for comment in comments:
            if 'soap' in comment:
                entity_name = sp.preprocess(comment['soap'])
                if entity_name is not None:
                    bs = matcher.get_brand_and_scent(entity_name)
                    brand = scent = name = ''
                    if bs:
                        brand = bs[0]
                        scent = bs[1]
                        name = f"{brand} - {scent}"
                    raw_unlinked["original"].append(entity_name[0:50])
                    raw_unlinked["user_id"].append(comment["author"])
                    raw_unlinked["brand"].append(brand)
                    raw_unlinked["scent"].append(scent)
                    raw_unlinked["name"].append(name)

        usage = pd.DataFrame(raw_unlinked)
        # usage = usage.drop(columns=["user_id"])


        # remove nulls
        usage = usage.dropna(subset=["name"])
        # usage = usage.drop(columns=["user_id", "brand", "scent"])

        # sort
        # usage.sort_values(["name", "matched", "shaves", "unique users"], ascending=False, inplace=True)
        # df = df.groupby("name").agg({"user_id": ["count", "nunique"]}).reset_index()
        # df.columns = ["name", "shaves", "unique users"]
        # usage = usage.groupby(["name"])["original"].agg({"count"})
        usage = usage.groupby(["name", "brand", "scent"]).agg({"user_id": ["count", "nunique"]}).reset_index()

        usage = usage.sort_values(["name"], ascending=True)
        usage.columns = ["name", "brand", "scent", "shaves", "unique users"]
        usage = usage.drop(columns=["name"])
        return usage

        # enforce max entities
        # usage = usage.head(MAX_ENTITIES)

    def ungrouped(comments) -> pd.DataFrame:
        raw_unlinked = {"original": [], "user_id": [], "brand": [], "scent": []}
        sp = SoapAlternateNamer()
        matcher = SoapAlternateNamer()
        for comment in comments:
            if 'soap' in comment:
                entity_name = sp.preprocess(comment['soap'])
                if entity_name is not None:
                    bs = matcher.get_brand_and_scent(entity_name)
                    brand = scent = name = ''
                    if bs:
                        brand = bs[0]
                        scent = bs[1]
                        name = f"{brand} - {scent}"
                    raw_unlinked["original"].append(entity_name[0:50])
                    raw_unlinked["user_id"].append(comment["author"])
                    raw_unlinked["brand"].append(brand)
                    raw_unlinked["scent"].append(scent)

        usage = pd.DataFrame(raw_unlinked)
        usage = usage.drop(columns=["user_id"])

        usage = usage.sort_values(["brand", "scent"], ascending=True)
        return usage

        # enforce max entities
        # usage = usage.head(MAX_ENTITIES)

    pr = praw.Reddit("reddit")
    pl = SotdPostLocator(pr)
    target = datetime.date(2024, 1, 1)
    target2 = target - relativedelta(months=1)
    target3 = target - relativedelta(years=1)
    comments = pl.get_comments_for_given_month_staged(target)
    # print(len(comments))
    comments2 = pl.get_comments_for_given_month_staged(target2)
    # print(len(comments2))
    comments3 = pl.get_comments_for_given_month_staged(target3)
    # print(len(comments3))
    comments = comments + comments2 + comments3
    # print(len(comments))

    usage = grouped(comments)
    print(usage.to_markdown(index=False))
    # print(usage)
    
    print("\n")

