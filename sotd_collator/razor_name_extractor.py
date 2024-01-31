import re
from functools import cached_property
from sotd_collator.razor_alternate_namer import RazorAlternateNamer
from sotd_collator.base_name_extractor import BaseNameExtractor


class RazorNameExtractor(BaseNameExtractor):
    """
    From a given comment, extract the razor name
    """

    @cached_property
    def alternative_namer(self):
        return RazorAlternateNamer()

    @cached_property
    def detect_regexps(self):
        razor_name_re = r"""\w\t ./\-_()#;&\'\"|<>:$~"""

        return [
            re.compile(
                r"^[*\s\-+/]*Razor\s*[:*\-\\+\s/]+\s*([{0}]+)(?:\+|,|\n|$)".format(
                    razor_name_re
                ),
                re.MULTILINE | re.IGNORECASE,
            ),  # TTS and similar
            re.compile(
                r"\*Razor\*:.*\*\*([{0}]+)\*\*".format(razor_name_re),
                re.MULTILINE | re.IGNORECASE,
            ),  # sgrddy
            re.compile(
                r"^\*\*Safety Razor\*\*\s*-\s*([{0}]+)[+,\n]".format(razor_name_re),
                re.MULTILINE | re.IGNORECASE,
            ),  # **Safety Razor** - RazoRock - Gamechanger 0.84P   variant
            re.compile(
                r"^[*\s\-+/]*Razor\s*[:*\-\\+\s/]+\s*\[*([{0}]+)(?:\+|,|\n|$|]\()".format(
                    razor_name_re
                ),
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
            # at some point this can be genericised in to a block words / phrases list to catch razorock too
            if res and "and blade note" in res.group(1).lower():
                continue

            # catch case where we match against razorock
            if res and not (len(res.group(1)) >= 3 and res.group(1)[0:3] == "ock"):
                result = res.group(1).strip()
                if len(result) > 0:
                    return result

        # principal_name = self.alternative_namer.get_principal_name(comment_text)
        # if principal_name:
        #     return principal_name

        return None
