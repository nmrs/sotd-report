from collections import OrderedDict
from functools import cached_property, lru_cache
from unittest.mock import Base
from base_parser import BaseParser
import re


class BladeParser(BaseParser):
    """
    Amalgamate names
    """

    __raw = {
        "7 O'Clock - Permasharp": {"patterns": ["clock.*perm"]},
        "7 O'Clock - Sharpedge (Yellow)": {
            "patterns": ["clock.*sharp.*edg", "clock.*yellow"]
        },
        "7 O'Clock - Super Platinum (Black)": {
            "patterns": ["clock.*pla", "clock.*black", "gill.*black"]
        },
        "7 O'Clock - Super Stainless (Green)": {
            "patterns": [
                "clock.*sta",
                "clock.*green",
                "clock",
                "gil.*et.*super.*stain",
            ]
        },
        "AccuTec Pro Premium (GEM)": {"patterns": ["acc?utec"], "format": "GEM"},
        "Aeterna": {"patterns": ["aeter"]},
        "Astra Superior Platinum (Green)": {
            "patterns": [
                "astra.*plat",
                "astra.*green",
                "astra.*sp",
                "astra",
            ]
        },
        "Astra Superior Stainless (Blue)": {
            "patterns": [
                "astra.*sta",
                "astra.*blue",
                "astra.*ss",
            ]
        },
        "Bic Astor Stainless": {"patterns": ["bic.*(ast|stai)"]},
        "Bic Chrome": {"patterns": ["bic.*(chr|pla)", "bic"]},
        "Big Ben": {"patterns": ["big ben"]},
        "Boker": {"patterns": ["boker"]},
        "Bolzano": {"patterns": ["b(o|a)lzano"]},
        "Cartridge": {
            "patterns": ["twin.*pivot", "gil.*fusion", "gil.*labs"],
            "format": "Cartridge",
        },
        "Crystal": {"patterns": ["crystal"]},
        "Derby Blue Bird": {"patterns": ["blue.*bird"]},
        "Derby Concord": {"patterns": ["concord"]},
        "Derby Extra": {"patterns": ["derb.*extra", "derby"]},
        "Derby Extra Blue": {"patterns": ["derb.*blue"]},
        "Derby Premium": {"patterns": ["derb.*prem"]},
        "Dorco BB-20 (AC)": {"patterns": ["dorco.*bb*"], "format": "AC"},
        "Dorco ST-300": {"patterns": ["dorco.*st.*300", "dorco"]},
        "Dorco ST-301": {"patterns": ["dorco.*st.*301"]},
        "Durablade Sharp Titanium": {"patterns": ["durablade"]},
        "Dorco Titan": {"patterns": ["dorco.*titan"]},
        "Eddison Stainless": {"patterns": ["eddison"]},
        "Elios": {"patterns": ["elios"]},
        "Euromax": {"patterns": ["euromax"]},
        "Feather (DE)": {
            "patterns": [
                "feather",
                "feather.*hi.*st",
                "feather.*hs",
                r"feather\s*blade",
                "feather.*de",
            ]
        },
        "Feather FHS-1": {"patterns": ["fhs-1"], "format": "FHS"},
        "Feather Pro (AC)": {
            "patterns": ["feather.*pro", "feather.*a.*c.*"],
            "format": "AC",
        },
        "Feather Pro Light (AC)": {"patterns": ["feather.*light"], "format": "AC"},
        "Feather Pro Super (AC)": {
            "patterns": ["feather.*super", r"pro\s*super"],
            "format": "AC",
        },
        "Feather ProGuard (AC)": {"patterns": ["feather.*guard"], "format": "AC"},
        "Feather Soft Guard (AC)": {"patterns": ["feather.*soft"], "format": "AC"},
        "GEM Blue Star": {"patterns": ["gem.*blue.*star"], "format": "GEM"},
        "Gillette 365": {"patterns": [r"\b365\b"]},
        "Gillette London Bridge": {"patterns": ["london\s*bridge"]},
        "Gillette Minora": {"patterns": ["minora", "minora.*plat"]},
        "Gillette Nacet": {"patterns": ["nan*cet"]},
        "Gillette Perma-Sharp": {"patterns": [r"perma\s*-*sharp"]},
        "Gillette Platinum": {"patterns": ["gil.*pla"]},
        "Gillette Rubie": {"patterns": ["rubie"]},
        "Gillette Silver Blue": {
            "patterns": [
                "gsb",
                "Gill.*sil.*blue",
                "silver.*blue",
                "gill.*sb",
                "gill.*blu.*sil",
            ]
        },
        "Gillette Spoiler": {"patterns": ["gil.*et.*spoil"]},
        "Gillette Sputnik": {"patterns": ["sputnik"]},
        "Gillette Wilkinson Sword": {"patterns": ["gil.*et.*wilk.*swor"]},
        "Gillette Winner": {"patterns": ["gil.*winn"]},
        "Kai (DE)": {"patterns": ["kai", "kai.*sta", "kai.*ss"]},
        "Kai Captain Blade (AC)": {
            "patterns": ["kai.*blade", r"kai captain\s*$", "kai.*cap"],
            "format": "AC",
        },
        "Kai Captain Sharpblade (AC)": {"patterns": ["kai.*sharp"], "format": "AC"},
        "Kai Captain Titan Mild (AC)": {
            "patterns": ["kai.*titan", "kai.*cap.*mild"],
            "format": "AC",
        },
        "Kai Captain Titan Mild Protouch (AC)": {
            "patterns": ["kai.*pro\s*touch"],
            "format": "AC",
        },
        "King C Gillette": {"patterns": ["king.*c.*gil.*et", "gil.*et.*king.*c"]},
        "Ladas": {"patterns": ["lada"]},
        "Leaf": {"patterns": ["leaf"]},
        "Lord Classic": {"patterns": ["lord.*cla"]},
        "Lord Cool": {"patterns": ["lord.*cool"]},
        "Lord Super Stainless": {"patterns": ["lord.*sup"]},
        "Kismet Hair Shaper": {"patterns": ["kismet"], "format": "Hair Shaper"},
        "Merkur Super Platinum": {"patterns": ["merkur"]},
        "Mühle": {"patterns": ["m(u|ü)hle"]},
        "Personna Hair Shaper": {
            "patterns": ["personn.*hair.*shap"],
            "format": "Hair Shaper",
        },
        "Personna Platinum": {"patterns": ["personn.*plat"]},
        "Personna GEM PTFE": {
            "patterns": [
                "(person|gem).*(ptfe|pfte)",
                "gem by personna",
                "(ptfe|pfte).*(person|gem)",
                "(person|ptfe).*gem",
                "ptfe",
                "gem",  # matching just GEM to this blade per guidance here: https://www.reddit.com/r/Wetshaving/comments/19a43q7/comment/kil95r8/
            ],
            "format": "GEM",
        },
        "Personna GEM Stainless": {
            "patterns": ["(personna)*gem.*stainless", "gem.*ss"],
            "format": "GEM",
        },
        "Personna Injector": {
            "patterns": ["(person|personna).*(inject|injector)"],
            "format": "Injector",
        },  # unecessarily long to ensure priority of checking
        "Personna Med Prep": {"patterns": ["person.*med"]},
        "Personna 74": {"patterns": [r"p(?:ersonn*a)?\s*74", "pseventy-four", "p74"]},
        "Personna Red": {"patterns": ["personn*a.*red"]},
        "Personna Stainless": {
            "patterns": ["personn*a.*stainless", "personn*a.*super"]
        },
        "Personna Blue": {
            "patterns": ["personn*a.*blue", "personn*a.*c.*c", "personn*a"]
        },
        "Polsilver": {"patterns": ["pol(i|-)*silver", "polsiver"]},
        "Rapira Super Stainless": {"patterns": ["rapira.*stain", "rapira.*ss"]},
        "Rapira Platinum Lux": {"patterns": ["rapira"]},
        "Rapira Swedish": {"patterns": ["rapira.*swe"]},
        "RK Stainless": {"patterns": ["rk"]},
        "Rockwell": {"patterns": ["rockwell"]},
        "Sapphoo Red (AC)": {"patterns": ["sapp?hoo(\s*red)?"]},
        "Schick Stainless (DE)": {"patterns": ["schick.*s(?:tainles)*s"]},
        "Schick Injector": {"patterns": ["schick"], "format": "Injector"},
        "Schick Proline (AC)": {"patterns": ["proline"], "format": "AC"},
        "Shark Chrome": {"patterns": ["shark.*chr"]},
        "Shark Stainless": {"patterns": ["shark"]},
        "Shark Platinum": {"patterns": ["shark.*pla"]},
        "Shaving Revolution Platinum": {"patterns": ["shaving\s*revolution"]},
        "Silver Star - Super Stainless": {"patterns": ["silver.*star.*stain"]},
        "Super-Max Blue Diamond": {"patterns": ["super.*max.*(?:blu)*.*dia"]},
        "Super-Max Platinum": {"patterns": ["super.*max.*plat"]},
        "Super-Max Super Stainless": {"patterns": ["super.*max.*stai"]},
        "Tatara": {"patterns": ["tatara"]},
        "Tatra Platinum": {"patterns": ["tatra"]},
        "Ted Pella Injector": {"patterns": ["pella"], "format": "Injector"},
        "Ted Pella PTFE": {"patterns": ["pella.*ptfe"], "format": "GEM"},
        "Tiger Platinum": {"patterns": ["tiger"]},
        "Treet Black Beauty": {"patterns": ["treet\s*bla", "treet.*carb"]},
        "Treet Classic": {"patterns": ["treet.*classic"]},
        "Treet Dura Sharp": {"patterns": ["treet.*dura.*shar"]},
        "Treet GEM": {"patterns": ["treet.*gem", "gem.*treet"]},
        "Treet New": {"patterns": ["treet.*new"]},
        "Treet New Edge": {"patterns": ["treet.*new.*edge"]},
        "Treet New Steel": {"patterns": ["treet.*new.*steel"]},
        "Treet Platinum": {"patterns": ["treet.*pla"]},
        "Viking's Sword Stainless": {"patterns": ["vik.*swor.*sta"]},
        "Wilkinson Sword": {"patterns": ["wilk.*swor", "wilkinson"]},
        "Wizamet": {"patterns": ["wizamet", "wiz"]},
        "Voskhod": {"patterns": ["vokshod", "voskhod", "voshk"]},
    }

    # @lru_cache(maxsize=1024)
    # def get_principal_name(self, name):
    #     stripped = self.remove_digits_in_parens(name)
    #     return super().get_principal_name(stripped)

    @cached_property
    def __mapper(self):
        output = {}
        for name, property_map in self.__raw.items():
            for pattern in property_map["patterns"]:
                format = property_map["format"] if "format" in property_map else "DE"
                output[pattern] = {"name": name, "format": format}
        return output

    # def extract_uses(input_string):
    #     match = re.search(r"[[(](\d{1,4})[)\]]", input_string)
    #     if match:
    #         return int(match.group(1))

    #     return None

    @lru_cache(maxsize=None)
    def _get_value(self, input_string: str, field: str) -> str:
        return self.__get_value(input_string, field)
        # input_string = self.remove_digits_in_parens(input_string)
        # return self.__get_value(input_string, field)

    @lru_cache(maxsize=None)
    def __get_value(self, input_string, field):
        regexes = sorted(self.__mapper.keys(), key=len, reverse=True)
        for alt_name_re in regexes:
            if re.search(alt_name_re, input_string, re.IGNORECASE):
                property_map = self.__mapper[alt_name_re]
                if field in property_map:
                    return self.__mapper[alt_name_re][field]
                # else:
                #     raise ValueError(f"Unsupported field: {field}")
        return None


if __name__ == "__main__":
    # ban = BladeAlternateNamer()
    # print(ban.get_principal_name('Gillette 7 O\'Clock Super Platinum'))

    print(re.search("feather.*(?:de)?", "Feather (de)", re.IGNORECASE))
