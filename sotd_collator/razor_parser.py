from functools import cached_property, lru_cache
import re

from base_parser import BaseParser


class RazorParser(BaseParser):
    """
    Amalgamate names
    """

    _raw = {
        "3D Printed": {"": {"patterns": ["3d"]}},
        "Above the Tie": {
            "H1": {
                "patterns": [
                    r"\b(?:att|tie)\b.*h-*1",
                    "(atlas|bamboo|calypso|colossus|kronos).*h1",
                ],
            },
            "H2": {
                "patterns": [
                    r"\b(?:att|tie)\b.*h-*2",
                    "(?:atlas|bamboo|calypso|colossus|kronos).*h2",
                ],
            },
            "R1": {
                "patterns": [
                    r"\b(?:att|tie)\b.*r-*1",
                    "(?:atlas|bamboo|calypso|colossus|kronos).*r1",
                ],
            },
            "R2": {
                "patterns": [
                    r"\b(?:att|tie)\b.*r-*2",
                    "(?:atlas|bamboo|calypso|colossus|kronos).*r2",
                ],
            },
            "S1": {
                "patterns": [
                    r"\b(?:att|tie)\b.*s-*1",
                    "(?:atlas|bamboo|calypso|colossus|kronos).*s1",
                ],
            },
            "S2": {
                "patterns": [
                    r"\b(?:att|tie)\b.*s-*2",
                    "(?:atlas|bamboo|calypso|colossus|kronos).*s2",
                ],
            },
            "SE1": {
                "patterns": [
                    r"(?:\batt\b|tie).*se-*1*",
                    "(?:atlas|bamboo|calypso|colossus|kronos).*se1",
                ],
                "format": "AC",
            },
            "Windsor SSRH2": {
                "patterns": [r"\b(?:att|tie)\b.*(?:windsor)*\b.*ssrh2"],
            },
            "Windsor Pro SB90": {
                "patterns": [r"\b(?:att|tie)\b.*sb90", r"\b(?:att|tie)\b.*windsor"],
            },
        },
        "Alpha": {
            "Outlaw": {
                "patterns": ["alpha.*outl"],
            },
        },
        "Asylum": {
            "Evolution": {"patterns": ["asylum.*evo"], "format": "AC"},
            "Rx": {"patterns": ["asylum.*rx"], "format": "AC"},
        },
        "Atelier Durdan": {
            "Vestige": {"patterns": ["dur.*vestig"], "format": "GEM"},
            "Le Faulx": {"patterns": ["atelier.*durdan.*faulx"], "format": "AC"},
            "Le Maurice": {
                "patterns": ["dur.*maurice"],
            },
            "Mauritius": {
                "patterns": ["dur.*mauritius"],
            },
        },
        "Aylsworth": {
            "Apex": {"patterns": ["aylsworth.*apex"]},
            "Drakkant": {"patterns": ["drakk?ant", "aylsworth"]},
            "Kopparkant": {"patterns": ["kopp?arkant"]},
        },
        "Baili": {
            "TTO": {
                "patterns": [
                    r"(bail[ie]|br|bt|bd)[\s-]*[12]\d{1}[79]",
                    "bail[ie].*(tto|butterfly)",
                ]
            },
            "3-Piece": {"patterns": ["baili", r"(bail[ie]|br|bt|bd)[\s-]*[12]\d{2}"]},
        },
        "Barbaros": {
            "TR-1": {"patterns": [r"barbaros.*tr[\s-]1"]},
            "TR-2": {"patterns": [r"barbaros"]},
            "TR-3": {"patterns": [r"barbaros.*tr[\s-]3"]},
            "TR-4": {"patterns": [r"barbaros.*tr[\s-]4"]},
        },
        "Baxter": {"Safety Razor": {"patterns": ["baxter"]}},
        "BBNY": {"Safety Razor": {"patterns": ["bbny"]}},
        "Bevel": {"Razor": {"patterns": ["bevel"]}},
        "Blackland": {
            "Blackbird": {
                "patterns": [
                    r"bb\s*(sb|oc)",
                    r"(brass|black|ti)\s*bird",
                    "Balckbird",
                    "Blackbrid",
                    "Blaclbird",
                    "Blckbird",
                    "Blclbird",
                    r"Blackland\s*Tb?ird",
                ]
            },
            "Dart": {"patterns": [r"\bdart\b"]},
            "Era": {"patterns": ["black.*era", r"\bera\b", "black.*dna"]},
            "Osprey": {"patterns": ["osprey"]},
            "Sabre": {"patterns": ["sabre", "saber"], "format": "GEM"},
            "Tradere": {"patterns": ["tradere"]},
            "Vector": {"patterns": ["vector"], "format": "AC"},
        },
        "Blutt Rasur": {"BR-1": {"patterns": ["blutt?"]}},
        "Boker": {
            "Straight": {"patterns": [r"Boker(\s+straight)?"], "format": "Straight"}
        },
        "Broman": {
            "Razor": {"patterns": ["broman"]},
            "Razor Mark II": {"patterns": [r"broman\s*(mark|mk)\s*(?:two|2|ii)"]},
        },
        "Cartridge / Disposable": {
            "": {
                "patterns": [
                    "atra",
                    r"\bbic\b",
                    "cartridge",
                    "disposable",
                    "fusion",
                    r"gil.*et.*labs",
                    "Gil.*et.*guard",
                    "harry",
                    r"mach\s*(3|iii)",
                    "sensor",
                    r"trac[\s-]*2",
                    r"trac[\s-]*ii",
                ],
                "format": "Cartridge",
            }
        },
        "Carbon": {
            "Cx": {
                "patterns": [
                    "carbon.*cx",
                    "carbon.*shav.*com",
                    "carbon.*316",
                    "carbon.*orig",
                    "carbon.*ti",
                ]
            },
        },
        "CV Heljestrand": {
            "Straight": {
                "patterns": [r"heljestra.*(stra)?"],
                "format": "Straight",
            },
            "Lather Catcher": {
                "patterns": [r"heljestrand.*catcher"],
                "format": "Wedge",
            },
        },
        "Charcoal Goods": {
            "Everyday": {"patterns": [r"^(?!.*wcs).*\b(char\w*l|cg).*every"]},
            "Lvl 1": {
                "patterns": [
                    r"^(?!.*wcs).*\b(char\w*l|cg).*(level|lvl|lv)(\s*|-)(1|one|i)\b"
                ]
            },
            "Lvl 2": {
                "patterns": [
                    r"^(?!.*wcs).*\b(char\w*l|cg).*(level|lvl|lv)(\s*|-)(2|two|ii)\b",
                    "charcoal\s*goods",  # Lvl 2 is the most popular so assume just CG is this
                ]
            },
            "Lvl 3": {
                "patterns": [
                    r"^(?!.*wcs).*\b(char\w*l|cg).*(level|lvl|lv)(\s*|-)(3|three|iii)\b"
                ]
            },
            "Lithe Head": {"patterns": ["lithe"]},
        },
        "Chinchilla": {
            "Razor": {
                "patterns": ["chinchilla"],
            }
        },
        "Chiseled Face": {
            "Legacy": {
                "patterns": [
                    "chiseled.*face.*(ti|legacy|alum)",
                    "cfl*.*(ti|legacy|alum)",
                    "face.*legacy",
                    "legacy",
                ]
            }
        },
        "CJB": {
            "Kamisori Shavette": {
                "patterns": ["cjb*vett*e", "cjb.*kamisori"],
                "format": "AC",
            }
        },
        "Classic": {
            "King Cobra": {"patterns": ["king.*cobra"], "format": "AC"},
            "Cobra Classic": {
                "patterns": ["cobra.*(clas|razor)", "classic.*cobra", "^cobra$"],
                "format": "AC",
            },
        },
        "Colonial": {
            "General": {
                "patterns": ["col.*gener", "general", "colonial.*ac"],
                "format": "AC",
            },
            "Silversmith": {"patterns": ["silversmith"]},
        },
        "Crescent City": {"Closed Comb 79": {"patterns": ["cres.*city.*79"]}},
        "DSCosmetic": {"T7SE": {"patterns": ["t7se"]}},
        "Dorco": {
            "ST-301": {"patterns": ["ST(?:-*\s*)301"]},
            "PL-602": {"patterns": ["pl(?:-*\s*)602"]},
        },
        "Dovo": {
            "Straight": {
                "patterns": [r"^(?!.*shavette).*dovo(?:\s+straight)*"],
                "format": "Straight",
            }
        },
        "Edwin Jagger": {
            "DE89": {
                "patterns": [
                    r"DE\s*89",
                    "kelvin",
                    "edwi",
                    r"(?:de|ej)\s*8\d",
                ]
            },
            "3one6": {"patterns": [r"\b3\s*one\s*6\b", r"EJ\s*316"]},
        },
        "EldrormR Industries": {
            "MM24": {"patterns": [r"mm\s*24"], "format": "GEM"},
            "Scrubty-four": {
                "patterns": [r"mm\s*24\s*scrub", r"scrubty(?:-|\s)*four"],
                "format": "GEM",
            },
        },
        "Enders": {
            "Speed Shaver": {"patterns": ["enders"], "format": "Enders"},
        },
        "Ever-Ready": {
            "1912": {
                "patterns": [r"(?:ever|er).*1912", r"1912.*(?:ever|er)"],
                "format": "GEM",
            },
            "1914": {
                "patterns": [
                    r"(?:ever|er).*1914",
                    r"1914.*(?:ever|er)",
                    r"ever.*lather",
                ],
                "format": "GEM",
            },
            "1924": {
                "patterns": [
                    r"(ever|er).*1924",
                    r"1924.*(ever|er)",
                    r"shovel\s*head",
                    "gem.*1924",
                    "1924",
                ],
                "format": "GEM",
            },
            "E-Bar": {"patterns": [r"(ever|er).*e-bar"], "format": "GEM"},
            "Featherweight": {
                "patterns": [r"(ever|er).*featherw", "featherweight"],
                "format": "GEM",
            },
            "G-Bar": {"patterns": [r"(ever|er).*g-bar"], "format": "GEM"},
            "Streamline": {
                "patterns": [
                    r"(?:ever|er).*(stream\s*line|ambassador|jewel)",
                    r"\bstream\s*line\b",
                ],
                "format": "GEM",
            },
        },
        "Everyday": {"Stinger": {"patterns": ["everyday", "magnet"]}},
        "Executive Shaving": {
            "Claymore": {"patterns": ["claymore"], "format": "AC"},
            "Outlaw": {"patterns": ["exec.*outlaw", r"\bxec.*outlaw"]},
        },
        "Fatip": {
            "Grande": {"patterns": ["fatt?ip.*grande", "fatt?ip.*classic"]},
            "Gentile": {"patterns": ["fatt?ip.*gentile", "test.*genti.*"]},
            "Lo Storto": {"patterns": ["fatt?ip.*stor[tn]o"]},
            "Olive Wood": {"patterns": ["fatt?ip.*(olive|ulivo|wood)"]},
            "Piccolo": {"patterns": ["fatt?ip.*picc*oll*o", "fatip"]},
            "Retro": {"patterns": ["fatt?ip.*retro"]},
        },
        "Feather": {
            "AS-D2": {"patterns": ["feather.*as.*2", "as-*d2"]},
            "Popular": {"patterns": ["feather.*popular"]},
            "Shavette": {
                "patterns": [
                    "Feather.*(dx|ss|sr)",
                    "feather.*artist.*club",
                    "feather.*ac",
                ],
                "format": "AC",
            },
            # "DX": {
            #     "patterns": ["Feather.*dx", "feather.*artist.*club"],
            #     "format": "AC",
            # },
            # "SS": {
            #     "patterns": ["feather.*ss", "feather.*artist.*club.*ss", "feather.*folding"],
            #     "format": "AC",
            # },
            # "SR": {
            #     "patterns": ["feather.*sr", "feather.*artist.*club.*sr"],
            #     "format": "AC",
            # },
        },
        "Fine": {
            "Marvel": {"patterns": ["fine.*marvel"]},
            "Superlight Slant": {"patterns": ["superlight.*slant", "fine.*slant"]},
            "World's Finest": {"patterns": ["fine.*world"]},
        },
        "Filarmonica": {
            "Straight": {
                "patterns": [r"Filar*monica(\s+straight)*", "monserrat"],
                "format": "Straight",
            }
        },
        "Focus": {
            "R48": {"patterns": ["focus.*r48"]},
            "Tritok Slant": {"patterns": ["focus.*slant"]},
        },
        "FrankenRazor": {
            "": {"patterns": ["franken"]},
        },
        "Futur Clone": {
            "": {"patterns": ["futur.*clone", "Ming.*Shi.*(2000|adj)", "qshave"]},
        },
        "GEM": {
            "1912": {"patterns": ["gem.*1912", "1912.*gem"], "format": "GEM"},
            "Flying Wing (aka Bullet Tip)": {
                "patterns": [
                    "bullet.*tip|ajsdglkjalglkdglkgj",
                    "flying.*wing|lkasjdglkjadlgjld",
                ],
                "format": "GEM",
            },
            "Clog Pruf": {
                "patterns": ["gem.*clog|lkajdgjkag", ".*clog.*pruf|dlakjglgkjaglkdg"],
                "format": "GEM",
            },
            "Damaskeene": {"patterns": ["gem.*damas", "damaskeene"], "format": "GEM"},
            "Featherweight": {"patterns": ["gem.*(feather)"], "format": "GEM"},
            "G-Bar": {"patterns": ["gem.*g.*bar"], "format": "GEM"},
            "Junior": {"patterns": ["gem.*(junior|jr)"], "format": "GEM"},
            "Micromatic Open Comb": {
                "patterns": [
                    "gem.*(micro.*matic|mmoc|ocmm)",
                    "mmoc",
                    "ocmm",
                    "gem.*open.*comb",
                    "gem",
                ],
                "format": "GEM",
            },
            "Pushbutton": {"patterns": [r"gem.*push"], "format": "GEM"},
        },
        "Gibbs": {
            "no. 15/17": {"patterns": ["gibbs.*1[5|7]"]},
        },
        "Gillette": {
            "Aristocrat": {"patterns": ["art?istocrat"]},
            "Diplomat": {"patterns": ["Diplomat"]},
            "Fatboy": {
                "patterns": [r"fat\s*boy", r"gil.*et.*\b195\b", r"gil.*et.*exec"]
            },
            "Goodwill": {"patterns": ["Gil.*et.*goodwill"]},
            "Heritage": {"patterns": ["Gil.*et.*heritage"]},
            "Knack": {"patterns": ["Gil.*et.*knack"]},
            "Lady Gillette": {"patterns": ["lady.*gil.*et", "gil.*et.*lady"]},
            # gill.*new so that new.*improved is longer and gets evaluated first!
            "NEW": {
                "patterns": [
                    "gil.*new",
                    "bostonian",
                    "new.*(s|l)c",
                    "new.*(short|long).*comb",
                    "(british|english).*new",
                    "tuckaway",
                    "new.*luxe",
                    "rfb.*new",
                    "new.*rfb",
                    "gil.*et.*rfb",
                    "bottom.*new",
                    "big boy",
                ]
            },
            "New Improved": {"patterns": ["new.*improved"]},
            "Old Type": {
                "patterns": [
                    r"gillette\s*old",
                    "oc.*ball",
                    "old.*type",
                    "pocket.*ed",
                    "(single|double).*ring",
                    "big.*fellow",
                    "gil.*et.*bulldog",
                ]
            },
            "President": {"patterns": ["president"]},
            "Senator": {"patterns": ["senator"]},
            "Sheraton": {"patterns": ["sheraton"]},
            "7 O'Clock Sterling": {"patterns": ["gil.*te.*sterling", "o'?clock"]},
            "Slim": {
                "patterns": [
                    "Gil.*Slim",
                    "slim.*adjust",
                    r"\d\d.*slim",
                    r"slim.*\d",
                    "^slim$",
                ]
            },
            "Super Adjustable": {
                "patterns": [
                    "Black.*Beauty",
                    "Super.*adjust",
                    r"gil.*et.*\bbb\b",
                    "super.*109",
                ]
            },
            "Super Blue": {"patterns": [r"super\s*blue"]},
            "Super Speed": {
                "patterns": [
                    "Super.*speed",
                    "(red|black|blue|flare|flair).*tip",
                    r"gillette.*tto(\W|$)",
                    r"gil.*\bss\b",
                    r"\d\ds*\s*\bss\b",
                    "TV special",
                    "gil.*rocket",
                    "rocket.*hd",
                    r"gil.*mii*lord",
                ]
            },
            "Toggle": {"patterns": ["Toggle"]},
            "Tech": {
                "patterns": [
                    r"^(?!.*milord).*(gil|war|contract|slot|triangle|flat|hybrid|canada|english).*Tech",
                    "fbt",
                    r"triangle\s*slot",
                ]
            },
        },
        "Goodfellas Smile": {
            "Bayonetta": {"patterns": ["bayonett?a"]},
            "Legione Slant": {"patterns": ["legione"]},
            "Syntesi": {"patterns": ["syntesi"]},
            "Valynor": {"patterns": ["valyn"]},
        },
        "Greencult": {
            "GC 2.0": {"patterns": ["GC.*2", "green.*cult"]},
        },
        "Headblade": {
            "ATX": {"patterns": ["headbl.*atx"], "format": "Cartridge"},
        },
        "Handlebar": {
            "Shaving Company Dali": {"patterns": ["handlebar.*dali"]},
        },
        "Henson": {
            "AL13": {
                "patterns": ["henson", "(henson)?.*al13|lakdgjljagdlglklkaglkjgjkagkl"]
            },
            "Ti22": {"patterns": ["henson.*ti", "ti22", "ti.*henson"]},
        },
        "Hoffritz": {
            "Slant": {"patterns": ["hoff?ritz(.*\bslant\b)?"]},
        },
        "Homelike": {
            "START": {"patterns": ["Homelike.*start"]},
        },
        "iKon": {
            "101": {"patterns": ["ikon.*101"]},
            "102": {"patterns": ["ikon.*102"]},
            "103": {"patterns": ["ikon.*103"]},
            "B1": {"patterns": ["ikon.*b1"]},
            "SBS": {"patterns": ["ikon.*sbs"]},
            "Short Comb": {"patterns": ["ikon.*short"]},
            "Tek": {"patterns": ["ikon.*tek"]},
            "X3": {"patterns": ["ikon.*x3"]},
        },
        "J A Henckels": {
            "Straight": {
                "patterns": [
                    r"friodur(\s+straight)*",
                    r"Henckels(\s+straight)*",
                    r"henkels(\s+straight)*",
                ],
                "format": "Straight",
            },
        },
        "Kampfe": {
            "Star Lather Catcher 1902 ": {
                "patterns": ["kampfe(.*1902)?", "1902.*lather"],
                "format": "Wedge",
            },
        },
        "Karve": {
            "Bison": {"patterns": ["(karve)?.*bison"]},
            "Christopher Bradley": {
                "patterns": ["karve", "(karve)?.*cb", "christopher.*brad"]
            },
            "Overlander": {"patterns": ["(over|out)lander"]},
        },
        "Kai": {
            "Captain Folding": {"patterns": ["kai.*captain.*fold"], "format": "AC"},
            "Captain Kamisori": {
                "patterns": ["kai.*captain.*(kami|cloneisori)"],
                "format": "AC",
            },
            "Excelia Kamisori": {"patterns": ["kai.*excelia"], "format": "AC"},
        },
        "King C Gillette": {
            "": {"patterns": ["k*.*c.*gil.*et", "gil.*et.*king.*c"]},
        },
        "Koraat": {
            "Straight": {"patterns": [r"koraat(\s+straight)*"], "format": "Straight"},
        },
        "Krisp Beauty": {
            "DE Safety Razor": {"patterns": ["krisp"]},
        },
        "Krect": {
            "Spiral Slant": {"patterns": ["krect"]},
        },
        "KureNai": {
            "GF35": {"patterns": ["kurenai.*35"]},
            "GF36s": {"patterns": ["kurenai.*36"]},
        },
        "Lambda": {
            "Athena": {"patterns": [r"lambda\s*athena"]},
        },
        "LASSCo": {
            "BBS-1": {"patterns": ["BBS-*1"]},
        },
        "Leaf": {
            "Twig": {
                "patterns": ["leaf", r"(?:leaf)?\s*twig"],
                #  "format": "Half DE"
            },
            "Thorn": {
                "patterns": [r"(?:leaf)?\s*thorn"],
                #   "format": "Half DE"
            },
        },
        "Like Grandpa": {
            "Razor": {"patterns": ["like.*grandpa"]},
        },
        "Lord": {
            "L5": {"patterns": ["lord.*l5"]},
            "L6": {"patterns": ["lord.*l6"]},
        },
        "Maggard": {
            "Slant": {"patterns": ["mag.*ard.*slant", "mr.*slant"]},
            "SS70": {"patterns": ["ss70", "maggard.*cnc"]},
            "V2": {"patterns": ["maggard.*V2", "maggard.*(oc|open)", "mr.*v2"]},
            "V3": {
                "patterns": [
                    "maggard",
                    "Maggard.*V3",
                    "Maggard.*M3",
                    "V3",
                    r"MR\d{1,2}",  # assume folks who ordered a full maggard razor and listed it as such went with V3
                ]
            },
        },
        "Merkur": {
            "15C": {"patterns": ["(merkur.*)?15c"]},
            "23C": {"patterns": ["(merkur.*)?23-?[bc]"]},
            "24C": {"patterns": ["(merkur.*)?24c"]},
            "33C": {"patterns": ["(merkur.*)?33-*c"]},
            "34C": {"patterns": ["(merkur.*)?34-*[cg]", "merk.*hd", "^HD$", "merkur"]},
            # "34G": ["34g"], # 34G is just a color variety of 34C so collapse them
            "37C": {"patterns": ["(merkur.*)?37c", "merkur.*37c.*(slant)*"]},
            "38C": {"patterns": ["(merkur.*)?38c"]},
            "39C": {"patterns": ["(merkur.*)?39c"]},
            "41C": {"patterns": ["(merkur.*)?41c"]},
            "43C": {"patterns": ["(merkur.*)?43c"]},
            "45": {"patterns": ["(merkur.*)?45"]},
            "51C": {"patterns": ["(merkur.*)?51c"]},
            "Futur": {"patterns": [r"^(?!.*clone).*(merkur)?.*futur"]},
            "Progress": {"patterns": ["(pro|mer|di)gress"]},
            "Vision": {"patterns": ["vision"]},
        },
        "Mongoose": {
            "Original": {"patterns": ["goose"], "format": "AC"},
            "Alumigoose": {"patterns": ["al[iu]migoose"], "format": "AC"},
            "II": {"patterns": ["goose.*(2|two|ii)"], "format": "AC"},
        },
        "Muninn Woodworks": {
            "Sextoblade": {"patterns": ["mun+in.*sexto"], "format": "Hair Shaper"},
        },
        "Mühle": {
            "Companion": {"patterns": ["companion"]},
            "R41": {"patterns": ["R ?(41|103)"]},
            "R89": {"patterns": ["R(89|106)", "m[uü]hle.*89"]},
            "Rocca": {"patterns": ["(m[uü]hle)?.*rocca"]},
        },
        "Noble Otter": {
            "DE": {"patterns": ["NOC(1|2)", "NO(1|2)C", r"NOB\d", r"nobc\d"]},
        },
        "Oberon": {
            "Safety Razor": {"patterns": ["Oberon"]},
        },
        "Occams Razor": {
            "Enoch": {"patterns": ["enoch"], "format": "AC"},
        },
        "OneBlade": {
            "Core": {"patterns": ["oneblade.*core"], "format": "FHS"},
            "Dawn": {"patterns": ["oneblade.*dawn"], "format": "FHS"},
            "Element": {"patterns": ["oneblade.*element"], "format": "FHS"},
            "Genesis": {"patterns": ["oneblade.*genesis"], "format": "FHS"},
            "Hybrid": {"patterns": ["oneblade.*hybrid"], "format": "FHS"},
        },
        "Other": {
            "DE Clone":
            # make sure this is long enough to get evaluated first
            # matches any clone except "futur clone"
            {"patterns": [r"^(?!.*\bfutur\b).*(\bclone|knock-?off|kinghood)\b.*"]},
            "Shavette": {
                "patterns": ["shavette", "daune", "hess.*ezy", "hair.*sha"],
                "format": "AC",
            },
            "Straight Razor": {
                "patterns": [
                    r"(&|and)\s+son",
                    r"\d{1,2}/(8|16)",
                    "20th.*Century.*Mfg.*HH",
                    "alberta",
                    "case.*red",
                    "Cattaraugus",
                    "diamondine",
                    "ditzer",
                    "dubl.*duck",
                    "engels",
                    "frameback",
                    "fred.*Reynolds?",
                    "french.*point",
                    "friedr.*herd",
                    "gold.*dollar",
                    "green.*lizard",
                    "hadoson",
                    "henkotsu",
                    "hollow",
                    r"joseph\s*(elliot|allen)",
                    "kamisori",
                    "leger",
                    "maher.*grosh",
                    "otto.*busc?h",
                    "red.*imp",
                    "robeson",
                    "solingen",
                    "straight",
                    "suzumasa",
                    "thomas.*turner",
                    "tornblom",
                    "torrey",
                    "wacker",
                    "wedge",
                    "wester.*brothers",
                    "wostenholm",
                    "yankee.*cutlery",
                    # 'chani|trillian|triilian|mariko',# SSS named razors
                ],
                "format": "Straight",
            },
        },
        "PAA": {
            "Ascension": {"patterns": ["(phoenix|p\.?a\.?a\.?).*ascen"]},
            "Alpha Ecliptic": {"patterns": ["alpha.*ecli"]},
            "Bakelite Slant": {"patterns": ["(phoenix|p\.?a\.?a\.?).*bake.*slant"]},
            "DOC": {
                "patterns": [
                    "(phoenix|p\.?a\.?a\.?).*doc",
                    "(phoenix|p\.?a\.?a\.?).*double.*comb",
                ]
            },
            "La Criatura": {"patterns": ["criatura"]},
            "Meta-4": {"patterns": ["(phoenix|p\.?a\.?a\.?).*meta"]},
        },
        "Paradigm": {
            "17-4": {"patterns": ["parad.*17"]},
            "Diamondback": {"patterns": ["parad.*diam"]},
            "Salient": {
                "patterns": ["parad.*sal.*"],
            },
            "SE": {"patterns": ["parad.*se"], "format": "AC"},
            "Ti Diamondback": {
                "patterns": ["parad.*ti", "parad.*ti.*diam", "parad.*diam.*ti"]
            },
            "Ti II": {"patterns": ["parad.*ii"]},
        },
        "Paragon": {
            "Don": {"patterns": ["paragon.*don"]},
        },
        "Parker": {
            "A1R": {"patterns": ["parker.*a1r"]},
            "11R": {"patterns": ["parker.*11r"]},
            "22R": {"patterns": ["parker.*22R"]},
            "24C": {"patterns": ["parker.*24C"]},
            "29L": {"patterns": ["29L"]},
            "60R": {"patterns": ["60R"]},
            "66R": {"patterns": ["66R"]},
            "87R": {"patterns": ["87R"]},
            "90R": {"patterns": ["90R"]},
            "91R": {"patterns": ["91R"]},
            "96R": {"patterns": ["96R"]},
            "98R": {"patterns": ["98R"]},
            "99R": {"patterns": ["99R"]},
            "111W": {"patterns": ["111W"]},
            "Semi Slant": {"patterns": ["parker.*semi.*sla"]},
            "SoloEdge": {"patterns": ["parker.*solo"]},
            "SR1": {"patterns": ["parker.*sr1"]},
            "SRX": {"patterns": ["parker.*srx"]},
            "SRW": {"patterns": ["parker.*srw"]},
            "Variant": {"patterns": ["variant"]},
        },
        "Pearl": {
            "L-55": {"patterns": ["l-?55"]},
            "Flexi": {"patterns": ["Pearl.*flex"]},
            "Blaze": {"patterns": ["Pearl.*blaz"]},
        },
        "Personna": {
            "BBS-0": {"patterns": ["bbs-0", "person.*bbs.*0"]},
        },
        "PILS": {
            "": {"patterns": ["pils.*10", "^pils$"]},
        },
        "Portland Razor Co.": {
            "Straight": {
                "patterns": [r"portland.*(razor)?(\s+straight)*"],
                "format": "Straight",
            },
        },
        "Proof": {
            "Razor": {"patterns": [r"(\bhigh\s*)?proof\b"]},
        },
        "QShave": {
            "Parthenon": {"patterns": ["parthenon"]},
        },
        "Ralf Aust": {
            "Straight": {
                "patterns": [r"ralf.*aust(\s+straight)*"],
                "format": "Straight",
            },
        },
        "Raw Shaving": {
            "RS-10": {"patterns": ["rs-*10"]},
            "RS-18": {"patterns": ["rs-*18"]},
        },
        "Razorine": {
            "": {"patterns": ["razorine"]},
        },
        "RazoRock": {
            "Baby Smooth": {"patterns": ["ba*by.*smooth", "razorock.*bbs"]},
            "DE1": {"patterns": ["razorock.*de1"]},
            "Eco": {
                "patterns": ["eco"],
                # "format": "Half DE"
            },
            # 'Game Changer .84': ['game.*changer.*84', 'gc.*84', 'game.*changer'],
            # 'Game Changer .84 JAWS': ['JAWS'],
            # 'Game Changer .68': ['game.*changer.*68', 'gc.*68'],
            "Game Changer": {
                "patterns": ["game.*changer?", "gc", "game.*center", "game.*ganger"]
            },
            "German 37 Slant": {
                "patterns": [
                    r"german.*\b37\b",
                    r"slant.*\b37\b",
                    r"\b37\b.*slant",
                ]
            },
            "Hawk v1": {"patterns": ["(razorock)?.*hawk.*1"], "format": "AC"},
            "Hawk v2": {"patterns": ["(razorock)?.*hawk", "hawk.*2"], "format": "AC"},
            "Hawk v3": {"patterns": ["(razorock)?.*hawk.*3a?"], "format": "AC"},
            "Lupo": {"patterns": [r"lupp?o.*(\.?\d\d)?"]},
            "Mamba": {"patterns": ["ma[nm]ba"]},
            "Mentor": {"patterns": ["mentor.*(base)?"]},
            "Mission": {"patterns": ["mission"]},
            "MJ-90": {"patterns": ["mj-*90"]},
            "SLOC": {"patterns": ["sloc"]},
            "Stealth Slant": {"patterns": ["stealth.*slant"]},
            "Superslant": {"patterns": ["super\s*slant"]},
            "Teck II": {"patterns": ["teck"]},
            "Wunderbar Slant": {"patterns": ["wunderbar"]},
        },
        "Rex": {
            "Ambassador": {
                "patterns": ["rex.*ambassador", "ambassador.*(rex)?", r"rex.*\d"]
            },
            "Envoy": {"patterns": ["(rex)?.*envoy"]},
            "Konsul": {"patterns": ["konsul"]},
            "Sentry": {"patterns": ["sentry"]},
        },
        "Robin": {
            "Snap 2.0": {
                "patterns": ["robin.*snap"],
                #  "format": "Half DE"
            },
        },
        "Rockwell": {
            "2C": {"patterns": ["rockwell.*2C", "2C"]},
            "6C": {"patterns": ["rockwell.*6C", "rockwell", "6c"]},
            "6S": {"patterns": ["rockwell.*6S", "6s"]},
            "T2": {"patterns": [r"rockwell.*\bT2?\b", "t2"]},
        },
        "Rocnel": {
            "Elite 2019": {"patterns": ["Roc.*elite.*2019", "2019.*Roc.*elite"]},
            "Sailor": {"patterns": ["Roc.*sail"]},
        },
        "Rocky Mountain Barber": {
            "Double Edge Safety Razor": {"patterns": ["rocky moun"]},
        },
        "Rolls": {
            "Razor": {"patterns": ["rolls.*(razor)?"], "format": "Rolls"},
        },
        "Romer-7": {
            "Wazir": {"patterns": [r"wazir"]},
            "CS11": {"patterns": [r"romer.*CS[\s-]*11"]},
        },
        "SCS": {
            "Model A": {"patterns": ["simple.*clean.*shave", r"\bscs\b"]},
        },
        "Schick": {
            "Hydromagic": {"patterns": [r"hydro[\-\s]*magic"], "format": "Injector"},
            "Eversharp": {"patterns": [r"ever\s*sharp"], "format": "Injector"},
            "Injector": {
                "patterns": [
                    # "Schick.*Injector",
                    # "schick.*type",
                    "golden.*500",
                    # "schick.*grip",
                    "schl?ick",
                    "lad(y.|ies)*eversharp",
                    "injector",
                ],
                "format": "Injector",
            },
            "Krona": {"patterns": ["krona"]},
            "BBR-1J Kamisori Shavette": {"patterns": ["schick.*kami"], "format": "AC"},
            # "Proline Folding Shavette": ["schick.*proline"],
        },
        "Shavent": {
            "Razor": {
                "patterns": [
                    "shavent",
                ]
            },
        },
        "Shield": {
            "Avenger": {"patterns": ["shield.*avenger", "shield.*ac"], "format": "AC"},
            "Evolution": {"patterns": ["shield.*evo"], "format": "AC"},
            "Predator": {"patterns": ["shield.*pred"]},
        },
        "Smart-Helix": {
            "Apollo": {"patterns": ["helix.*apol"]},
        },
        "Star": {
            "1912": {"patterns": ["star.*1912"], "format": "GEM"},
            "Double Edge": {"patterns": ["star.*de"]},
        },
        # "Standard": {
        #     "Razor": {
        #         "patterns": [
        #             "standard.*razor",
        #             "^standard$",
        #             "standard.*(black|raw)",
        #             "(raw|black).*standard",
        #         ]
        #     }
        # },
        "Stirling": {
            "Slant": {"patterns": ["stirling.*slant"]},
            "DE3P6S": {"patterns": ["DE3P6S"]},
            "DE3P7S": {"patterns": ["DE3P7S"]},
            "Stainless DE Razor": {
                "patterns": [
                    "st[ei]rling.*stain",
                    "st[ei]rling.*(ss|hyper|ha|stai)",
                    "st[ei]rling",
                ]
            },
        },
        "Superior Cuts": {
            "": {
                "patterns": [r"superior\s*cuts"],
            },
        },
        "Supply": {
            "SE": {
                "patterns": [
                    "sup.*ly.*inject",
                    "sup.*ly.*2",
                    r"^(?!.*sentry).*supply.*se",
                ],
                "format": "Injector",
            },
        },
        "Tatara": {
            "Nodachi": {
                "patterns": ["ta.*nodachi", "masadachi", "masamodachi", "tatara.*dachi"]
            },
            # matusumi is a common mispelling apparently
            "Masamune": {"patterns": ["masamune", "Matusumi", "tatara"]},
            "Muramasa": {"patterns": ["muramasa"]},
        },
        "Tedalus": {
            "Essence Shavette": {"patterns": ["tedalus"], "format": "AC"},
        },
        "Thiers Issard": {
            "Straight": {
                "patterns": [r"th.*iss?ard(.*straight)?"],
                "format": "Straight",
            },
        },
        "Timeless": {
            "Razor": {
                "patterns": [
                    r"\btime?less?\b.*(\.?\d\d)?",
                ]
            },
            # "Slim": {"patterns": ["timeless.*slim"]},
            # "(Unspecified)": {"patterns": ["timeless"]},
            # ".68": {"patterns": ["timeless.*68", "t(i|l).*68"]},
            # ".95": {"patterns": ["timeless.*95", "95.*timeless"]},
            # "Aluminum": {"patterns": ["timeless.*alumi"]},
            # "Bronze": {"patterns": ["timeless.*bronze"]},
        },
        "The Holy Black": {
            "SR-71": {"patterns": ["sr-*71"]},
        },
        "TRC": {
            "Razor": {"patterns": [r"\btrc\b"]},
        },
        "Valet": {
            "Autostrop": {"patterns": ["valet", "autostrop"], "format": "FHS"},
        },
        "Van Der Hagen": {
            "Razor": {"patterns": ["Van Der Haa*gen", r"\bvdh\b"]},
        },
        "Viking": {
            "Revolution": {"patterns": ["vik.*rev"]},
        },
        "Wade & Butcher": {
            "Straight": {
                "patterns": [
                    r"wade.*butcher(\s+straight)*",
                    r"w&b\s+straight",
                ],
                "format": "Straight",
            },
        },
        "WCS": {
            "77": {"patterns": ["77-*S", "WCS.*77"]},
            "78": {"patterns": ["78-*BL", "78M", "(wcs|west).*78"]},
            "84": {"patterns": ["84-*R*B", "WCS.*84"]},
            "88": {"patterns": ["88-*S", "WCS.*88"]},
            "American Liberty (designed by Charcoal Goods)": {
                "patterns": ["wcs.*liberty", "wcs.*patriot"]
            },
            "El Capitan": {"patterns": [r"el\s*capitan"]},
            "Hyperion": {"patterns": ["hyperion"]},
            "Hollywood Palm": {"patterns": ["hollywood.*palm"]},
            "Lithe (designed by Charcoal Goods)": {"patterns": ["wcs.*lithe"]},
            "Multi Titanium Collection Razor": {
                "patterns": [r"(W\.?C\.?S\.?|West Coast Shaving).*titanium"]
            },
        },
        "Weber": {
            "ARC": {"patterns": ["weber.*arc"]},
            "DLC": {"patterns": ["weber.*dlc", "weber"]},
            "PH": {"patterns": ["weber.*ph"]},
        },
        "Weck": {
            "Sextoblade": {"patterns": ["Sextoblade", "weck"], "format": "Hair Shaper"},
            "Hair Shaper": {"patterns": ["weck.*hair"], "format": "Hair Shaper"},
            "450-110": {"patterns": ["450-110"], "format": "Hair Shaper"},
            "Med Prep": {"patterns": ["weck.*med.*prep"], "format": "Hair Shaper"},
        },
        "Weishi": {
            "Adjustable": {"patterns": ["weishi.*adj."]},
            "9306": {"patterns": ["weishi"]},
        },
        "Wilkinson Sword": {
            "Classic": {"patterns": ["wilk.*sword."]},
        },
        "Wizamet": {
            "Junior P-1": {"patterns": [r"\bp-?1\b", "wizamet"]},
        },
        "Wolfman": {
            "Guerilla": {
                "patterns": [
                    "guerr*ill*a",
                    "wolf.*uag",
                    "^uag$",
                    "^uag",
                    "uag$",
                    r"uag\s*razor",
                ]
            },
            "WR1": {
                "patterns": [
                    r"(Wolfman)?.*WR[\s-]*1",  # this will be evaluated first, as will the wr2 variant, so we will be as specfic as possible
                    "Wolfman",  # assume if not specified that it is a WR1?
                ]
            },
            "WR2": {"patterns": [r"(Wolfman)?.*WR[\s-]*2"]},
            "WR3": {"patterns": [r"(Wolfman)?.*WR[\s-]*3"], "format": "GEM"},
            "WR4": {"patterns": [r"(Wolfman)?.*WR[\s-]*4"], "format": "AC"},
        },
        "Yates": {
            "921": {"patterns": [r"921-*\w", "(yates|ypm).*921", "921.*yates", "921"]},
            # "BYOR": {"patterns": [r"yates\s+(?!Winning|Merica|921)\S*\s+(M|E|EH)"]},
            "'Merica": {"patterns": [r"('|\s|^)merica"]},
            "Winning": {"patterns": ["winning.*razor", "winning"]},
        },
        "Yaqi": {
            "Adjustable TFC": {"patterns": ["yaqi.*tfc", "yaqi.*adj", "yaqi.*final"]},
            "Beast": {"patterns": ["yaqi.*beast"]},
            "Bohemia": {"patterns": ["yaqi.*bohem"]},
            "DLC": {"patterns": ["yaqi.*dlc"]},
            "Excalibur": {"patterns": ["yaqi.*excal"]},
            "Flipside": {"patterns": ["yaqi.*flip"]},
            "Katana": {
                "patterns": ["yaqi.*katana"],
                #    "format": "Half DE"
            },
            "Remus": {"patterns": ["yaqi.*remus"]},
            "Slant": {"patterns": ["yaqi.*slant"]},
            "Sputnik": {"patterns": ["yaqi.*sput"]},
            "Telstar": {"patterns": ["yaqi.*telstar"]},
            "Zephyr": {"patterns": ["yaqi.*zaph"]},
        },
        "Yintal": {
            "Adjustable": {"patterns": ["yintal.*adj"]},
        },
    }

    @cached_property
    def __mapper(self):
        output = {}
        for brand, model_map in self._raw.items():
            for model, property_map in model_map.items():
                for pattern in property_map["patterns"]:
                    format = (
                        property_map["format"] if "format" in property_map else "DE"
                    )

                    output[pattern] = {
                        "brand": brand,
                        "model": model,
                        "name": f"{brand} {model}".strip(),
                        "format": format,
                    }
        return output

    @lru_cache(maxsize=None)
    def _get_value(self, input_string: str, field: str) -> str:
        regexes = sorted(self.__mapper.keys(), key=len, reverse=True)
        for alt_name_re in regexes:
            if re.search(alt_name_re, input_string, re.IGNORECASE):
                property_map = self.__mapper[alt_name_re]
                if field in property_map:
                    return property_map[field]
        return None


if __name__ == "__main__":
    rp = RazorParser()
    # print(arn.all_entity_names)
