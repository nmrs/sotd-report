import re
import unicodedata
import urllib.request
import ssl
from diskcache import Cache

c = Cache(directory="/tmp")


class TtsScraper(object):
    ssl._create_default_https_context = ssl._create_unverified_context

    MANUAL_ADDITIONS = [
        "arko",
        "Siliski Soaps Unscented",
        "Zingari The Duo",
        "Zingari The Watchman",
    ]

    @classmethod
    @c.memoize()
    def get_tts_soaps(cls):
        def _fixup_soap_name(name):
            replacements = [
                ("-", " "),
                ("|", ""),
                ("!", ""),
                ("&#39;", "'"),
                ("&quot;", '"'),
                ("&amp;", "&"),
                ("/", " / "),
            ]
            if name:
                for replacement in replacements:
                    name = name.replace(*replacement)
                # remove accents on fougere etc
                name = (
                    unicodedata.normalize("NFKD", name)
                    .encode("ascii", "ignore")
                    .decode("ascii")
                )
                # remove double spaces
                name = re.sub(r"\s{2,}", " ", name)

            return name

        with urllib.request.urlopen("https://trythatsoap.com/soap/#!") as response:
            html = response.read()
            soaps = re.findall(
                r">([^<>]+) - (?:Soap|Cream|Soap \(Vegan\)|Soap \(LE\))</div",
                html.decode("utf-8"),
            )
            soaps.extend(cls.MANUAL_ADDITIONS)
            # make unique - we dont differentiate between variants of the same soap (eg vegan vs tallow)
            return list(set([_fixup_soap_name(x) for x in soaps]))
