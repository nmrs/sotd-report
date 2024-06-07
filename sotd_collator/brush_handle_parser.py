from collections import OrderedDict
from functools import cached_property, lru_cache
from unittest.mock import Base
from base_parser import BaseParser
import re


class BrushHandleParser(BaseParser):
    """
    Amalgamate names
    """

    __raw = {
        "AKA Brushworx": {"patterns": ["aka.*brush", "aka"]},
        "Alpha": {"patterns": ["alpha"]},
        "AMACK": {"patterns": ["amack"]},
        "Anbbas": {"patterns": ["anbbas"]},
        "AP Shave Co": {
            "patterns": [r"AP\s*shave", r"\bap\b"],
        },
        "Art of Shaving": {
            "patterns": [r"^\s*aos", "art.*of.*sha"],
        },
        "Artesania Romera": {"patterns": ["romera"]},
        "Aurora Grooming": {"patterns": ["aurora\s*grooming"]},
        "B&M": {"patterns": ["b&m", r"\bbam\b", "b & m", "barrister"]},
        "Balea Men": {"patterns": ["balea"]},
        "Bass": {
            "patterns": [
                r"\bbass\b",
            ],
        },
        "Beaumont": {"patterns": ["bea.{1,3}mont"]},
        "Billy Goat Brushworks": {"patterns": ["billy.*goat"]},
        "Black Anvil": {"patterns": ["black.*anv"]},
        "Black Eagle": {"patterns": ["black.*eag"]},
        "Blackland": {
            "patterns": ["blackland"],
        },
        "Boker": {
            "patterns": ["boker"],
        },
        "Boti": {
            "patterns": ["boti", "boti.*brush"],
        },
        "Brad Sears": {
            "patterns": ["brad.*sears"],
        },
        "Bristle Brushwerks": {
            "patterns": ["huck", "bristle.*brush"],
        },
        "Brushcraft": {
            "patterns": ["brushcraft"],
        },
        "Bullseye Brushworks": {
            "patterns": ["bullseye"],
        },
        "C-Mon": {
            "patterns": ["c-mon"],
        },
        "Carnavis & Richardson": {
            "patterns": ["carn.*rich"],
        },
        "Catalin": {
            "patterns": ["catalin"],
        },
        "CaYuen": {
            "patterns": ["cayuen"],
        },
        "Century": {
            "patterns": ["century"],
        },
        "Chisel & Hound": {
            "patterns": ["chisel.*hound", "chis.*fou", r"\bc(?:\&|and|\+)h\b"],
        },
        "Cool Dog": {
            "patterns": ["cool dog"],
        },
        "Craving Shaving": {
            "patterns": ["crav.*shav"],
        },
        "Cremo": {
            "patterns": ["cremo"],
        },
        "Crescent City Craftsman": {
            "patterns": ["cres.*city"],
        },
        "Cumberbatch": {
            "patterns": ["cumberbatch"],
        },
        "Declaration Grooming": {
            "patterns": [r"^(?!.*dogwood)declaration", r"^(?!.*dogwood)\bdg\b"],
        },
        "DS Cosmetics": {
            "patterns": [r"DSC?\s*Cosmetic", r"\bDSC\b"],
        },
        "Den of Man": {
            "patterns": ["den.*of.*man"],
        },
        "Dogwood Handcrafts": {
            "patterns": [
                "dogwoo",
                "dogwood.*handcrafts+",
                "dogc*l",
                "^voa",
                r"\bdw\b",
            ],
        },
        "Doug Korn": {
            "patterns": [r"doug\s*korn"],
        },
        "Dubl Duck": {
            "patterns": ["dubl.*duck"],
        },
        "Edwin Jagger": {
            "patterns": ["edwin.*jag"],
        },
        "El Druida": {
            "patterns": ["druidi*a"],
        },
        "Elite": {
            "patterns": ["elite"],
        },
        "Envy Shave": {
            "patterns": ["envy.*shave"],
        },
        "Erskine": {
            "patterns": ["erskine"],
        },
        "Ever Ready": {
            "patterns": ["ever.*read"],
        },
        "Executive Shaving": {
            "patterns": ["execut.*shav"],
        },
        "Farvour Turn Craft": {
            "patterns": ["farvour.*(?:turn).*(?:craft)"],
        },
        "Fine": {
            "patterns": [r"fine\b"],
        },
        "Firehouse Potter": {
            "patterns": ["fireh.*pott"],
        },
        "Fendrihan": {
            "patterns": ["fendri"],
        },
        "Frank Shaving": {
            "patterns": ["frank.*sha"],
        },
        "Fuller": {
            "patterns": ["fuller"],
        },
        "Geo F. Trumper": {
            "patterns": ["geo.*trumper"],
        },
        "Grizzly Bay": {
            "patterns": ["grizzly.*bay"],
        },
        "Haircut & Shave Co": {
            "patterns": ["haircut.*shave"],
        },
        "Heritage Collection": {
            "patterns": ["heritage", "heritage collection"],
        },
        "Holzleute": {
            "patterns": ["holzleute"],
        },
        "Imperial": {
            "patterns": ["imperial"],
        },
        "L'Occitane en Provence": {
            "patterns": ["oc*citane"],
        },
        "Lancaster Brushworks": {
            "patterns": ["lancaster"],
        },
        "Leavitt & Pierce": {
            "patterns": ["leav.*pie"],
        },
        "Lentfer Custom Woodworks": {
            "patterns": ["lentfer"],
        },
        "Leonidam": {
            "patterns": ["leonidam", "leo.*nem"],
        },
        "Liojuny Shaving": {
            "patterns": ["liojuny"],
        },
        "Long Shaving": {
            "patterns": [r"long\s*shaving"],
        },
        "Lutin Brushworks": {
            "patterns": ["lutin"],
        },
        "Maggard": {
            "patterns": ["magg"],
        },
        "Maseto": {
            "patterns": ["maseto"],
        },
        "Mistic": {
            "patterns": ["mistic"],
        },
        "Mojo": {
            "patterns": ["mojo"],
        },
        "Mondial": {
            "patterns": ["mondial"],
        },
        "Morris & Forndran": {
            "patterns": ["morris", r"m\s*&\s*f"],
        },
        "Mozingo": {
            "patterns": ["mozingo"],
        },
        "MRed": {
            "patterns": ["mred"],
        },
        "Muninn Woodworks": {
            "patterns": [r"mun*in.*(?:woodworks+)+"],
        },
        "Muhle": {
            "patterns": [r"\bmuhle\b"],
        },
        "Mutiny": {
            "patterns": ["mutiny"],
        },
        "New England Shaving Company": {
            "patterns": ["new.*england"],
        },
        "Noble Otter": {
            "patterns": ["noble", r"no\s*\d{2}mm"],
        },
        "Nom": {
            "patterns": [r"\bnom\b"],
        },
        "NY Shave Co": {
            "patterns": [r"ny\s.*shave.*co"],
        },
        "Omega": {
            "patterns": ["omega"],
        },
        "Oumo": {
            "patterns": ["o[ou]mo"],
        },
        "Oz Shaving": {
            "patterns": ["oz.*sha"],
        },
        "PAA": {
            "patterns": ["paa", "phoenix.*art"],
        },
        "Paladin": {
            "patterns": ["paladin"],
        },
        "Paragon": {
            "patterns": ["paragon"],
        },
        "Parker": {
            "patterns": ["parker"],
        },
        "Perfecto": {
            "patterns": ["perfecto"],
            "knot size": "20mm",
        },
        "Plisson": {
            "patterns": ["plisson"],
        },
        "Prometheus Handcrafts": {
            "patterns": ["prometheus.*(?:handcraft)+"],
        },
        "Razorock": {
            "patterns": ["Razorr*ock", r"(^|\s)rr\s", "plissoft", "razor rock"],
        },
        "Rex Supply Co.": {
            "patterns": [r"rex.*(?:supply)+"],
        },
        "Rockwell": {
            "patterns": ["rockwell"],
        },
        "Rooney": {
            "patterns": ["rooney"],
        },
        "Rubberset": {
            "patterns": ["rubberset"],
        },
        "Rudy Vey": {
            "patterns": ["rudy.*vey"],
        },
        "Rick Montalvo": {
            "patterns": ["montalv"],
        },
        "Sawdust Creation Studios": {
            "patterns": ["sawdust", "sawdust creation"],
        },
        "Semogue": {
            "patterns": ["semogue"],
        },
        "SHAVEDANDY": {
            "patterns": ["shavedandy"],
        },
        "Shave Forge": {
            "patterns": ["shave.*forge"],
        },
        "Shavemac": {
            "patterns": ["shavemac"],
        },
        "Shave Nation": {
            "patterns": ["shave.*nation"],
        },
        "Shore Shaving": {
            "patterns": ["shore.*shav"],
        },
        "Simpson": {
            "patterns": ["simpson", "duke", "chubby.*(1|2|3)", "trafalgar"],
        },
        "Some Making Required": {
            "patterns": ["some.*maki"],
        },
        "Spiffo": {
            "patterns": ["spiffo"],
        },
        "Stirling": {
            "patterns": [r"^(?!.*zeni).*st[ie]rl"],
        },
        "Strike Gold Shave": {
            "patterns": ["strike.*gold"],
        },
        "Summer Break": {
            "patterns": ["summer.*break"],
        },
        "Supply": {
            "patterns": ["supply"],
        },
        "Surrey": {
            "patterns": ["surrey"],
        },
        "TanZ": {
            "patterns": ["tobs", "tanz"],
        },
        "Teton Shaves": {
            "patterns": ["teton"],
        },
        "The Bluebeard's Revenge": {
            "patterns": ["bluebeard.*rev"],
        },
        "The Holy Black": {
            "patterns": ["tgn", "golden.*nib"],
        },
        "The Golden Nib": {
            "patterns": ["tgn", "golden.*nib"],
        },
        "The Razor Company": {
            "patterns": ["razor.*co", "trc"],
        },
        "The Varlet": {
            "patterns": ["varlet"],
        },
        "Tony Forsyth": {
            "patterns": ["tony.*fors"],
        },
        "That Darn Rob": {
            "patterns": ["darn.*rob", "tdr"],
        },
        "Thater": {
            "patterns": ["thater"],
        },
        "TOBS": {
            "patterns": ["tobs", "taylor.*bond"],
        },
        "Trotter Handcrafts": {
            "patterns": ["trotter.*(?:handcraft)*"],
        },
        "Turn-N-Shave": {
            "patterns": [r"^(?!.*chis)turn.{1,5}shave", r"^(?!.*chis)\btns\b"],
        },
        "Van der Hagen": {
            "patterns": ["van.*hag.*"],
        },
        "Vie Long": {
            "patterns": ["vie.*long"],
        },
        "Viking": {
            "patterns": ["viking"],
        },
        "Vintage Blades": {
            "patterns": ["vintage.*blades"],
        },
        "Virginia Cheng": {
            "patterns": ["virginia.*cheng"],
        },
        "Voigt & Cop": {
            "patterns": ["v&c", "voigt"],
        },
        "Vulfix": {
            "patterns": ["vulfix"],
        },
        "Wald": {
            "patterns": ["wald", "west.*coast"],
        },
        "WCS": {
            "patterns": ["wcs", "west.*coast"],
        },
        "Whipped Dog": {
            "patterns": ["whipped.*dog"],
        },
        "Wilkinson Sword": {
            "patterns": ["wilkinson"],
        },
        "Wolfman": {
            "patterns": [r"wolfman.*(?:wrb\d)+"],
        },
        "Wolf Whiskers": {
            "patterns": ["wolf.*whisker"],
        },
        "Wild West Brushworks": {
            "patterns": ["wild.*west", "wwb", "ww.*brushw"],
        },
        "Yaqi": {
            "patterns": [r"yaqu*i\b"],
        },
        "Zenith": {
            "patterns": [r"zen\w+", "moar"],
        },
    }

    @cached_property
    def __mapper(self):
        output = {}
        for name, property_map in self.__raw.items():
            for pattern in property_map["patterns"]:
                output[pattern] = {
                    "name": name,
                }
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
