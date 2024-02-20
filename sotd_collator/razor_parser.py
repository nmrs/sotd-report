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
                    "(?:att|tie).*h-*1",
                    "(atlas|bamboo|calypso|colossus|kronos).*h1",
                ],
            },
            "H2": {
                "patterns": [
                    "(?:att|tie).*h-*2",
                    "(?:atlas|bamboo|calypso|colossus|kronos).*h2",
                ],
            },
            "R1": {
                "patterns": [
                    "(?:att|tie).*r-*1",
                    "(?:atlas|bamboo|calypso|colossus|kronos).*r1",
                ],
            },
            "R2": {
                "patterns": [
                    "(?:att|tie).*r-*2",
                    "(?:atlas|bamboo|calypso|colossus|kronos).*r2",
                ],
            },
            "S1": {
                "patterns": [
                    "(?:att|tie).*s-*1",
                    "(?:atlas|bamboo|calypso|colossus|kronos).*s1",
                ],
            },
            "S2": {
                "patterns": [
                    "(?:att|tie).*s-*2",
                    "(?:atlas|bamboo|calypso|colossus|kronos).*s2",
                ],
            },
            "SE1": {
                "patterns": [
                    "(?:att|tie).*se-*1*",
                    "(?:atlas|bamboo|calypso|colossus|kronos).*se1",
                ],
                "format": "AC",
            },
            "Windsor Pro SB90": {
                "patterns": ["(?:ATT|tie).*sb90", "(?:ATT|tie).*wind"],
            },
        },
        "Alpha": {
            "Outlaw": {
                "patterns": ["alpha.*outl"],
            },
        },
        "Asylum": {
            "Evolution": {"patterns": ["asylum.*evo"], "format": "AC"},
            "Rx V2": {"patterns": ["asylum.*rx"], "format": "AC"},
        },
        "Atelier Durdan": {
            "Vestige": {"patterns": ["dur.*vestig"], "format": "GEM"},
            "Mauritius": {
                "patterns": ["dur.*mauri"],
            },
        },
        "Aylsworth": {
            "Drakkant": {"patterns": ["drakk?ant"]},
            "Kopparkant": {"patterns": ["kopp?arkant"]},
        },
        "Baili": {
            "BR1xx": {"patterns": [r"(baili|BR)(\s|-)*(1|2)\d{2}", "baili.*tto"]},
        },
        "Barbaros": {
            "TR-2": {"patterns": ["barbaros"]},
            "TR-3": {"patterns": ["barbaros.*tr3"]},
        },
        "BBNY": {"Safety Razor": {"patterns": ["bbny"]}},
        "Bevel": {"Razor": {"patterns": ["bevel"]}},
        "Blackland": {
            "Blackbird": {"patterns": [r"black\s*bird", r"bb\s*(sb|oc)", "brassbird"]},
            "Dart": {"patterns": [r"\bdart\b"]},
            "Era": {"patterns": ["black.*era", r"\bera\b"]},
            "Sabre": {"patterns": ["sabre"], "format": "GEM"},
            "Tradere": {"patterns": ["tradere"]},
            "Vector": {"patterns": ["vector"], "format": "AC"},
        },
        "Blutt Rasur": {"BR-1": {"patterns": ["blutt?"]}},
        "Boker": {
            "Straight": {"patterns": [r"Boker(\s+straight)*"], "format": "Straight"}
        },
        "Broman": {
            "Razor": {"patterns": ["broman"]},
            "Razor Mark II": {"patterns": [r"broman\s*(mark|mk)\s*(?:two|2|ii)"]},
        },
        "Cartridge / Disposable": {
            "": {
                "patterns": [
                    "cartridge",
                    "disposable",
                    "atra",
                    r"mach\s*(3|iii)",
                    "fusion",
                    r"gil.*et.*labs",
                    "trac2",
                ],
                "format": "Cart",
            }
        },
        "Carbon": {
            "Cx": {
                "patterns": [
                    "carbon.*cx",
                    "carbon.*shav.*com",
                    "carbon.*316",
                    "carbon.*orig",
                ]
            },
        },
        "Charcoal Goods": {
            "Everyday": {"patterns": ["(char|cg).*every"]},
            "Lvl 1": {"patterns": ["(?:char.*l|cg).*(1|one|i)"]},
            "Lvl 2": {"patterns": ["(?:char.*l|cg).*(2|two|ii)"]},
            "Lvl 3": {"patterns": ["(?:char.*l|cg).*(3|three|iii)"]},
            "Lithe Head": {"patterns": ["lithe"]},
        },
        "Chiseled Face": {
            "Legacy": {
                "patterns": [
                    "chiseled.*face.*(ti|legacy|alum)",
                    "cfl*.*(ti|legacy|alum)",
                ]
            }
        },
        "CJB": {"Shavette": {"patterns": ["cjb*vett*e"], "format": "AC"}},
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
        },
        "Enders": {
            "Speed Shaver": {"patterns": ["enders"], "format": "Enders"},
        },
        "Ever Ready": {
            "1912": {
                "patterns": [r"(?:ever|er).*1912", r"1912.*(?:ever|er)"],
                "format": "GEM",
            },
            "1914": {
                "patterns": [r"(?:ever|er).*1914", r"1914.*(?:ever|er)"],
                "format": "GEM",
            },
            "1924": {
                "patterns": [
                    r"(ever|er).*1924",
                    r"1924.*(ever|er)",
                    r"shovel\s*head",
                    "gem.*1924",
                ],
                "format": "GEM",
            },
            "Streamline": {
                "patterns": [r"(?:ever|er).*stream\s*line", r"^stream\s*line$"],
                "format": "GEM",
            },
            "E-Bar": {"patterns": [r"(ever|er).*e-bar"], "format": "GEM"},
            "G-Bar": {"patterns": [r"(ever|er).*g-bar"], "format": "GEM"},
        },
        "Executive Shaving": {"Outlaw": {"patterns": ["exec.*outlaw"]}},
        "Fatip": {
            "Grande": {"patterns": ["fa.*grande"]},
            "Gentile": {"patterns": ["fa.*gentile", "test.*genti.*"]},
            "Piccolo": {"patterns": ["fa.*picc*oll*o", "fati[.*spec]"]},
            "Lo Storto": {"patterns": ["fat.*storto"]},
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
                "patterns": [r"Filar*monica(\s+straight)*"],
                "format": "Straight",
            }
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
                ],
                "format": "GEM",
            },
            "Pushbutton": {"patterns": [r"gem.*push(\s|-)*button"], "format": "GEM"},
        },
        "Gibbs7": {
            "no. 17": {"patterns": ["gibbs.*17"]},
        },
        "Gillette": {
            "Aristocrat": {"patterns": ["art?istocrat"]},
            "Diplomat": {"patterns": ["Diplomat"]},
            "Fatboy": {"patterns": [r"fat\s*boy", "gil.*et.*195"]},
            "Goodwill": {"patterns": ["Gil.*et.*goodwill"]},
            "Guard": {"patterns": ["Gil.*et.*guard"], "format": "Cart"},
            "Heritage": {"patterns": ["Gil.*et.*heritage"]},
            "Knack": {"patterns": ["Gil.*et.*knack"]},
            "Lady Gillette": {"patterns": ["lady.*gil.*et", "gil.*et.*lady"]},
            "Milord": {"patterns": ["milord"]},
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
                    "old.*type",
                    "pocket.*ed",
                    "(single|double).*ring",
                    "big.*fellow",
                    "gil.*et.*bulldog",
                ]
            },
            "President": {"patterns": ["President"]},
            "Senator": {"patterns": ["senator"]},
            "Sheraton": {"patterns": ["sheraton"]},
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
                    "gil.*et.*bb",
                    "super.*109",
                ]
            },
            "Super Speed": {
                "patterns": [
                    "Super.*speed",
                    "(red|black|blue|flare|flair).*tip",
                    r"gillette.*tto(\W|$)",
                    "gil.*ss",
                    r"\d\ds*\s*ss",
                    "TV special",
                    "gil.*rocket",
                    "rocket.*hd",
                ]
            },
            "Toggle": {"patterns": ["Toggle"]},
            "Tech": {
                "patterns": [
                    "(gil|war|contract|slot|triangle|flat|hybrid|canada|english).*Tech",
                    "fbt",
                ]
            },
        },
        "Goodfellas Smile": {
            "Bayonetta": {"patterns": ["bayonett?a"]},
            "Legione Slant": {"patterns": ["legione"]},
            "Valynor": {"patterns": ["valyn"]},
        },
        "Greencult": {
            "GC 2.0": {"patterns": ["GC.*2"]},
        },
        "Headblade": {
            "ATX": {"patterns": ["headbl.*atx"], "format": "Cart"},
        },
        "Handlebar": {
            "Shaving Company Dali": {"patterns": ["handlebar.*dali"]},
        },
        "Henson": {
            "AL13": {"patterns": ["henson", "al13"]},
            "Ti22": {"patterns": ["henson.*ti", "ti22", "ti.*henson"]},
        },
        "Homelike": {
            "START": {"patterns": ["Homelike.*start"]},
        },
        "High Proof": {
            "Razpr": {"patterns": [r"high\s*proof"]},
        },
        "iKon": {
            "101": {"patterns": ["ikon.*101"]},
            "102": {"patterns": ["ikon.*102"]},
            "103": {"patterns": ["ikon.*103"]},
            "B1": {"patterns": ["ikon.*b1"]},
            "SBS": {"patterns": ["ikon.*sbs"]},
            "X3": {"patterns": ["ikon.*x3"]},
        },
        "J A Henckels:": {
            "Straight": {
                "patterns": [
                    r"friodur(\s+straight)*",
                    r"Henckels(\s+straight)*",
                    r"henkels(\s+straight)*",
                ],
                "format": "Straight",
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
            "": {"patterns": ["king.*c.*gil.*et", "gil.*et.*king.*c"]},
        },
        "Koraat": {
            "Straight": {"patterns": [r"koraat(\s+straight)*"], "format": "Straight"},
        },
        "KureNai": {
            "GF35": {"patterns": ["kurenai.*35"]},
            "GF36s": {"patterns": ["kurenai.*36"]},
        },
        "LASSCo": {
            "BBS-1": {"patterns": ["BBS-*1"]},
        },
        "Leaf": {
            "Twig": {"patterns": ["leaf", r"(?:leaf)?\s*twig"]},
            "Thorn": {"patterns": [r"(?:leaf)?\s*thorn"]},
        },
        "Like Grandpa": {
            "Razor": {"patterns": ["like.*grandpa"]},
        },
        "Lord": {
            "L6": {"patterns": ["lord.*l6"]},
        },
        "Maggard": {
            "Slant": {"patterns": ["mag.*ard.*slant", "mr.*slant"]},
            "SS70": {"patterns": ["ss70"]},
            "V2": {"patterns": ["maggard.*V2", "maggard.*(oc|open)", "mr.*v2"]},
            "V3M": {"patterns": ["maggard.*V3M", "V3M"]},
            "V3A": {"patterns": ["Maggard.*V3A", "V3A"]},
            "V3": {
                "patterns": [
                    "Maggard.*V3",
                    "Maggard.*M3",
                    "V3",
                    r"MR\d{1,2}",  # assume folks who ordered a full maggard razor and listed it as such went with V3
                ]
            },
        },
        "Merkur": {
            "15C": {"patterns": ["(merkur.*)?15c"]},
            "23C": {"patterns": ["(merkur.*)?23c"]},
            "24C": {"patterns": ["(merkur.*)?24c"]},
            "33C": {"patterns": [r"(merkur.*)?33\(*c"]},
            "34C": {
                "patterns": [r"(merkur.*)?34\(*(c|g)", "merk.*hd", "^HD$", "merkur"]
            },
            # "34G": ["34g"], # 34G is just a color variety of 34C so collapse them
            "37C": {"patterns": ["(merkur.*)?37c", "merkur.*37c.*(slant)*"]},
            "38C": {"patterns": ["(merkur.*)?38c"]},
            "39C": {"patterns": ["(merkur.*)?39c"]},
            "41C": {"patterns": ["(merkur.*)?41c"]},
            "43C": {"patterns": ["(merkur.*)?43c"]},
            "45": {"patterns": ["(merkur.*)?45"]},
            "51C": {"patterns": ["(merkur.*)?51c"]},
            "Futur": {"patterns": ["futur"]},
            "Mergress": {"patterns": ["mergress", "digress"]},
            "Progress": {"patterns": ["progress"]},
            "Vision": {"patterns": ["vision"]},
        },
        "Mongoose": {
            "Original": {"patterns": ["goose"], "format": "AC"},
            "Alumigoose": {"patterns": ["alumigoose"], "format": "AC"},
            "II": {"patterns": ["goose.*(2|two|ii)"], "format": "AC"},
        },
        "Mühle": {
            "Companion": {"patterns": ["companion"]},
            "R41": {"patterns": ["R41"]},
            "R89": {"patterns": [r"R10\d", "R89", "m(u|ü)hle.*89"]},
            "Rocca": {"patterns": ["rocca"]},
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
            {
                "patterns": [
                    r"^(?!.*\bfutur\b).*(?:\bclone\b.*|;alskdjhglk;jadslkgjadsl;kgjadlskgjl;kgdasjglkdjg)"
                ]
            },
            "Shavette": {
                "patterns": ["shavette", "daune", "hess.*ezy"],
                "format": "AC",
            },
            "Straight Razor": {
                "patterns": [
                    r"&\s+son",
                    "\d/(8|16)",
                    "20th.*Century.*Mfg.*HH",
                    "case.*red",
                    "Cattaraugus",
                    "diamondine",
                    "dubl.*duck",
                    "engels",
                    "frameback",
                    "fred.*Reynolds",
                    "french.*point",
                    "friedr.*herd",
                    "gold.*dollar",
                    "green.*lizard",
                    "hadoson",
                    "henkotsu",
                    "heljstrand",
                    "hollow",
                    "Issard",
                    r"joseph\s*(elliot|allen)",
                    "kamisori",
                    "red.*imp",
                    "straight",
                    "suzumasa",
                    "tornblom",
                    "torrey",
                    "wacker",
                    "wedge",
                    "wester.*brothers",
                    "wostenholm",
                    # 'chani|trillian|triilian|mariko',# SSS named razors
                ],
                "format": "Straight",
            },
        },
        "PAA": {
            "Alpha Ecliptic": {"patterns": ["alpha.*ecli"]},
            "Bakelite Slant": {"patterns": ["(phoenix|paa).*bake.*slant"]},
            "DOC": {"patterns": ["(phoenix|paa).*doc", "(phoenix|paa).*double.*comb"]},
        },
        "Paradigm": {
            "17-4": {"patterns": ["parad.*17"]},
            "Diamondback": {"patterns": ["parad.*diamondb"]},
            "Salient": {
                "patterns": ["parad.*sal.*"],
            },
            "SE": {"patterns": ["parad.*se"], "format": "AC"},
            "Ti": {"patterns": ["parad.*ti"]},
            "Ti II": {"patterns": ["parad.*ii"]},
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
            "SR1": {"patterns": ["parker.*sr1"]},
            "SRX": {"patterns": ["parker.*srx"]},
            "SRW": {"patterns": ["parker.*srw"]},
            "Variant": {"patterns": ["variant"]},
        },
        "Pearl": {
            "L-55": {"patterns": ["l-?55"]},
            "Flexi": {"patterns": ["Pearl.*flex"]},
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
            "Eco": {"patterns": ["eco"]},
            # 'Game Changer .84': ['game.*changer.*84', 'gc.*84', 'game.*changer'],
            # 'Game Changer .84 JAWS': ['JAWS'],
            # 'Game Changer .68': ['game.*changer.*68', 'gc.*68'],
            "Game Changer": {"patterns": ["game.*changer.", "gc", "game.*center"]},
            "German 37 Slant": {
                "patterns": [
                    r"german.*\b37\b",
                    r"slant.*\b37\b",
                    r"\b37\b.*slant",
                ]
            },
            "Hawk v1": {"patterns": ["hawk.*1"], "format": "AC"},
            "Hawk v2": {"patterns": ["hawk", "hawk.*2"], "format": "AC"},
            "Hawk v3": {"patterns": ["hawk.*3a?"], "format": "AC"},
            "Lupo": {"patterns": ["Lupp*o"]},
            "Mamba": {"patterns": ["mamba"]},
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
            "Envoy": {"patterns": ["envoy"]},
            "Konsul": {"patterns": ["konsul"]},
            "Sentry": {"patterns": ["sentry"]},
        },
        "Rockwell": {
            "2C": {"patterns": ["rockwell.*2C", "2C"]},
            "6C": {"patterns": ["rockwell.*6C", "rockwell", "6c"]},
            "6S": {"patterns": ["rockwell.*6S", "6s"]},
            "T2": {"patterns": ["rockwell.*T2", "t2"]},
        },
        "Rocnel": {
            "Elite 2019": {"patterns": ["Roc.*elite.*2019", "2019.*Roc.*elite"]},
        },
        "Rolls": {
            "Razor": {"patterns": ["rolls.*razor"], "format": "Rolls"},
        },
        "Romer-7": {
            "Wazir": {"patterns": ["romer-?7"]},
        },
        "SCS": {
            "Model A": {"patterns": ["simple.*clean.*shave", r"\bscs\b"]},
        },
        "Schick": {
            "Hydromagic": {"patterns": [r"hydro[\-\s]*magic"], "format": "Injector"},
            "Injector": {
                "patterns": [
                    # "Schick.*Injector",
                    # "schick.*type",
                    "golden.*500",
                    # "schick.*grip",
                    "schick",
                    "lad(y.|ies)*eversharp",
                    "injector",
                ],
                "format": "Injector",
            },
            "Krona": {"patterns": ["krona"]},
            "BBR-1J Kamisori Shavette": {"patterns": ["schick.*kami"], "format": "AC"},
            # "Proline Folding Shavette": ["schick.*proline"],
        },
        "Smart-Helix": {
            "Apollo": {"patterns": ["helix.*apol"]},
        },
        "Star": {
            "Double Edge": {"patterns": ["star.*de"]},
        },
        "Standard": {
            "Razor": {
                "patterns": [
                    "standard.*razor",
                    "^standard$",
                    "standard.*(black|raw)",
                    "(raw|black).*standard",
                ]
            }
        },
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
            "Nodachi": {"patterns": ["ta.*nodachi", "masadachi"]},
            # matusumi is a common mispelling apparently
            "Masamune": {"patterns": ["masamune", "Matusumi", "tatara"]},
            "Muramasa": {"patterns": ["muramasa"]},
        },
        "Timeless": {
            "Slim": {"patterns": ["Timeless.*slim"]},
            "(Unspecified)": {"patterns": ["Timeless"]},
            ".68": {"patterns": ["Timeless.*68", "t(i|l).*68"]},
            ".95": {"patterns": ["Timeless.*95", "95.*timeless"]},
            "Aluminum": {"patterns": ["Timeless.*alumi"]},
            "Bronze": {"patterns": ["Timeless.*bronze"]},
        },
        "The Holy Black": {
            "SR-71": {"patterns": ["sr-*71"]},
        },
        "TRC": {
            "Razor": {"patterns": [r"\btrc\b"]},
        },
        "Van Der Hagen": {
            "Razor": {"patterns": ["Van Der Haa*gen", "vdh"]},
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
            "78": {"patterns": ["78-*BL", "78M", "WCS.*78"]},
            "84": {"patterns": ["84-*R*B", "WCS.*84"]},
            "88": {"patterns": ["88-*S", "WCS.*88", "(wcs|west).*78"]},
            "El Capitan": {"patterns": [r"el\s*capitan"]},
            "Hyperion": {"patterns": ["hyperion"]},
            "Hollywood Palm": {"patterns": ["hollywood.*palm"]},
            "Multi Titanium Collection Razor": {
                "patterns": [r"(W\.?C\.?S\.?|West Coast Shaving).*titanium"]
            },
        },
        "Weber": {
            "ARC": {"patterns": ["weber.*arc"]},
            "DLC": {"patterns": ["weber.*dlc"]},
            "PH": {"patterns": ["weber.*ph"]},
        },
        "Weck": {
            "Sextoblade": {"patterns": ["Sextoblade"], "format": "Hair Shaper"},
            "Hair Shaper": {"patterns": ["weck.*hair"], "format": "Hair Shaper"},
            "450-110": {"patterns": ["450-110"], "format": "Hair Shaper"},
        },
        "Wilkinson Sword": {
            "Classic": {"patterns": ["wilk.*sword."]},
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
                    "Wolfman.*WR-*1",  # this will be evaluated first, as will the wr2 variant, so we will be as specfic as possible
                    "Wolfman",  # assume if not specified that it is a WR1
                    "WR-*1",  # catch the case where eg ntownuser just lists wr1 / wr2
                ]
            },
            "WR2": {"patterns": ["Wolfman.*WR-*2", "WR-*2"]},
            "WR3": {"patterns": ["Wolfman.*WR-*3", "WR-*3"], "format": "GEM"},
            "WR4": {"patterns": ["Wolfman.*WR-*4", "WR-*4"], "format": "AC"},
        },
        "Yates": {
            "921": {"patterns": [r"921-*\w", "(yates|ypm).*921", "921.*yates", "921"]},
            "BYOR": {"patterns": [r"yates\s+(?!Winning|Merica|921)\S*\s+(M|E|EH)"]},
            "'Merica": {"patterns": [r"('|\s|^)merica"]},
            "Winning": {"patterns": ["winning.*razor", "winning"]},
        },
        "Yaqi": {
            "DLC": {"patterns": ["yaqi.*dlc"]},
            "Excalibur": {"patterns": ["yaqi.*excal"]},
            "Slant": {"patterns": ["yaqi.*slant"]},
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
