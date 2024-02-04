import datetime
from functools import cached_property, lru_cache

import pandas as pd
import praw

from sotd_collator.base_alternate_namer import BaseAlternateNamer
import re

from sotd_collator.sotd_post_locator import SotdPostLocator


class SoapMatcher():
    """
    Amalgamate names
    """

    _raw = {
            "345 Soap Co.":
            [
                [r"\b345\b"],
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
                [r"\bcatie'?s?\b", r"\bcb\b"],
                {
                },
            ],
            "Cella":
            [
                [r"\bcella\b"],
                {
                },
            ],
            "Central Texas Soaps":
            [
                [r"\bcentral\s+texas\b"],
                {
                },
            ],
            "Chicago Grooming Co.":
            [
                [r"\bchicago\s+grooming\b", r"\bc\s*g\b"],
                {
                },
            ],
            "Chiseled Face":
            [
                [r"\bchiseled\s*face\b"],
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
                [r"\bdg\b",r"\bdeclar.*groom.*\b", r"\bdeclar.*shaving\b"],
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
            "First Line Shave":
            [
                [r"\bfirst\s+line\s+shaves?\b"],
                {
                },
            ],
            "Gentleman's Nod":
            [
                [r"\bgentlem(?:a|e)n'?s?\s+nod\b"],
                {
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
            "Hendrix Classics & Co":
            [
                [r"\bhendrix\s+classics?\b", r"\bhendrex\s+c(?:&|and|\+)?c\b", r"\bhc(?:&|and|\+)?c\b"],
                {
                },
            ],
            "HAGS":
            [
                [r"\bhags\b"],
                {
                },
            ],
            "The Holy Black":
            [
                [r"\bholy\s+black\b"],
                {
                },
            ],
            "La Toja":
            [
                [r"\b(?:la\s+)?toja\b"],
                {
                },
            ],
            "House of Mammoth":
            [
                [r"\bhouse\s+of\s+mammoth\b", r"\bhoue\s+of\s+mammoth\b", r"\bhom\b", r"\bmammoth\b"],
                {
                },
            ],
            "London Razors":
            [
                [r"\blondon\s+razors?\b"],
                {
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
                [r"\bmacduff'?s?\b"],
                {
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
                },
            ],
            "Mickey Lee Soapworks":
            [
                [r"\bmickey\s+lee\b"],
                {
                },
            ],
            "Mike's Natural Soaps":
            [
                [r"\bmike'?s\s+natural\b"],
                {
                },
            ],
            "Mitchell's Wool Fat":
            [
                [r"\bmwf\b"],
                {
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
                [r"\bnoble\s*otter\b"],
                {
                },
            ],
            "Noble Otter":
            [
                [r"\bmurphy\s+(?:&|and|\+)\s+mcneill?\b"],
                {
                },
            ],
            "Oaken Lab":
            [
                [r"\boaken\b"],
                {
                },
            ],
            "Proraso":
            [
                [r"\bproraso\b"],
                {
                },
            ],
            "RazoRock":
            [
                [r"\brazorock\b"],
                {
                },
            ],
            "Rock Bottom Soap":
            [
                [r"\brock\s+bottom\b"],
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
                },
            ],
            "Spearhead Shaving Co.":
            [
                [r"\bspearhead\b", r"\bsperahead\b",r"\bseaforth\b", r"\bsea\s+iced?\s+lime\b"],
                {
                    'Seaforth! Spiced': [r'\bseaforth\b[\s!]*\bspiced\b']
                },
            ],
            "Stirling":
            [
                [r"\bstirling\b"],
                {
                },
            ],
            "Summer Break Soaps":
            [
                [r"\bsummer\s*break\s*soaps\b"],
                {
                },
            ],
            "Wholly Kaw":
            [
                [r"\wholly kaw\b"],
                {
                },
            ],
            "Talent Soap Factory":
            [
                [r"\btalent\s*soap\b"],
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
                [r"\bwet\s+shaving\b"],
                {
                },
            ],
            "Zingari Man":
            [
                [r"\bzina?gari\b"],
                {
                },
            ],
    }

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
    
    def preprocess(self, name):
        name = re.sub(r"\[([^]]+)\]\([^)]+\)", r"\1", name)
        name = re.sub(r'\(\d+\)', '', name)
        pattern = re.compile(r'\s*-\s*(soap|cream)', re.IGNORECASE)
        name = pattern.sub('', name)
        return name
    
    @lru_cache(maxsize=1024)
    def get_brand(self, name):
        name = self.preprocess(name)
        mapper = self._mapper[0]
        for regex in sorted(mapper.keys(), key=len, reverse=True):
            res = re.search(regex, name, re.IGNORECASE)
            if res:
                return mapper[regex]

        return None
    
    def get_scent(self, brand, name):
        mapper = self._mapper[1][brand]
        for regex in sorted(mapper.keys(), key=len, reverse=True):
            res = re.search(regex, name, re.IGNORECASE)
            if res:
                return mapper[regex]
            
        return None

    def get_scent_fallback(self, name):
        mapper = self._mapper[0]
        for regex in sorted(mapper.keys(), key=len, reverse=True):
            regex = fr"(?:{regex})[\s\-:]*(.*)$"
            print(regex)
            res = re.match(regex, name, re.IGNORECASE)
            if res:
                return res.group(1)

        return None

    @lru_cache(maxsize=1024)
    def get_scent(self, brand, name):
        val = self._mapper[1][brand]
        for alt_name_re in sorted(val.keys(), key=len, reverse=True):
            res = re.search(alt_name_re, name, re.IGNORECASE)
            if res:
                return val[alt_name_re]
        return None

    # def get_scent_name(self, principal_name):




    # @lru_cache(maxsize=1024)
    # def get_principal_name(self, name):
    #     stripped = self.remove_digits_in_parens(name)
    #     return super().get_principal_name(stripped)

if __name__ == "__main__":

    pr = praw.Reddit("reddit")
    pl = SotdPostLocator(pr)
    target = datetime.date(2024, 1, 1)
    comments = pl.get_comments_for_given_month_staged(target)

    raw_unlinked = {"name": [], "user_id": [], "brand": []}
    sp = SoapMatcher()
    matcher = SoapMatcher()
    for comment in comments:
        if 'soap' in comment:
            entity_name = sp.preprocess(comment['soap'])
            if entity_name is not None:
                brand = matcher.get_brand(entity_name)
                raw_unlinked["name"].append(entity_name)
                raw_unlinked["user_id"].append(comment["author"])
                raw_unlinked["brand"].append(brand if brand is not None else '')    

    usage = pd.DataFrame(raw_unlinked)
    usage = usage.drop(columns=["user_id"])


    # remove nulls
    # usage.dropna(subset=["name"], inplace=True)

    # sort
    # usage.sort_values(["name", "matched", "shaves", "unique users"], ascending=False, inplace=True)
    usage.sort_values(["brand", "name"], ascending=False, inplace=True)

    # enforce max entities
    # usage = usage.head(MAX_ENTITIES)

    print(usage.to_markdown(index=False))
    print("\n")
