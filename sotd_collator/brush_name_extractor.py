import re
from functools import cached_property
from sotd_collator.brush_alternate_namer import BrushAlternateNamer
from sotd_collator.base_name_extractor import BaseNameExtractor


class BrushNameExtractor(BaseNameExtractor):
    """
    From a given comment, extract the razor name
    """

    @cached_property
    def alternative_namer(self):
        return BrushAlternateNamer()

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
        for detector in self.detect_regexps:
            res = detector.search(comment_text)

            # catch case where some jerk writes ❧ Brush Notes or similar
            # at some point this can be genericised in to a block words / phrases list to catch razorock too
            if res and res.group(1) == 'Notes':
                continue

            if res:
                return res.group(1).strip()

        principal_name = self.alternative_namer.get_principal_name(comment_text)
        if principal_name:
            return principal_name

        return None
