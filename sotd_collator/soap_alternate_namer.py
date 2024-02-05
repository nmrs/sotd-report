import datetime
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

    _outliermap = {
        ("Spearhead Shaving Co.", "Sea Ice Lime"): [r"\bsea\s+ice\s+lime\b"],
        ("West Coast Shaving","Grapefroot"): [r'\bcbubs\/WCS\s+grapefroot\b'],
        ("Declaration Grooming", "Cerberus"): [r"\bcerberus\b"],
        ("Maurer & Wirtz", "Tabac"): ["tabac"]
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
                },
            ],
            "Ariana & Evans":
            [
                [r"\bariann?a\s*(?:&|and|\+)\s*evan(?:s)?\b", r"\ba\s*(?:&|and|\+)?\s*e\b"],
                {
                },
            ],
            "Arko":
            [
                [r"\barko\b"],
                {
                },
            ],
            "Azalea City Suds":
            [
                [r"\bazalea\s+city\b"],
                {
                },
            ],
            "Barrister & Mann":
            [
                [r"\bb\s*?(?:&|and|\+)?\s*?m\b", r"\bbar\S*\s*?(?:&|and|\+)?\s*?man\S*\b"],
                {
                    "Mûir(e) Wood": [r"muire?"],
                    "Nocturne": [r"nocturne"],
                    "Nordost": [r"nordost"],
                    "Paganini's Violin": [r"nordost"],
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
                [r"\bblack\s+ship\b"],
                {
                },
            ],
            "Catie's Bubbles":
            [
                [r"\bcatie'?s?\s+bubbles\b", r"\bcb\b"],
                {
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
                 r"chicago\s+grooming\s+co\.?\/xicano\b"],
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
                [r"\bchiseled\s*face\b", r"\bchiseled\s*face\s+groom(?:ing|atorium)\b"],
                {
                    # "Trade Winds": [r"\btrade\s+winds\s+"]
                },
            ],
            "The Club":
            [
                [r"\bthe\s+club\b"],
                {
                },
            ],
            "Col. Ichabod Conk":
            [
                [r"\bcol.?\s+(?:ichabod\s+)?conk\b"],
                {
                },
            ],
            "Declaration Grooming":
            [
                [r"\bdg\b",r"\bdeclaration\s+grooming\b", r"\bdeclaration\s+shaving\b"],
                {
                    "Peaches + Scream": [r"\bpeaches\b"]
                },
            ],
            "Declaration Grooming / Chatillon Lux":
            [
                [r"\bdg\/cl\b",r"\bdeclaration\s+grooming\s*\/\s*chatillon\s+lux\b",
                 r"\bchatillon\s+lux\s*(?:and|\/)\s*declaration\s+grooming\b"],
                {
                },
            ],
            "Denton Majik":
            [
                [r"\bdenton\s*majic?k?\b"],
                {
                },
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
                [r"\bd\.?r\.?\s+harris\b"],
                {
                },
            ],
            "Dr. Jon's":
            [
                [r"\bdr.?\s+jon'?s?\b"],
                {
                },
            ],
            "Eleven":
            [
                [r"\beleven\b"],
                {
                },
            ],
            "Elysian":
            [
                [r"\belysian\b"],
                {
                },
            ],
            "Fine Accoutrements":
            [
                [r"\bfine\s+accoutrements\b", r"\bfine\b"],
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
                    "Empire State of Mind": [r"\bempire\s+state\b"]
                },
            ],
            "Henri et Victoria":
            [
                [r"\bhenri\s+et\s+victoria\b"],
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
                },
            ],
            "House of Mammoth":
            [
                [r"\bhouse\s+of\s+mammoth\b", r"\bhoue\s+of\s+mammoth\b", r"\bhom\b", r"\bmammoth\b"],
                {
                    "Fu Dao": [r"\bfu\s+dao\b"],
                    "Hygge": [r"\bhygge\b"],
                    "Indigo": [r"\bindigo\b"],
                    "Uitwaaien": [r"\bui?twaaien\b"],
                    "Shire": [r"\bshire\b"],
                    "Voices": [r"\bvoices\b"],
                },
            ],
            "Imaginary Authors":
            [
                [r"\bimaginary\s+authors\b", r"\bimaginary\s+authors\/noble\s+otter\b"],
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
            "Maurer & Wirtz":
            [
                [r"\bmaurer\s+(?:&|and|\+)?\s+wirtz\b", r"\btabac\b"],
                {
                },
            ],
            "MacDuff's Soap Company":
            [
                [r"\bma?cduff'?s?\b", r"\bma?cduff'?s?\s+soap\s+co(?:mpany)?\b"],
                {
                    "American Vintage": [r"\bamerican\s+vintage\b"],
                    "Autumn Cabin": [r"\bautumn\s+cabin\b"],
                    "Santa's Cheer": ["santa"]
                },
            ],
            "Martin de Candre":
            [
                [r"\bmartin\s+de\s+candre\b"],
                {
                },
            ],
            "Master Soap Creations":
            [
                [r"\bmaster\s+soap\s+creations\b", r"\bmsc\b"],
                {
                    "Light Blue": [r"light\s+blue"]
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
                [r"\bmwf\b"],
                {
                    "Shaving Soap": [".*"]
                },
            ],
            "Moon Soaps":
            [
                [r"\bmoon\s*soaps\b"],
                {
                },
            ],
            "Murphy & McNeil":
            [
                [r"\bmurphy\s+(?:&|and|\+)\s+mcneill?\b"],
                {
                },
            ],
            "Noble Otter":
            [
                [r"\bnoble\s*otter\b", r"^\bno\b"],
                {
                    "Hamami": ["hamami"],
                    "Neon Sun": [r"\bneon\s+sun\b"],
                    "The Noir Et Vanille": [r"\bnoir\s+et\s+vanille\b", r"\btnev\b"],
                    "Orbit": [r"\borbit\b"],
                },
            ],
            "Oaken Lab":
            [
                [r"\boaken\s+lab\b"],
                {
                },
            ],
            "Pré de Provence":
            [
                [r"\bpr(?:é|e)\s+de\s+Provence\b"],
                {
                },
            ],
            "Proraso":
            [
                [r"\bproraso\b"],
                {
                    "Aloe and Vitamin E (Blue)": ["aloe", "blue", "protective"],
                    "Eucalyptus Oil and Menthol (Green)": ["eucalyptus", "menthol", "green"],
                    "Green Tea and Oat Sensitive Skin (White)" : ["green tea", r"\boat\b", "sensitive", "white"],
                    "Sandalwood with Shea Butter (Red)": ["sandalwood", "red"],
                },
            ],
            "RazoRock":
            [
                [r"\brazorock\b"],
                {
                },
            ],
            "Red House Farm":
            [
                [r"\bred\s+house\s+farms?\b"],
                {
                    "Nine Days Up Nort": ["up\s+nort"]
                },
            ],
            "Rock Bottom Soap":
            [
                [r"\brock\s+bottom\s+soap\b"],
                {
                },
            ],
            "Saponificio Varesino":
            [
                [r"\bsaponificio\s+varesino\b"],
                {
                },
            ],
            "Shannon's Soaps":
            [
                [r"\bshannon(?:\')?(?:s)?\s*soap(?:s)?\b"],
                {
                },
            ],
            "Southern Witchcrafts":
            [
                [r"\bsouthern\s*witchcraft(?:s)?\b"],
                {
                    "Grave Fruit": [r"grave\s*fruit"]
                },
            ],
            "Spearhead Shaving Co.":
            [
                [r"\bspearhead\b", r"\bsperahead\b", r"spearhead\s+soaps", r"spearhead\s+seaforth\b"],
                {
                    'Black Watch': [r"\bblack\s*watch\b"],
                    'Seaforth! Spiced': [r'\bseaforth\b[\s!]*\bspiced\b', "spice"],
                },
            ],
            "Stirling":
            [
                [r"\bstirling\b", r"\bstirling\s+soap\s+(?:co(?:mpany)?)?\b"],
                {
                    "Barbershop": [r"\bbarbershop\b"],
                    "Margaritas in the Arctic": [r"\bmargaritas\s+in\s+the\s+arc?tic\b"],
                    "Electric Sheep": [r"electric\s+shr?eep"]
                },
            ],
            "Stone Cottage Soapworks ":
            [
                [r"\bstone\s+cottage(?:\s+(?:soaps?|soapworks?|shaving))?\b"],
                {
                },
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
                    "Woodshop": [r"\bwood\s*shop\b"],
                },
            ],
            "Summer Break Soaps / London Razors":
            [
                [r"\blondon\s+razors?\b", r"\bsummer\s+break.*london\s+razors", 
                 r"\blondon\s+razors.*summer\s+break(?:\s+soaps)?\b"],
                {
                    "But first... Coffee": ['first\s*coffee'],
                    "Coffee & Contemplation": ['contemplation'],
                },
            ],
            "Wholly Kaw":
            [
                [r"\wholly kaw\b"],
                {
                    "1869 Timmermann Red Label": [r"\b1869\s+red\s+label\b"],
                },
            ],
            "Talent Soap Factory":
            [
                [r"\btalent\s+soap\s+factory\b"],
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
            "Zingari Man":
            [
                [r"\bzina?gari\b", r"\bzina?gari\s+man\b"],
                {
                    "Unscented": [r"\bunscented\b"],
                    "Barrel Proof": [r"\bbarrel\b"],
                    "Bon Monsieur": [r'\bbon\s+mons[ieu]+r\b'],
                    "Mousse Illuminee": [r"\bmouss?e?\s+il.+\b"],
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
                    scent = self.scentFixup(brand, scent)
                scent = self.postprocess(scent)
                return (brand.strip(), scent.strip())

        return None

    @lru_cache(maxsize=1024)
    def get_scent(self, brand, name):
        val = self._mapper[1][brand]
        for alt_name_re in sorted(val.keys(), key=len, reverse=True):
            res = re.search(alt_name_re, name, re.IGNORECASE)
            if res:
                return val[alt_name_re]
        return None
    
    _preprocess_remove_patterns = [
        # remove usage counts -- e.g. "(4)" -- from the name
        r'\(\d+\)',
        # drop "- soap" suffix, etc.
        r'\s*-\s*(soap|cream|shaving soap|shave soap|premium shaving soap)',
        # drop "sample"
        r'\(?sample\)?',
        # drop (killed) and (almost gone)
        r'\((?:killed|almost gone)\)',
        #drop punction
        r'[\."]',
    ]

    _postprocess_remove_patterns = [
        # drop anything in parens (except "(e)" so we don't nuke B&M Mûir(e) Wood")
        r"\((?!e\))[^)]+\)",
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

        return name

    def scentFixup(self, brand, scent):
        if brand == 'Zingari Man':
            if not scent.lower().startswith("the "):
                return "The " + scent
            else:
                return scent
        return scent

if __name__ == "__main__":
    pr = praw.Reddit("reddit")
    pl = SotdPostLocator(pr)
    target = datetime.date(2024, 1, 1)
    comments = pl.get_comments_for_given_month_staged(target)
    raw_unlinked = {"name": [], "user_id": [], "brand": [], "scent": []}
    sp = SoapAlternateNamer()
    matcher = SoapAlternateNamer()
    for comment in comments:
        if 'soap' in comment:
            entity_name = sp.preprocess(comment['soap'])
            if entity_name is not None:
                brand = matcher.get_brand_and_scent(entity_name)
                raw_unlinked["name"].append(entity_name[0:50])
                raw_unlinked["user_id"].append(comment["author"])
                raw_unlinked["brand"].append(brand[0][0:40] if brand is not None and brand[0] is not None else '')
                raw_unlinked["scent"].append(brand[1][0:40] if brand is not None and brand[1] is not None else '')

    usage = pd.DataFrame(raw_unlinked)
    usage = usage.drop(columns=["user_id"])


    # remove nulls
    # usage.dropna(subset=["name"], inplace=True)

    # sort
    # usage.sort_values(["name", "matched", "shaves", "unique users"], ascending=False, inplace=True)
    usage = usage.sort_values(["brand", "scent", "name"], ascending=True)

    # enforce max entities
    # usage = usage.head(MAX_ENTITIES)

    print(usage.to_markdown(index=False))
    
    print("\n")

