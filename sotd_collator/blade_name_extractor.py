import re
from functools import cached_property
from sotd_collator.blade_alternate_namer import BladeAlternateNamer
from sotd_collator.base_name_extractor import BaseNameExtractor


class BladeNameExtractor(BaseNameExtractor):
    """
    From a given comment, extract the razor name
    """

    @cached_property
    def alternative_namer(self):
        return BladeAlternateNamer()

    @property
    def detect_regexps(self):
        blade_name_re = r"""\w\t ./\-_()#;&\'\"|<>:$~"""

        return [
            re.compile(r'^[*\s\-+/]*blade\s*[:*\-\\+\s/]+\s*([{0}]+)(?:\+|,|\n|$)'.format(blade_name_re),
                       re.MULTILINE | re.IGNORECASE),  # TTS and similar
            re.compile(r'\*blade\*:.*\*\*([{0}]+)\*\*'.format(blade_name_re), re.MULTILINE | re.IGNORECASE),  # sgrddy
            # re.compile(r'^\*\*Safety Razor\*\*\s*-\s*([{0}]+)[+,\n]'.format(blade_name_re),
            #            re.MULTILINE | re.IGNORECASE),  # **Safety Razor** - RazoRock - Gamechanger 0.84P   variant

        ]

    @BaseNameExtractor.post_process_name
    def get_name(self, comment_text):
        comment_text = self._to_ascii(comment_text)
        for detector in self.detect_regexps:
            res = detector.search(comment_text)
            if res:
                # remove blade count - eg Astra (3)
                return re.sub(r'[()\d]', '', res.group(1)).strip()

        principal_name = self.alternative_namer.get_principal_name(comment_text)
        if principal_name:
            return principal_name

        return None
