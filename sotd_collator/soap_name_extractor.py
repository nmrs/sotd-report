import re
import unicodedata
from functools import cached_property
from sotd_collator.base_name_extractor import BaseNameExtractor


class SoapNameExtractor(BaseNameExtractor):
    """
    From a given comment, extract the brush size name
    """

    HTML_FIXUPS = [
        ('&#39;', "'"),
        ('&quot;', '"'),
        ('&amp;', '&'),
    ]

    NAME_FIXUPS = [
        ('A&E', 'Ariana & Evans'),
        ('AE', 'Ariana & Evans'),
        ('Ariana&Evans', 'Ariana & Evans'),
        ('Arianna & Evans', 'Ariana & Evans'),
        ('APR', 'Australian Private Reserve'),
        ('AP Reserve', 'Australian Private Reserve'),
        ('BM', 'Barrister and Mann'),
        ('B&M', 'Barrister and Mann'),
        ('b&m', 'Barrister and Mann'),
        ('B+M', 'Barrister and Mann'),
        ('BaM', 'Barrister and Mann'),
        ('Barrister & Mann', 'Barrister and Mann'),
        ('CB', "Catie's Bubbles"),
        ('Caties Bubbles', "Catie's Bubbles"),
        ('CL', "Chatillon Lux"),
        ('CF', "Chiseled Face"),
        ('DG', 'Declaration Grooming'),
        ('L&L Grooming', 'Declaration Grooming'),
        ('MLS', 'Mickey Lee Soapworks'),
        ('NO', 'Noble Otter'),
        ('N.O', 'Noble Otter'),
        ('PDP', 'Pre de Provence'),
        ('PdP', 'Pre de Provence'),
        ('Pheonix and Beau', 'Phoenix & Beau'),
        ('Phoenix and Beau', 'Phoenix & Beau'),
        ('P&B', 'Phoenix & Beau'),
        ('PAA', 'Phoenix Artisan Accoutrements'),
        ('Proraso Green', 'Proraso Menthol and Eucalyptus'),
        ('Proraso White', 'Proraso Aloe and Vitamin E'),
        ('Proraso Red', 'Proraso Sandalwood'),
        ('SV', 'Saponificio Varesino'),
        ('SW', 'Southern Witchcrafts'),
        ('T+S', 'Tallow + Steel'),
        ('T&S', 'Tallow + Steel'),
        ('Tallow & Steel', 'Tallow + Steel'),
        ('Tallow and Steel', 'Tallow + Steel'),
        ('TOBS', 'Taylor of Old Bond Street'),
        ('WCS', 'West Coast Shaving'),
        ('WK', 'Wholly Kaw'),
        ('Zingari Man', 'Zingari'),
        ('ZM', 'Zingari'),
    ]

    SKIP_WORDS = [
        'balm',
        'grindermonk',
        'splash',
    ]

    DROP_WORDS = [
        'base',
        'excelsior',
        'bison',
    ]

    @cached_property
    def detect_regexps(self):
        soap_name_re = r"""\w\t ./\-_()#;&\'\"|<>:$~,!+"""

        return [
            re.compile(r'^[*\s\-+/]*(?:Lather|Soap)\s*[:*\-\\+\s/]+\s*([{0}]+)(?:\+|\n|$)'.format(soap_name_re),
                       re.MULTILINE | re.IGNORECASE),  # TTS and similar
            re.compile(r'\*(?:Lather|Soap)\*:.*\*\*([{0}]+)\*\*'.format(soap_name_re), re.MULTILINE | re.IGNORECASE),  # sgrddy
            re.compile(r'^[*\s\-+/]*(?:Lather|Soap)\s*[:*\-\\+\s/]+\s*\[*([{0}]+)(?:\+|\n|$|]\()'.format(soap_name_re),
                       re.MULTILINE | re.IGNORECASE),  # TTS style with link to eg imgur
        ]

    @BaseNameExtractor.post_process_name
    def get_name(self, comment_text):
        comment_text = self._to_ascii(comment_text)
        for detector in self.detect_regexps:
            res = detector.search(comment_text)
            if res:
                # remove trailing - soap / cream
                name = re.sub(r'\s*-*\s*(?:Soap|Cream|Soap \(Vegan\)|Soap \(LE\))\s*$', '', res.group(1), flags=re.IGNORECASE)

                # name fixups for B&M etc
                if name:
                    for skip in self.SKIP_WORDS:
                        if skip in name.lower():
                            return None

                    # remove words like 'base', 'excelsior
                    name = ' '.join([x for x in name.split() if x.lower() not in self.DROP_WORDS])

                    for fixup in self.HTML_FIXUPS:
                        name = name.replace(fixup[0], fixup[1])

                    for fixup in self.NAME_FIXUPS:
                        name = name.replace(fixup[0], fixup[1])

                    # remove anything insside brackets
                    name = re.sub(r'\(.+\)', '', name)

                    # declaration fixup
                    name = re.sub(r'declaration(?!\sgrooming)', 'Declaration Grooming', name, flags=re.IGNORECASE)

                    name = re.sub(r'st[ei]rling(?!\ssoap)', 'Stirling Soap Co.', name, flags=re.IGNORECASE)
                    name = re.sub(r'st[ei]rling soap(?!\sco)', 'Stirling Soap Co.', name, flags=re.IGNORECASE)

                    # seaforth specific fixup
                    name = re.sub(r'spearhead(?!\sshaving)', 'Spearhead Shaving Company', name, flags=re.IGNORECASE)
                    name = re.sub(r'spearhead shaving(?!\sco)', 'Spearhead Shaving Company', name, flags=re.IGNORECASE)
                    name = re.sub(r'seaforth(?!\!)', 'Seaforth!', name, flags=re.IGNORECASE)

                    # sbs specific fixup
                    name = re.sub(r'summer break(?!\ssoaps)', 'Summer Break Soaps', name, flags=re.IGNORECASE)

                    # oleo fixup
                    name = re.sub(r'(?!formerly\s)oleo', 'Chicago Grooming Co. (Formerly Oleo Soapworks)', name, flags=re.IGNORECASE)

                    name = re.sub(r'[-,]', ' ', name)

                    # remove double spaces
                    name = re.sub(r'\s{2,}', ' ', name)

                    # remove accents on fougere etc
                    name = unicodedata.normalize('NFKD', name)

                    if len(name) < 4:
                        return None

                    return name.strip().lower()

        return None
