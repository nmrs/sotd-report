import re
from functools import cached_property
from sotd_collator.base_name_extractor import BaseNameExtractor


class BladeNameExtractor(BaseNameExtractor):
    """
    From a given comment, extract the razor name
    """

    # patterns people use repeatedly to document the brush they used
    # but that we can't match to anything
    GARBAGE = []

    @cached_property
    def _garbage(self):
        return self.BASE_GARBAGE + self.GARBAGE

    @cached_property
    def detect_regexps(self):
        blade_name_re = r"""\w\t ./\-_()\[\]#;&\'\"|<>:$~"""

        return [
            re.compile(
                rf"\*blade[\*:\s]+([{blade_name_re}]+)\*\*",
                re.MULTILINE | re.IGNORECASE,
            ),  # sgrddy
            re.compile(
                rf"^[*\s\-+/]*blade\s*[:*\-\\+\s/]+\s*([{blade_name_re}]+)(?:\+|,|\n|$)",
                re.MULTILINE | re.IGNORECASE,
            ),  # TTS and similar
            # re.compile(r'^\*\*Safety Razor\*\*\s*-\s*([{0}]+)[+,\n]'.format(blade_name_re),
            #            re.MULTILINE | re.IGNORECASE),  # **Safety Razor** - RazoRock - Gamechanger 0.84P   variant
        ]

    @BaseNameExtractor.post_process_name
    def get_name(self, comment):
        if "blade" in comment:
            return comment["blade"]

        comment_text = self._to_ascii(comment["body"])
        for detector in self.detect_regexps:
            res = detector.search(comment_text)
            if res:
                result = str(res.group(1)).strip()
                if len(result) > 0:
                    for pattern in self._garbage:
                        if re.search(pattern, result, re.IGNORECASE):
                            return None
                    return result

        # principal_name = self.alternative_namer.get_principal_name(comment_text)
        # if principal_name:
        #     return principal_name

        return None
