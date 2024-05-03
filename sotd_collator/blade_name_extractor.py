import re
from functools import cached_property
from sotd_collator.base_name_extractor import BaseNameExtractor


class BladeNameExtractor(BaseNameExtractor):
    """
    From a given comment, extract the blade name
    """

    # patterns people use repeatedly to document the brush they used
    # but that we can't match to anything
    GARBAGE = []

    def _garbage(self):
        return self.GARBAGE

    @cached_property
    def detect_regexps(self):
        # blade_name_re = r"""\w\t ./\-_()#;&\'\"|<>:$~"""

        # prefix = r"[*\s\-+/]*blade\s*[:*\-\\+\s/]+\s*\""
        # sgrddy =

        return [
            # self.sgrddy_detector("Blade"),
            self.imgur_detector("Blade"),
            self.tts_detector("Blade"),
        ]

    @BaseNameExtractor.post_process_name
    def get_name(self, comment):
        if "blade" in comment:
            return comment["blade"]

        return super().get_name(comment)

        # comment_text = self._to_ascii(comment["body"])
        # for detector in self.detect_regexps:
        #     res = detector.search(comment_text)
        #     if res:
        #         result = str(res.group(1)).strip()
        #         if len(result) > 0:
        #             # for pattern in self._garbage:
        #             #     if re.search(pattern, result, re.IGNORECASE):
        #             #         return None
        #             if res.lastindex > 1:
        #                 use_count = res.group(2).strip()
        #                 if len(use_count) > 0:
        #                     return f"{result} ({use_count})"
        #             return result

        # principal_name = self.alternative_namer.get_principal_name(comment_text)
        # if principal_name:
        #     return principal_name

        # return None
