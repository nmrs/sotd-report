from abc import ABC, abstractmethod
import re
from functools import lru_cache, cached_property
from typing import Dict


class BaseBrushParsingStrategy(ABC):
    pass
    # @abstractmethod
    # def get_property_map(input_string: str) -> dict[str, str]:
    #     return {}

    _fibers = {
        "Boar": r"\b(boar|shoat)\b",
        "Synthetic": r"(timber|tux|mew|silk|synt|synbad|2bed|captain|cashmere|faux.*horse|black.*(magic|wolf)|g4|boss|st-?1|trafalgar|t[23]|kong|hi\s*brush)",
        "Horse": "(horse)",
        "Mixed Badger/Boar": "(mix|mixed|mi(s|x)tura?|badg.*boar|boar.*badg)",
        "Badger": r"(hmw|high.*mo|(2|3|two|three)\s*band|shd|badger|silvertip|super|gelo|bulb|fan|finest|best)",
    }

    @abstractmethod
    def get_property_map(self, input_string: str) -> dict[str, str]:
        return None

    @lru_cache(maxsize=None)
    def get_fiber(self, input_string):
        for fiber, pattern in self._fibers.items():
            if re.search(pattern, input_string, re.IGNORECASE):
                return fiber
        return None

    def get_knot_size(self, input_string):
        detectors = [
            r"(\d{2})x\d{2}\s*mm",
            r"(\d{2})x\d{2}\s*",
            r"(\d{2})\s*mm",
        ]
        for d in detectors:
            detector = re.compile(d, re.IGNORECASE)
            res = detector.findall(input_string)
            for match in res:
                # num_mm = int(re.search(r"\d+", match).group(0))
                num_mm = int(match)
                if num_mm < 18 or num_mm > 40:
                    # probably a mistake, these are outside the usual brush sizes
                    continue
                return f"{num_mm}mm"

        # known_sizes = {
        #     "T1": {"patterns": ["simp.*t1"], "knot size": "23mm"},
        #     "T2": {"patterns": ["simp.*t2"], "knot size": "24mm"},
        #     "T3": {"patterns": ["simp.*t3"], "knot size": "26mm"},
        #     "CH1": {"patterns": ["simp.*ch1", "chubby\s*1"], "knot size": "22mm"},
        #     "CH2": {"patterns": ["simp.*ch2", "chubby\s*1"], "knot size": "26mm"},
        #     "CH3": {"patterns": ["simp.*ch3", "chubby\s*1"], "knot size": "29mm"},
        # }
        # for data in known_sizes.values():
        #     for pattern in data["patterns"]:
        #         if re.search(pattern, input_string, re.IGNORECASE):
        #             return data["knot size"]

        return None


class DeclarationGroomingParsingStrategy(BaseBrushParsingStrategy):

    _raw = {
        "Declaration Grooming": {
            "B1": {
                "patterns": [r"B1(\.\s|\.$|\s|$)"],
            },
            "B2": {
                "patterns": [r"B2(\.\s|\.$|\s|$)"],
            },
            "B3": {
                "patterns": [r"B3(\.\s|\.$|\s|$)"],
            },
            "B4": {
                "patterns": ["B4"],
            },
            "B5": {
                "patterns": ["B5"],
            },
            "B6": {
                "patterns": ["B6"],
            },
            "B7": {
                "patterns": ["B7"],
            },
            "B8": {
                "patterns": ["B8"],
            },
            "B9A+": {
                "patterns": [r"B9A\+", "b9.*alpha.*plus"],
            },
            "B9A": {
                "patterns": ["B9A", "b9.*alpha"],
            },
            "B9B": {
                "patterns": ["B9B", "b9.*bravo"],
            },
            "B10": {
                "patterns": ["b10"],
            },
            "B11": {
                "patterns": ["b11"],
            },
            "B12": {
                "patterns": ["b12"],
            },
            "B13": {
                "patterns": ["b13"],
            },
            "B14": {
                "patterns": ["b14"],
            },
            "B15": {
                "patterns": ["b15"],
            },
            "B16": {
                "patterns": ["b16"],
            },
            "B17": {
                "patterns": ["b17"],
            },
            "B18": {
                "patterns": ["b18"],
            },
        },
        "Zenith": {
            "B7": {
                "patterns": ["zenith.*b0?7"],
                "fiber": "Boar",
                "knot size": "24mm",
            },
            "B8": {
                "patterns": ["zenith.*b8"],
                "fiber": "Boar",
                "knot size": "28mm",
            },
            "B16": {
                "patterns": ["zenith.*b16"],
                "fiber": "Boar",
                "knot size": "24mm",
            },
        },
    }

    @cached_property
    def _pattern_map(self):
        result = {}
        for brand, models in self._raw.items():
            for model, data in models.items():
                for pattern in data["patterns"]:
                    fiber = "Badger"
                    if "fiber" in data:
                        fiber = data["fiber"]
                    result[pattern] = {
                        "brand": brand,
                        "name": f"{brand} {model}",
                        "fiber": fiber,
                    }
                    if "knot size" in data:
                        result[pattern]["knot size"] = data["knot size"]
                    else:
                        result[pattern]["knot size"] = "28mm"

        return result

    @lru_cache(maxsize=None)
    def get_property_map(self, input_string: str) -> dict[str, str]:
        map = self._pattern_map
        for alt_name_re in sorted(map.keys(), key=len, reverse=True):
            if re.search(alt_name_re, input_string, re.IGNORECASE):
                result = map[alt_name_re]
                knot_size = self.get_knot_size(input_string)
                if knot_size:
                    result["knot size"] = knot_size
                return result
        return None


class KnownBrushStrategy(BaseBrushParsingStrategy):

    _raw = {
        "Hand Lather": {
            "": {
                "patterns": [r"^\s*hands*\s*$", "hand.*lather"],
                "fiber": "Hand",
            },
        },
        "Omega": {
            "Hi-Brush Synthetic": {
                "patterns": ["hi-*brush", "omega.*syn"],
                "fiber": "Synthetic",
            },
            "Proraso Professional": {
                "patterns": [
                    "proraso.*pro",
                    "omega.*proraso",
                    "proraso.*omega",
                ],
                "fiber": "Boar",
                "knot size": "28mm",
            },
            "10048": {
                "patterns": ["omega.*(pro)*.*48"],
                "fiber": "Boar",
                "knot size": "28mm",
            },
            "10049": {
                "patterns": ["omega.*(pro)*.*49"],
                "fiber": "Boar",
                "knot size": "26mm",
            },
            "10098": {
                "patterns": ["10098"],
                "fiber": "Boar",
                "knot size": "27mm",
            },
            "11047": {
                "patterns": ["11047"],
                "fiber": "Mixed Badger/Boar",
                "knot size": "22mm",
            },
            "11126": {
                "patterns": ["11126"],
                "fiber": "Boar",
                "knot size": "24mm",
            },
            "11137": {
                "patterns": ["11137"],
                "fiber": "Boar",
                "knot size": "24mm",
            },
            "20102": {
                "patterns": ["20102"],
                "fiber": "Boar",
                "knot size": "28mm",
            },
            "20106": {
                "patterns": ["20106"],
                "fiber": "Boar",
                "knot size": "28mm",
            },
            "80005": {
                "patterns": ["80005"],
                "fiber": "Boar",
                "knot size": "24mm",
            },
            "EVO Sythetic": {
                "patterns": ["omega.*evo", "evo.*omega"],
                "fiber": "Synthetic",
            },
            "Special Veteran - E1860": {
                "patterns": ["omega.*evo.*e1860", "e1860"],
                "fiber": "Synthetic",
                "knot size": "28mm",
            },
        },
        "RazoRock": {
            "Monster": {
                "patterns": [r"razo.*monster"],
                "fiber": "Synthetic",
                "knot size": "26mm",
            },
            "Big Bruce": {
                "patterns": [r"razo.*big.*bruce"],
                "fiber": "Synthetic",
                "knot size": "26mm",
            },
            "Bruce": {
                "patterns": [r"razo.*bruce"],
                "fiber": "Synthetic",
                "knot size": "24mm",
            },
        },
        "Semogue": {
            "620": {
                "patterns": [r"semogue\s*620"],
                "fiber": "Boar",
                "knot size": "21mm",
            },
            "820": {
                "patterns": [r"semogue\s*820"],
                "fiber": "Boar",
                "knot size": "22mm",
            },
            "830": {
                "patterns": ["semogue.*830"],
                "fiber": "Boar",
                "knot size": "22mm",
            },
            "1250": {
                "patterns": ["semogue.*1250"],
                "fiber": "Boar",
                "knot size": "22mm",
            },
            "1305": {
                "patterns": ["semogue.*1305"],
                "fiber": "Boar",
                "knot size": "21mm",
            },
            "1438": {
                "patterns": ["semogue.*1438"],
                "fiber": "Boar",
                "knot size": "21mm",
            },
            "1800": {
                "patterns": ["semogue.*1800"],
                "fiber": "Boar",
                "knot size": "22mm",
            },
            "2000": {
                "patterns": ["semogue.*2000"],
                "fiber": "Boar",
                "knot size": "24mm",
            },
            "2015": {
                "patterns": ["semogue.*2015"],
                "fiber": "Badger",
                "knot size": "22mm",
            },
            "2020": {
                "patterns": ["semogue.*2020"],
                "fiber": "Badger",
                "knot size": "22mm",
            },
            "Galahad C3": {
                "patterns": [r"galahad"],
                "fiber": "Boar",
                "knot size": "22mm",
            },
            "Pharos C3": {
                "patterns": [r"pharos"],
                "fiber": "Synthetic",
                "knot size": "21mm",
            },
            "Shave Nook Final Edition": {
                "patterns": ["semogue.*bullgoose", "semogue.*shave.*nook"],
                "fiber": "Boar",
                "knot size": "26.5mm",
            },
            "SOC Boar": {
                "patterns": [
                    r"(semogue\s*owner.*club|s\.?\s*o\.?\s*c\.?\s*).*boar",
                    r"(semogue\s*owner.*club|s\.?\s*o\.?\s*c\.?\s*)",
                    "owner.*club",
                ],
                "fiber": "Boar",
                "knot size": "24mm",
            },
            "SOC Badger": {
                "patterns": [r"(semogue\s*owner.*club|s\.?\s*o\.?\s*c\.?\s*).*badger"],
                "fiber": "Badger",
                "knot size": "24mm",
            },
            "SOC Mixed Badger/Boar": {
                "patterns": [
                    r"(semogue\s*owner.*club|s\.?\s*o\.?\s*c\.?\s*).*badg.*boar",
                    r"(semogue\s*owner.*club|s\.?\s*o\.?\s*c\.?\s*).*boar.*badg",
                    r"(semogue\s*owner.*club|s\.?\s*o\.?\s*c\.?\s*).*mi[sx]t",
                    "semogue.*mist",
                ],
                "fiber": "Mixed Badger/Boar",
                "knot size": "24mm",
            },
            "Torga C5 Boar": {
                "patterns": ["torga.*c5"],
                "fiber": "Boar",
                "knot size": "24mm",
            },
            "r/wetshaving Brushbutt Boar": {
                "patterns": ["brushbutt"],
                "fiber": "Boar",
                "knot size": "22mm",
            },
        },
        "Simpson": {
            "Captain 2": {
                "patterns": [r"captain\s*2"],
                "fiber": "Badger",
                "knot size": "24mm",
            },
            "Colonel X2L": {
                "patterns": [r"colonel"],
                "fiber": "Badger",
                "knot size": "22mm",
            },
            "Chubby 1": {
                "patterns": [r"simp.*chubby\s*1", r"simp.*ch1"],
                "fiber": "Badger",
                "knot size": "22mm",
            },
            "Chubby 2": {
                "patterns": [r"simp.*chubby\s*2", r"simp.*ch2"],
                "fiber": "Badger",
                "knot size": "27mm",
            },
            "Chubby 3": {
                "patterns": [r"simp.*chubby\s*3", r"simp.*ch3"],
                "fiber": "Badger",
                "knot size": "29mm",
            },
            "Trafalgar T1": {
                "patterns": [r"simp(?:.*traf)?.*t?1"],
                "fiber": "Synthetic",
                "knot size": "23mm",
            },
            "Trafalgar T2": {
                "patterns": [r"simp(?:.*traf)?.*t?2"],
                "fiber": "Synthetic",
                "knot size": "24mm",
            },
            "Trafalgar T3": {
                "patterns": [r"simp(?:.*traf)?.*t?3"],
                "fiber": "Synthetic",
                "knot size": "28mm",
            },
            "Tulip T1": {
                "patterns": [r"simp.*tulip.*t1"],
                "fiber": "Synthetic",
                "knot size": "19mm",
            },
            "Tulip T2": {
                "patterns": [r"simp.*tulip.*t2"],
                "fiber": "Synthetic",
                "knot size": "20mm",
            },
            "Tulip T3": {
                "patterns": [r"simp.*tulip.*t3"],
                "fiber": "Synthetic",
                "knot size": "22mm",
            },
        },
        "Stirling": {
            "2-Band Synthetic": {
                "patterns": [r"stirl.*(?:2|two)(?:-|\s)+band"],
                "fiber": "Synthetic",
                "knot size": "24mm",
            },
            "Li'l Bridder": {
                "patterns": ["brudder"],
                "fiber": "Synthetic",
                "knot size": "22mm",
            },
            "Synthetic": {
                "patterns": ["st(i|e)rling.*kong"],
                "fiber": "Synthetic",
            },
        },
        "Stirling/Zenith": {
            "Boar": {
                "patterns": [r"^(?=.*zenith)(?=.*st(i|e)rling).*"],
                "fiber": "Boar",
            },
            "28mmx50mm Boar (510SE)": {
                "patterns": [
                    "(510(\s*|-*)se|jhdsajkghjkdhagkgkjgkhagdkjagdassd)",
                    r"^(?=.*zenith)(?=.*st(i|e)rling)(?=.*28).*",
                ],
                "fiber": "Boar",
                "knot size": "28mm",
            },
            "31mmx50mm Boar (510SE-XL)": {
                "patterns": [
                    "(510(\s*|-*)se(\s*|-*)xl|jhdsajkghjkdhagkgkjgkhagdkjagdassd)",
                    r"^(?=.*zenith)(?=.*st(i|e)rling)(?=.*31).*",
                ],
                "fiber": "Boar",
                "knot size": "31mm",
            },
            "r/wetshaving MOAR BOAR": {
                "patterns": ["moar.*boar", r"508\s*xl", "wetshaving.*exc"],
                "fiber": "Boar",
                "knot size": "31mm",
                "name": "r/wetshaving MOAR BOAR",
            },
        },
        "Wald": {
            "A1": {
                "patterns": ["wald.*a1"],
                "fiber": "Synthetic",
                "knot size": "29mm",
            },
            "Calyx": {
                "patterns": ["(?:wald.*)?calyx"],
                "fiber": "Synthetic",
                "knot size": "27mm",
            },
            "J1": {
                "patterns": ["wald.*j1"],
                "fiber": "Badger",
                "knot size": "27mm",
            },
            "J2": {
                "patterns": ["wald.*j2"],
                "fiber": "Badger",
                "knot size": "27mm",
            },
            "J3": {
                "patterns": ["wald.*j3"],
                "fiber": "Badger",
                "knot size": "27mm",
            },
            "J4": {
                "patterns": ["wald.*j4"],
                "fiber": "Badger",
                "knot size": "27mm",
            },
        },
        "Zenith": {
            "502B XSE": {
                "patterns": ["502B"],
                "fiber": "Boar",
                "knot size": "26mm",
            },
            "506U SE": {
                "patterns": ["506U"],
                "fiber": "Boar",
                "knot size": "27mm",
            },
            "507U ": {
                "patterns": ["507U"],
                "fiber": "Boar",
                "knot size": "27mm",
            },
            "508 ": {
                "patterns": ["zen.*B26"],
                "fiber": "Boar",
                "knot size": "27mm",
            },
            "B03-A26": {
                "patterns": ["b03-a26"],
                "fiber": "Boar",
                "knot size": "26mm",
            },
            "B26": {
                "patterns": ["zen.*B26"],
                "fiber": "Boar",
                "knot size": "27mm",
            },
            "B28": {
                "patterns": ["zen.*B28"],
                "fiber": "Boar",
                "knot size": "28mm",
            },
            "B30": {
                "patterns": ["zen.*B30"],
                "fiber": "Boar",
                "knot size": "27.5mm",
            },
            "B33": {
                "patterns": ["zen.*B33"],
                "fiber": "Boar",
                "knot size": "27.5mm",
            },
            "B35": {
                "patterns": ["zen.*B35"],
                "fiber": "Boar",
                "knot size": "31mm",
            },
            "Butterscotch Chubby": {
                "patterns": ["zen.*B34", "butter.*chub", "chub.*butter"],
                "fiber": "Boar",
                "knot size": "28mm",
            },
            "Unbleached Boar": {
                "patterns": ["^(?=.*zenith)(?=.*unbleach).*"],
                "fiber": "Boar",
                "knot size": "27mm",
            },
        },
    }

    @cached_property
    def _pattern_map(self):
        result = {}
        for brand, models in self._raw.items():
            for model, property_map in models.items():
                for pattern in property_map["patterns"]:
                    map = property_map.copy()
                    map["brand"] = brand
                    if not "name" in map:
                        map["name"] = f"{brand} {model}"

                    del map["patterns"]
                    result[pattern] = map
                    # result[pattern] = {"name": name, "fiber": property_map["fiber"]}

        return result

    @lru_cache(maxsize=None)
    def get_property_map(self, input_string: str) -> dict[str, str]:
        map = self._pattern_map
        for alt_name_re in sorted(map.keys(), key=len, reverse=True):
            if re.search(alt_name_re, input_string, re.IGNORECASE):
                result = map[alt_name_re]
                # if "knot size" not in result:
                knot_size = self.get_knot_size(input_string)
                if knot_size:
                    result["knot size"] = knot_size

                fiber = self.get_fiber(input_string)
                if fiber:
                    result["fiber"] = fiber

                return result
        return None


class OmegaSemogueBrushParsingStrategy(BaseBrushParsingStrategy):

    @lru_cache(maxsize=None)
    def get_property_map(self, input_string: str) -> Dict[str, str]:
        input_string = input_string.lower().replace("semouge", "semogue")

        omse_brand = re.search(r"(omega|semogue)", input_string, re.IGNORECASE)
        omse_model = re.search(
            r"(omega|semogue)[^]\n\d]+(c\d{1,3}|\d{3,6})", input_string, re.IGNORECASE
        )
        omse_model_num = None
        if omse_model:
            omse_model_num = omse_model.group(2)
            if omse_model_num:
                brand = omse_brand.group(1).title()
                name = f"{brand} {omse_model_num}"
                fiber = self.get_fiber(input_string)
                if fiber == None:
                    fiber = "Boar"
                if fiber != "Boar":
                    name = f"{name} ({fiber})"
                result = {
                    "brand": brand,
                    "name": name,
                    "fiber": fiber,
                }
                knot_size = self.get_knot_size(input_string)
                if knot_size:
                    result["knot size"] = knot_size
                return result

        return None


class ZenithBrushParsingStrategy(BaseBrushParsingStrategy):

    @lru_cache(maxsize=None)
    def get_property_map(self, input_string: str) -> Dict[str, str]:
        zenith_re = r"Zenith.*([A-Za-z]\d{1,3})"
        res = re.search(zenith_re, input_string, re.IGNORECASE)
        if res:
            name = f"Zenith {res.group(1).upper()}"
            fiber = self.get_fiber(input_string)
            if fiber == None:
                fiber = "Boar"
            if fiber != "Boar":
                name = f"{name} ({fiber})"
            result = {"brand": "Zenith", "name": name, "fiber": fiber}
            knot_size = self.get_knot_size(input_string)
            if knot_size:
                result["knot size"] = knot_size
            return result

        return None


class OtherBrushStrategy(BaseBrushParsingStrategy):
    _raw = {
        "AKA Brushworx": {"patterns": ["aka.*brush"], "default": "Synthetic"},
        "Alpha": {"patterns": ["alpha"], "default": "Synthetic"},
        "AMACK": {"patterns": ["amack"], "default": "Synthetic"},
        "Anbbas": {"patterns": ["anbbas"], "default": "Synthetic"},
        "AP Shave Co": {
            "patterns": [r"AP\s*shave\s*(co)?", r"\bap\b"],
            "default": "Synthetic",
        },
        "Art of Shaving": {
            "patterns": [r"^\s*aos", "art.*of.*sha"],
            "default": "Badger",
        },
        "Aurora Grooming": {"patterns": ["aurora\s*grooming"], "default": "Synthetic"},
        "Bass": {
            "patterns": [
                r"\bbass\b",
            ],
            "default": "Boar",
        },
        "B&M": {"patterns": [r"b\s*(&|a)\s*m", "barrister"], "default": "Synthetic"},
        "Beaumont": {"patterns": ["bea.{1,3}mont"], "default": "Badger"},
        "Black Anvil": {"patterns": ["black.*anv"], "default": "Badger"},
        "Black Eagle": {"patterns": ["black.*eag"], "default": "Badger"},
        "Blackland": {
            "patterns": ["blackland"],
            "default": "Synthetic",
            "knot size": "23mm",
        },
        "Boker": {"patterns": ["boker"], "default": "Synthetic"},
        "Boti": {"patterns": ["boti"], "default": "Synthetic"},
        "Brad Sears": {"patterns": ["brad.*sears"], "default": "Badger"},
        "Bristle Brushwerks": {
            "patterns": ["huck", "bristle.*brush"],
            "default": "Badger",
        },
        "Brushcraft": {"patterns": ["brushcraft"], "default": "Synthetic"},
        "Bullseye Brushworks": {"patterns": ["bullseye"], "default": "Synthetic"},
        "Carnavis & Richardson": {"patterns": ["carn.*rich"], "default": "Synthetic"},
        "Catalin": {"patterns": ["catalin"], "default": "Badger"},
        "CaYuen": {"patterns": ["cayuen"], "default": "Synthetic"},
        "Chisel & Hound": {
            "patterns": ["chis.*hou", "chis.*fou", r"\bc(?:\&|and|\+)h\b"],
            "default": "Badger",
            "knot size": "26mm",
        },
        "Craving Shaving": {"patterns": ["crav.*shav"], "default": "Synthetic"},
        "Cremo": {"patterns": ["cremo"], "default": "Horse"},
        "Crescent City Craftsman": {"patterns": ["cres.*city"], "default": "Synthetic"},
        "Declaration Grooming (batch not specified)": {
            "patterns": ["declaration", r"\bdg\b"],
            "default": "Badger",
        },
        "DSCosmetics": {
            "patterns": [r"DSC?\s*Cosmetic", r"\bDSC\b"],
            "default": "Synthetic",
        },
        "Den of Man": {"patterns": ["den.*of.*man"], "default": "Synthetic"},
        "Dogwood": {
            "patterns": ["dogw", "dogc*l", "^voa", r"\bdw\b"],
            "default": "Badger",
        },
        "Doug Korn": {"patterns": [r"doug\s*korn"], "default": "Badger"},
        "Dubl Duck": {"patterns": ["dubl.*duck"], "default": "Boar"},
        "Edwin Jagger": {"patterns": ["edwin.*jag"], "default": "Badger"},
        "El Druida": {"patterns": ["druidi*a"], "default": "Badger"},
        "Elite": {"patterns": ["elite"], "default": "Badger"},
        "Erskine": {"patterns": ["erskine"], "default": "Boar"},
        "Ever Ready": {"patterns": ["ever.*read"], "default": "Badger"},
        "Executive Shaving": {"patterns": ["execut.*shav"], "default": "Synthetic"},
        "Farvour Turn Craft": {"patterns": ["farvour"], "default": "Badger"},
        "Fine": {"patterns": [r"fine\b"], "default": "Synthetic"},
        "Firehouse Potter": {"patterns": ["fireh.*pott"], "default": "Synthetic"},
        "Fendrihan": {"patterns": ["fendri"], "default": "Badger"},
        "Frank Shaving": {"patterns": ["frank.*sha"], "default": "Synthetic"},
        "Geo F. Trumper": {"patterns": ["geo.*trumper"], "default": "Badger"},
        "Grizzly Bay": {"patterns": ["griz.*bay"], "default": "Badger"},
        "Haircut & Shave Co": {"patterns": ["haircut.*shave"], "default": "Badger"},
        "Heritage Collection": {"patterns": ["heritage"], "default": "Badger"},
        "Holzleute": {"patterns": ["holzleute"], "default": "Badger"},
        "L'Occitane en Provence": {"patterns": ["oc*citane"], "default": "Synthetic"},
        "Lancaster Brushworks": {"patterns": ["lancaster"], "default": "Synthetic"},
        "Leavitt & Pierce": {"patterns": ["leav.*pie"], "default": "Badger"},
        "Leonidam": {"patterns": ["leonidam", "leo.*nem"], "default": "Badger"},
        "Liojuny Shaving": {"patterns": ["liojuny"], "default": "Synthetic"},
        "Long Shaving": {"patterns": [r"long\s*shaving"], "default": "Badger"},
        "Lutin Brushworks": {"patterns": ["lutin"], "default": "Synthetic"},
        "Maggard": {"patterns": ["^.*mag(g?ard)?s?"], "default": "Synthetic"},
        "Maseto": {"patterns": ["maseto"], "default": "Badger"},
        "Mojo": {"patterns": ["mojo"], "default": "Badger"},
        "Mondial": {"patterns": ["mondial"], "default": "Boar"},
        "Morris & Forndran": {
            "patterns": ["morris", r"m\s*&\s*f"],
            "default": "Badger",
        },
        "Mozingo": {"patterns": ["mozingo"], "default": "Badger"},
        "MRed": {"patterns": ["mred"], "default": "Badger"},
        "Muninn Woodworks": {"patterns": ["munin"], "default": "Badger"},
        "Muhle": {"patterns": [r"\bmuhle\b"], "default": "Badger"},
        "Mutiny": {"patterns": ["mutiny"], "default": "Synthetic"},
        "Noble Otter": {"patterns": ["noble", r"no\s*\d{2}mm"], "default": "Badger"},
        "NY Shave Co": {"patterns": [r"ny\s.*shave.*co"], "default": "Badger"},
        "Omega (model not specified)": {"patterns": ["omega"], "default": "Boar"},
        "Oumo": {"patterns": ["o[ou]mo"], "default": "Badger"},
        "Oz Shaving": {"patterns": ["oz.*sha"], "default": "Synthetic"},
        "PAA": {"patterns": ["paa", "phoenix.*art"], "default": "Synthetic"},
        "Paladin": {"patterns": ["paladin"], "default": "Badger"},
        "Parker": {"patterns": ["parker"], "default": "Badger"},
        "Perfecto": {"patterns": ["perfecto"], "default": "Badger"},
        "Plisson": {"patterns": ["plisson"], "default": "Badger"},
        "Prometheus Handcrafts": {"patterns": ["promethe"], "default": "Synthetic"},
        "Razorock": {
            "patterns": ["Razorr*ock", r"(^|\s)rr\s", "plissoft", "razor rock"],
            "default": "Synthetic",
        },
        "Rockwell": {"patterns": ["rockwell"], "default": "Synthetic"},
        "Rubberset": {"patterns": ["rubberset"], "default": "Badger"},
        "Rudy Vey": {"patterns": ["rudy.*vey"], "default": "Badger"},
        "Rick Montalvo": {"patterns": ["montalv"], "default": "Synthetic"},
        "Sawdust Creation Studios": {"patterns": ["sawdust"], "default": "Synthetic"},
        "Semogue (model not specified)": {"patterns": ["semogue"], "default": "Boar"},
        "SHAVEDANDY": {"patterns": ["shavedandy"], "default": "Synthetic"},
        "Shavemac": {"patterns": ["shavemac"], "default": "Badger"},
        "Shore Shaving": {"patterns": ["shore.*shav"], "default": "Synthetic"},
        "Simpson": {
            "patterns": ["simpson", "duke", "chubby.*2", "trafalgar"],
            "default": "Badger",
        },
        "Some Making Required": {"patterns": ["some.*maki"], "default": "Synthetic"},
        "Spiffo": {"patterns": ["spiffo"], "default": "Badger"},
        "Stirling": {"patterns": ["st[ie]rl"], "default": "Badger"},
        # "Stirling": {"patterns": ["st[ie]rl.*kong"], "default": "Synthetic"},
        "Strike Gold Shave": {"patterns": ["strike.*gold"], "default": "Synthetic"},
        "Summer Break": {"patterns": ["summer.*break"], "default": "Badger"},
        "Supply": {"patterns": ["supply"], "default": "Synthetic"},
        "Teton Shaves": {"patterns": ["teton"], "default": "Badger"},
        "The Bluebeard's Revenge": {
            "patterns": ["bluebeard.*rev"],
            "default": "Synthetic",
        },
        "The Holy Black": {"patterns": ["tgn", "golden.*nib"], "default": "Synthetic"},
        "The Golden Nib": {"patterns": ["tgn", "golden.*nib"], "default": "Boar"},
        "The Razor Company": {"patterns": ["razor.*co", "trc"], "default": "Synthetic"},
        "The Varlet": {"patterns": ["varlet"], "default": "Badger"},
        "Tony Forsyth": {"patterns": ["tony.*fors"], "default": "Badger"},
        "That Darn Rob": {"patterns": ["darn.*rob", "tdr"], "default": "Badger"},
        "Thater": {"patterns": ["thater"], "default": "Badger"},
        "TOBS": {"patterns": ["tobs", "taylor.*bond"], "default": "Badger"},
        "Trotter Handcrafts": {"patterns": ["trotter"], "default": "Synthetic"},
        "Turn-N-Shave": {"patterns": ["turn.{1,5}shave", "tns"], "default": "Badger"},
        "Van der Hagen": {"patterns": ["van.*hag.*"], "default": "Boar"},
        "Vie Long": {"patterns": ["vie.*long"], "default": "Horse"},
        "Viking": {"patterns": ["viking"], "default": "Badger"},
        "Vintage Blades": {"patterns": ["vintage.*blades"], "default": "Badger"},
        "Virginia Cheng": {"patterns": ["virginia.*cheng"], "default": "Badger"},
        "Voigt & Cop": {"patterns": ["v&c", "voigt"], "default": "Badger"},
        "Vulfix": {"patterns": ["vulfix"], "default": "Badger"},
        "Wald": {"patterns": ["wald", "west.*coast"], "default": "Badger"},
        "WCS": {"patterns": ["wcs", "west.*coast"], "default": "Synthetic"},
        "Whipped Dog": {"patterns": ["whipped.*dog"], "default": "Badger"},
        "Wolf Whiskers": {"patterns": ["wolf.*whis"], "default": "Badger"},
        "Wild West Brushworks": {
            "patterns": ["wild.*west", "wwb", "ww.*brushw"],
            "default": "Synthetic",
        },
        "Yaqi": {"patterns": ["yaqu*i"], "default": "Synthetic"},
        "Zenith": {"patterns": [r"zen\w+"], "default": "Boar"},
    }

    @cached_property
    def _pattern_map(self):
        result = {}
        # for most makers just split them out into the various fiber knots
        for maker, data in self._raw.items():
            for maker_re in data["patterns"]:
                result[maker_re] = {"name": maker, "default": data["default"]}
                if "knot size" in data:
                    result[maker_re]["knot size"] = data["knot size"]

            # pm = {
            #     "name": f"{maker} {data['default']}",
            #     "fiber": data["default"],
            # }
            # for maker_re in data["patterns"]:
            #     result[maker_re] = pm
            #     for fiber, fiber_re in self._fibers.items():
            #         name = f"{maker} {fiber}"
            #         property_map = {
            #             "name": name,
            #             "fiber": fiber,
            #         }
            #         full_re = maker_re + ".*" + fiber_re
            #         result[full_re] = property_map

        return result

    @cached_property
    def _sorted_pattern_map_keys(self):
        return sorted(self._pattern_map.keys(), key=len, reverse=True)

    @lru_cache(maxsize=None)
    def get_property_map(self, input_string: str) -> Dict[str, str]:
        for maker_re in self._sorted_pattern_map_keys:
            # match maker
            if re.search(maker_re, input_string, re.IGNORECASE):
                maker = self._pattern_map[maker_re]["name"]
                default = self._pattern_map[maker_re]["default"]
                # result = {}

                # get knot size
                knot_size = self.get_knot_size(input_string)
                if knot_size is None:
                    if "knot size" in self._pattern_map[maker_re]:
                        knot_size = self._pattern_map[maker_re]["knot size"]
                # result = result | {"knot size": knot_size}

                # match fiber
                for fiber, fiber_re in self._fibers.items():
                    if re.search(fiber_re, input_string, re.IGNORECASE):
                        return {
                            "brand": f"{maker}",
                            "name": f"{maker} {fiber}",
                            "fiber": fiber,
                            "knot size": knot_size,
                        }

                return {
                    "brand": f"{maker}",
                    "name": f"{maker} {default}",
                    "fiber": default,
                    "knot size": knot_size,
                }

        # for alt_name_re in self._sorted_pattern_map_keys:
        #     if re.search(alt_name_re, input_string, re.IGNORECASE):
        #         result = self._pattern_map[alt_name_re]
        #         knot_size = self.get_knot_size(input_string)
        #         if knot_size:
        #             result["knot size"] = knot_size
        #         return result
        return None
