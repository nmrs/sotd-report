import re
from functools import cached_property
from sotd_collator.base_name_extractor import BaseNameExtractor


class RazorNameExtractor(BaseNameExtractor):
    """
    From a given comment, extract the razor name
    """

    # patterns people use repeatedly to document the brush they used
    # but that we can't match to anything
    GARBAGE = ["and blade performance", r"^n/a$", "^buddies", "help me identify it"]

    @cached_property
    def detect_regexps(self):
        razor_name_re = r"""\w\t ./\-_()#;&\'\"|<>:$~"""

        return [
            re.compile(
                rf"^[*\s\-+/]*Razor\s*[:*\-\\+\s/]+\s*([{razor_name_re}]+)(?:\+|,|\n|$)",
                re.MULTILINE | re.IGNORECASE,
            ),  # TTS and similar
            re.compile(
                rf"\*Razor\*:.*\*\*([{razor_name_re}]+)\*\*",
                re.MULTILINE | re.IGNORECASE,
            ),  # sgrddy
            re.compile(
                rf"^\*\*Safety Razor\*\*\s*-\s*([{razor_name_re}]+)[+,\n]",
                re.MULTILINE | re.IGNORECASE,
            ),  # **Safety Razor** - RazoRock - Gamechanger 0.84P   variant
            re.compile(
                rf"^[*\s\-+/]*Razor\s*[:*\-\\+\s/]+\s*\[*([{razor_name_re}]+)(?:\+|,|\n|$|]\()",
                re.MULTILINE | re.IGNORECASE,
            ),  # TTS style with link to eg imgur
        ]

    # @BaseNameExtractor.post_process_name
    def get_name(self, comment):
        if "razor" in comment:
            return comment["razor"]

        comment_text = self._to_ascii(comment["body"])
        for detector in self.detect_regexps:
            res = detector.search(comment_text)
            # catch case where some jerk writes ❧ Razor and Blade Notes or similar
            # at some point this can be genericised
            # to a block words / phrases list to catch razorock too
            if res and "and blade note" in res.group(1).lower():
                continue

            # catch case where we match against razorock
            if res and not (len(res.group(1)) >= 3 and res.group(1)[0:3] == "ock"):
                result = res.group(1).strip()
                if len(result) > 0:
                    for pattern in self.GARBAGE:
                        if re.search(pattern, result, re.IGNORECASE):
                            return None
                    return result

        # principal_name = self.alternative_namer.get_principal_name(comment_text)
        # if principal_name:
        #     return principal_name

        return None
