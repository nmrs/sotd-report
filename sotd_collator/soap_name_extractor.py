import re
import unicodedata
from functools import cached_property
from sotd_collator.base_name_extractor import BaseNameExtractor


class SoapNameExtractor(BaseNameExtractor):
    """
    From a given comment, extract the brush size name
    """

    HTML_FIXUPS = [
        ("&#39;", "'"),
        ("&quot;", '"'),
        ("&amp;", "&"),
        ("!", ""),
        ("/", " / "),
    ]

    CASE_SENSITIVE_FIXUPS = [
        ("A&E", "Ariana & Evans"),
        ("AE", "Ariana & Evans"),
        ("APR", "Australian Private Reserve"),
        ("AP Reserve", "Australian Private Reserve"),
        ("BM", "Barrister and Mann"),
        ("CB", "Catie's Bubbles"),
        ("CL", "Chatillon Lux"),
        ("CF", "Chiseled Face"),
        ("DG", "Declaration Grooming"),
        ("M&M", "Murphy and McNeil"),
        ("MLS", "Mickey Lee Soapworks"),
        ("NO", "Noble Otter"),
        ("N.O", "Noble Otter"),
        ("PDP", "Pre de Provence"),
        ("PdP", "Pre de Provence"),
        ("P&B", "Phoenix & Beau"),
        ("PAA", "Phoenix Artisan Accoutrements"),
        ("SBSW", "Storybook Soapworks"),
        ("SV", "Saponificio Varesino"),
        ("SW", "Southern Witchcrafts"),
        ("TOBS", "Taylor of Old Bond Street"),
        ("WCS", "West Coast Shaving"),
        ("WK", "Wholly Kaw"),
        ("ZM", "Zingari"),
    ]

    CASE_INSENSITIVE_FIXUPS = [
        ("ariana&evans", "ariana & evans"),
        ("arianna & evans", "ariana & evans"),
        ("arianna and evans", "ariana & evans"),
        (
            "australian private reserve & southern witchcrafts",
            "australian private reserve / southern witchcrafts",
        ),
        (
            "australian private reserve x southern witchcrafts",
            "australian private reserve / southern witchcrafts",
        ),
        ("b&m", "barrister and mann"),
        ("b&m", "barrister and mann"),
        ("b+m", "barrister and mann"),
        ("bam", "barrister and mann"),
        ("b m ", "barrister and mann"),
        ("b & m", "barrister and mann"),
        ("barrister & mann", "barrister and mann"),
        ("barrister and man ", "barrister and mann "),
        ("barristers reserve", "barrister and mann reserve"),
        ("big soap energy", "bse"),
        ("bid soap energy", "bse"),
        ("blackship grooming", "black ship grooming"),
        ("caties bubbles", "catie's bubbles"),
        ("chiseled face groomatorium", "chiseled face"),
        ("dr jon's", "dr. jon's"),
        ("dr jons", "dr. jon's"),
        ("dr. jons", "dr. jon's"),
        ("lassc", "la shaving soap co."),
        ("ll grooming", "declaration grooming"),
        ("l &l grooming", "declaration grooming"),
        ("l&l grooming", "declaration grooming"),
        ("l&l", "declaration grooming"),
        ("maggard's", "maggard"),
        ("maggards", "maggard"),
        ("mammoth soap ", "mammoth soaps "),
        ("mickey lee soaps", "mickey lee soapworks"),
        ("murphy & mcneil", "murphy and mcneil"),
        ("pheonix and beau", "phoenix & beau"),
        ("phoenix and beau", "phoenix & beau"),
        ("proraso green", "proraso menthol and eucalyptus"),
        ("proraso white", "proraso aloe and vitamin e"),
        ("proraso red", "proraso sandalwood"),
        ("seville in reserve", "seville"),
        (" shs", "soft heart"),
        ("t+s", "tallow + steel"),
        ("t&s", "tallow + steel"),
        ("tallow & steel", "tallow + steel"),
        ("tallow and steel", "tallow + steel"),
        ("barts's", "bart"),
        ("odelight", "o delight"),
        ("pharoahs", "pharaoh's"),
        ("pharohs", "pharaoh's"),
        ("rambling man", "ramblin man"),
        ("shaving soap", ""),
        ("southern witchcraft ", "southern witchcrafts "),
        ("spearhead shaving co.", "spearhead shaving company"),
        ("taylor's", "taylor"),
        ("william's", "williams"),
        ("zingari man", "zingari"),
        ("yrp", "yuzu / rose / patchouli"),
    ]

    SKIP_WORDS = [
        "aftershave",
        "after shave",
        "balm",
        "grindermonk",
        "splash",
        "post:",
    ]

    DROP_WORDS = [
        "base",
        "bison",
        "by",
        "excelsior",
        "glissant",
        "icarus",
        "milksteak",
        "sample",
        "sego",
        "sierro",
        "siero",
        "terroraded",
        "tub",
        "vegan",
    ]

    @cached_property
    def detect_regexps(self):
        soap_name_re = r"""\w\t ./\-_()#;&\'\"|<>:$~,!+"""

        return [
            re.compile(
                r"^[*\s\-+/]*(?!lather games)(?:lather|soap)\s*[:*\-\\+\s/]+\s*([{0}]+)(?:\+|\n|$)".format(
                    soap_name_re
                ),
                re.MULTILINE | re.IGNORECASE,
            ),  # TTS and similar
            re.compile(
                r"\*(?!lather games)(?:lather|soap)\*:.*\*\*([{0}]+)\*\*".format(soap_name_re),
                re.MULTILINE | re.IGNORECASE,
            ),  # sgrddy
            re.compile(
                r"^[*\s\-+/]*(?!lather games)(?:lather|soap)\s*[:*\-\\+\s/]+\s*\[*([{0}]+)(?:\+|\n|$|]\()".format(
                    soap_name_re
                ),
                re.MULTILINE | re.IGNORECASE,
            ),  # TTS style with link to eg imgur
        ]

    @BaseNameExtractor.post_process_name
    def get_name(self, comment):
        if "soap" in comment:
            return comment["soap"]

        comment_text = self._to_ascii(comment['body'])
        for detector in self.detect_regexps:
            res = detector.search(comment_text)
            if res:
                # remove trailing - soap / cream
                name = re.sub(
                    r"\s*-*\s*(?:Soap|Cream|Soap \(Vegan\)|Soap \(LE\))\s*$",
                    "",
                    res.group(1),
                    flags=re.IGNORECASE,
                )

                # name fixups for B&M etc
                if name:
                    for skip in self.SKIP_WORDS:
                        if skip in name.lower():
                            return None

                    # remove words like 'base', 'excelsior
                    name = " ".join(
                        [x for x in name.split() if x.lower() not in self.DROP_WORDS]
                    )

                    for fixup in self.HTML_FIXUPS:
                        name = name.replace(fixup[0], fixup[1])

                    # remove double spaces
                    name = re.sub(r"\s{2,}", " ", name)

                    for fixup in self.CASE_SENSITIVE_FIXUPS:
                        name = name.replace(fixup[0], fixup[1])

                    # remove anything insside brackets
                    name = re.sub(r"\(.+\)", "", name)

                    # remove accents on fougere etc
                    name = (
                        unicodedata.normalize("NFKD", name)
                        .encode("ascii", "ignore")
                        .decode("ascii")
                    )

                    # remove double spaces
                    name = re.sub(r"\s{2,}", " ", name)

                    # declaration fixup
                    name = re.sub(
                        r"declaration(?!\sgrooming)",
                        "Declaration Grooming",
                        name,
                        flags=re.IGNORECASE,
                    )

                    name = re.sub(
                        r"st[ei]rling(?!\ssoap)",
                        "Stirling Soap Co.",
                        name,
                        flags=re.IGNORECASE,
                    )
                    name = re.sub(
                        r"st[ei]rling soap(?!\sco)",
                        "Stirling Soap Co.",
                        name,
                        flags=re.IGNORECASE,
                    )

                    # spearhead specific fixup
                    name = re.sub(
                        r"spearhead(?!\sshaving)",
                        "Spearhead Shaving Company",
                        name,
                        flags=re.IGNORECASE,
                    )
                    name = re.sub(
                        r"spearhead shaving(?!\sco)",
                        "Spearhead Shaving Company",
                        name,
                        flags=re.IGNORECASE,
                    )

                    # sbs specific fixup
                    name = re.sub(
                        r"summer break(?!\ssoaps)",
                        "Summer Break Soaps",
                        name,
                        flags=re.IGNORECASE,
                    )

                    # oleo fixup
                    name = re.sub(
                        r"(?!formerly\s)oleo",
                        "Chicago Grooming Co. (Formerly Oleo Soapworks)",
                        name,
                        flags=re.IGNORECASE,
                    )

                    name = re.sub(r"[-,]", " ", name)

                    # lowercase fixups
                    name = name.lower()
                    # remove double spaces
                    name = re.sub(r"\s{2,}", " ", name)

                    for fixup in self.CASE_INSENSITIVE_FIXUPS:
                        name = name.replace(fixup[0], fixup[1])

                    # remove double spaces
                    name = re.sub(r"\s{2,}", " ", name)

                    if len(name) < 4:
                        return None

                    return name.strip()

        return None
