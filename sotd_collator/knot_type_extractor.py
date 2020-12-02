import re
from functools import cached_property
from sotd_collator.base_name_extractor import BaseNameExtractor
from sotd_collator.razor_alternate_namer import RazorAlternateNamer


class KnotTypeExtractor(BaseNameExtractor):
    """
    Collate stats on knot type - eg silksmoke, cashmere, Bx, Gelousy etc
    """

    knot_types = [
                     {'name': '2BED', 'pattern': r'2bed'},
                     {'name': 'Bosss', 'pattern': r'boss'},
                     {'name': 'Cashmere', 'pattern': r'cashmere'},
                     {'name': 'Declaration Badger', 'pattern': r'B\d{1,2}'},
                     {'name': 'G4', 'pattern': r'g-*4'},
                     {'name': 'Gelousy', 'pattern': r'gelou*sy'},
                     {'name': 'Hawk', 'pattern': r'hawk'},
                     {'name': 'Plissoft', 'pattern': r'plissoft'},
                     {'name': 'Quartermoon', 'pattern': r'quartermoon'},
                     {'name': 'Silksmoke', 'pattern': r'silksmoke'},
                     {'name': 'SHD', 'pattern': r'shd'},
                     {'name': 'SynBad', 'pattern': r'synbad'},
                     {'name': 'Tuxedo', 'pattern': r'tuxedo'},
    ]

    @cached_property
    def detect_regexps(self):
        blade_name_re = r"""\w\t ./\-_()#;&\'\"|<>:$~"""

        return [
            re.compile(r'^[*\s\-+/]*brush\s*[:*\-\\+\s/]+\s*([{0}]+)(?:\+|,|\n|$)'.format(blade_name_re),
                       re.MULTILINE | re.IGNORECASE),  # TTS and similar
            re.compile(r'\*brush\*:.*\*\*([{0}]+)\*\*'.format(blade_name_re), re.MULTILINE | re.IGNORECASE),  # sgrddy

        ]


    @BaseNameExtractor.post_process_name
    def get_name(self, comment_text):
        comment_text = self._to_ascii(comment_text)
        extracted_name = None

        for detector in self.detect_regexps:
            res = detector.search(comment_text)
            if res:
                extracted_name = res.group(1)

        if not extracted_name:
            return None

        for knot_type in self.knot_types:
            if re.search(knot_type['pattern'], extracted_name, re.IGNORECASE):
                return knot_type['name']

        return None

